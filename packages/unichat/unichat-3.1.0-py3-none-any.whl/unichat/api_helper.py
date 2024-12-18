import anthropic
import openai
from mistralai import Mistral
from typing import List, Dict, Any, Generator, Iterator
import json
import time

from .models import MODELS_LIST, MODELS_MAX_TOKEN

class _ApiHelper:
    DEFAULT_MAX_TOKENS = 4096

    def __init__(self, api_key):
        self.api_key = api_key
        self.models = MODELS_LIST
        self.max_tokens = MODELS_MAX_TOKEN
        self.api_client = None

    def _get_max_tokens(self, model_name: str) -> int:
        return self.max_tokens.get(model_name, self.DEFAULT_MAX_TOKENS)

    def _get_client(self, model_name: str):
        if self.api_client is not None:
            return self.api_client

        if model_name in self.models["mistral_models"]:
            client = Mistral(api_key=self.api_key)
        elif model_name in self.models["anthropic_models"]:
            client = anthropic.Anthropic(api_key=self.api_key)
        elif model_name in self.models["grok_models"]:
            client = openai.OpenAI(api_key=self.api_key, base_url="https://api.x.ai/v1")
        elif model_name in self.models["gemini_models"]:
            client = openai.OpenAI(api_key=self.api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        elif model_name in self.models["openai_models"]:
            client = openai.OpenAI(api_key=self.api_key)
        else:
            raise ValueError(f"Model '{model_name}' not found.")

        self.api_client = client
        return client

    def _set_defaults(
        self,
        model_name: str,
        conversation: List[Dict[str, str]]
    ):
        role = ""
        # Extract the system instructions from the conversation.
        if model_name in self.models["anthropic_models"]:
            role = conversation[0]["content"] if conversation[0]["role"] == "system" else ""
            conversation = [message for message in conversation if message["role"] != "system"]
        elif model_name.startswith("o1"):
            # OpenAI "o1" models do not support system role as part of the beta limitations. More info here: https://platform.openai.com/docs/guides/reasoning/beta-limitations
            if conversation[0]["role"] == "system":
                system_content = conversation[0]["content"]
                conversation[1]["content"] = f"{system_content}\n\n{conversation[1]['content']}"
                conversation = [message for message in conversation if message["role"] != "system"]

        client = self._get_client(model_name)
        return client, conversation, role

    def transform_tools(self, input_tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform input tools to OpenAI function format."""
        return [{
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"]
            }
        } for tool in input_tools]

    def normalize_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize different tool formats to a standard format."""
        normalized_tools = []
        try:
            for tool in tools:
                if not isinstance(tool, dict):
                    raise ValueError(f"Invalid tool format. Expected a dictionary.")

                if "type" in tool and "function" in tool:
                    # Handle OutputTool format
                    function = tool.get("function", {})
                    if not isinstance(function, dict) or "name" not in function or "description" not in function:
                        raise ValueError("Malformed function object in tool")
                    normalized_tools.append({
                        "name": function["name"],
                        "description": function["description"],
                        "input_schema": function.get("parameters", {})
                    })
                else:
                    # Handle OriginalTool format
                    name = tool.get("name")
                    description = tool.get("description")
                    input_schema = (
                        tool.get("inputSchema") or
                        tool.get("input_schema") or
                        tool.get("parameters")
                    )

                    if not input_schema:
                        raise KeyError(
                            f"Tool is missing 'inputSchema', 'input_schema', or 'parameters'"
                        )

                    if not name or not description:
                        raise ValueError(f"Tool is missing required keys 'name' or 'description'")

                    normalized_tools.append({
                        "name": name,
                        "description": description,
                        "input_schema": input_schema
                    })

            return normalized_tools

        except KeyError as ke:
            raise KeyError(f"Unexpected tool format: {ke}")
        except ValueError as ve:
            raise ValueError(f"Validation error: {ve}")
        except Exception as e:
            raise Exception(f"Error processing tools: {e}")


    def transform_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform GPT tool calls to content blocks."""
        if not isinstance(tool_calls, list):
            return []

        return [{
            "type": "tool_use",
            "id": call.get("id", ""),
            "name": call.get("function", {}).get("name", ""),
            "input": json.loads(call.get("function", {}).get("arguments", "{}"))
        } for call in tool_calls]

    def transform_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform messages for compatibility between different formats."""
        if not isinstance(messages, list):
            return []

        transformed_messages = []
        i = 0

        while i < len(messages):
            message = messages[i]
            if not isinstance(message, dict):
                i += 1
                continue

            if (message.get("role") == "assistant" and
                isinstance(message.get("tool_calls"), list)):
                # Transform assistant message with tool calls
                transformed_messages.append({
                    "role": "assistant",
                    "content": self.transform_tool_calls(message["tool_calls"])
                })

                # Look for corresponding tool response
                if (i + 1 < len(messages) and
                    isinstance(messages[i + 1], dict) and
                    messages[i + 1].get("role") == "tool"):
                    tool_msg = messages[i + 1]
                    transformed_messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_msg.get("tool_call_id", ""),
                            "content": tool_msg.get("content", "")
                        }]
                    })
                    i += 1  # Skip the tool message since we've handled it
            elif message.get("role") != "tool":  # Skip tool messages as they're handled above
                transformed_messages.append(message)

            i += 1

        return transformed_messages

    def convert_claude_to_gpt(self, claude_response: object) -> object:
        text_content = []
        tool_calls = []
        has_tool_use = False

        if hasattr(claude_response, "content") and isinstance(claude_response.content, list):
            for block in claude_response.content:
                if isinstance(block, object):
                    if getattr(block, "type", None) == "text":
                        text_content.append(getattr(block, "text", ""))
                    elif getattr(block, "type", None) == "tool_use":
                        has_tool_use = True
                        # Create the tool call dictionary first
                        tool_call_dict = {
                            "id": getattr(block, "id", ""),
                            "type": "function",
                            "function": {
                                "name": getattr(block, "name", ""),
                                "arguments": json.dumps(getattr(block, "input", {}))
                            }
                        }
                        # Convert dictionary to object
                        function_obj = type('obj', (object,), tool_call_dict["function"])
                        tool_call = type('obj', (object,), {
                            "id": tool_call_dict["id"],
                            "type": tool_call_dict["type"],
                            "function": function_obj
                        })
                        tool_calls.append(tool_call)

        # Create message dictionary with all attributes
        message_dict = {
            "role": getattr(claude_response, "role", "assistant"),
            "content": "".join(text_content) if text_content else None,
        }

        # Only include tool_calls in the message dictionary if there was a tool_use block
        if has_tool_use:
            message_dict["tool_calls"] = tool_calls

        # Create the message object with all attributes included
        message_obj = type('obj', (object,), message_dict)

        # Get the stop reason from Claude's response
        stop_reason = getattr(claude_response, "stop_reason", None)

        # Determine finish reason based on stop reason and tool use
        if stop_reason == "tool_use":
            finish_reason = "tool_calls"
        elif stop_reason == "end_turn":
            finish_reason = "stop"
        else:
            finish_reason = stop_reason

        # Create the choice object with the message
        choice_obj = type('obj', (object,), {
            "index": 0,
            "message": message_obj,
            "logprobs": None,
            "finish_reason": finish_reason
        })

        usage_obj = type('obj', (object,), {
            "prompt_tokens": getattr(getattr(claude_response, "usage", {}), "input_tokens", 0),
            "completion_tokens": getattr(getattr(claude_response, "usage", {}), "output_tokens", 0),
            "total_tokens": (getattr(getattr(claude_response, "usage", {}), "input_tokens", 0) +
                        getattr(getattr(claude_response, "usage", {}), "output_tokens", 0))
        })

        return type('obj', (object,), {
            "id": getattr(claude_response, "id", ""),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": getattr(claude_response, "model", ""),
            "choices": [choice_obj],
            "usage": usage_obj,
            "system_fingerprint": "unichat"
        })


    def transform_response(self, response: object) -> object:
        """Transform API response to standard format."""
        if not isinstance(response, object):
            return type('obj', (object,), {})

        usage = getattr(response, "usage", {})
        transformed = type('obj', (object,), {
            **response.__dict__,
            "usage": type('obj', (object,), {
                "prompt_tokens": getattr(usage, "promptTokens", 0),
                "completion_tokens": getattr(usage, "completionTokens", 0),
                "total_tokens": getattr(usage, "totalTokens", 0)
            }),
            "choices": []
        })

        for choice in getattr(response, "choices", []):
            if not isinstance(choice, object):
                continue

            transformed_choice = type('obj', (object,), {
                **choice.__dict__,
                "message": type('obj', (object,), {
                    **getattr(choice, "message", {}).__dict__
                }),
                "finish_reason": getattr(choice, "finishReason", None)
            })

            if hasattr(getattr(choice, "message", {}), "toolCalls"):
                setattr(transformed_choice.message, "tool_calls", [
                    type('obj', (object,), {**tool_call.__dict__})
                    for tool_call in getattr(choice.message, "toolCalls")
                ])
                if hasattr(transformed_choice.message, "toolCalls"):
                    delattr(transformed_choice.message, "toolCalls")

            transformed.choices.append(transformed_choice)

        return transformed

    def transform_stream(self, response: object) -> object:
        """Transform Claude's streaming response to OpenAI format."""
        for chunk in response:
            chunk_type = getattr(chunk, "type")

            if chunk_type == "message_start":
                message = getattr(chunk, "message")
                yield type('obj', (object,), {
                    "id": getattr(message, "id"),
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": getattr(message, "model"),
                    "system_fingerprint": "unichat",
                    "choices": [type('obj', (object,), {
                        "index": 0,
                        "delta": type('obj', (object,), {
                            "role": getattr(message, "role"),
                            "content": "",
                        }),
                        "logprobs": None,
                        "finish_reason": None
                    })]
                })

            elif chunk_type == "content_block_start":
                content_block = getattr(chunk, "content_block")
                if getattr(content_block, "type") == "tool_use":
                    yield type('obj', (object,), {
                        "object": "chat.completion.chunk",
                        "choices": [type('obj', (object,), {
                            "index": 0,
                            "delta": type('obj', (object,), {
                                "tool_calls": [type('obj', (object,), {
                                    "index": 0,
                                    "id": getattr(content_block, "id"),
                                    "type": "function",
                                    "function": type('obj', (object,), {
                                        "name": getattr(content_block, "name"),
                                        "arguments": ""
                                    })
                                })]
                            }),
                            "logprobs": None,
                            "finish_reason": None
                        })]
                    })

            elif chunk_type == "content_block_delta":
                delta = getattr(chunk, "delta")
                if getattr(delta, "type") == "text_delta":
                    yield type('obj', (object,), {
                        "object": "chat.completion.chunk",
                        "choices": [type('obj', (object,), {
                            "index": 0,
                            "delta": type('obj', (object,), {
                                "content": getattr(delta, "text")
                            }),
                            "logprobs": None,
                            "finish_reason": None
                        })]
                    })
                elif getattr(delta, "type") == "input_json_delta":
                    yield type('obj', (object,), {
                        "object": "chat.completion.chunk",
                        "choices": [type('obj', (object,), {
                            "index": 0,
                            "delta": type('obj', (object,), {
                                "tool_calls": [type('obj', (object,), {
                                    "function": type('obj', (object,), {
                                        "arguments": getattr(delta, "partial_json")
                                    })
                                })]
                            }),
                            "logprobs": None,
                            "finish_reason": None
                        })]
                    })

            elif chunk_type == "message_delta":
                delta = getattr(chunk, "delta")
                if hasattr(delta, "stop_reason"):
                    stop_reason = getattr(delta, "stop_reason")
                    finish_reason = ("tool_calls" if stop_reason == "tool_use" else
                                "stop" if stop_reason == "end_turn" else
                                stop_reason)
                    yield type('obj', (object,), {
                        "object": "chat.completion.chunk",
                        "choices": [type('obj', (object,), {
                            "index": 0,
                            "delta": type('obj', (object,), {}),
                            "logprobs": None,
                            "finish_reason": finish_reason
                        })]
                    })

    def transform_stream_chunk(self, stream: Iterator[Any]) -> Generator[object, None, None]:
        """Transform stream chunks to standard format."""
        try:
            for chunk in stream:
                if not chunk or not hasattr(chunk, 'data'):
                    continue

                data = getattr(chunk, "data")
                if not isinstance(data, object):
                    continue

                # Create transformed chunk without system attributes
                base_dict = {k: v for k, v in data.__dict__.items()
                            if not k.startswith('__')}
                transformed_chunk = type('obj', (object,), base_dict)

                # Transform usage only if present and not None
                if hasattr(data, "usage") and data.usage is not None:
                    usage = data.usage
                    if not isinstance(usage, type('Unset', (), {})):
                        setattr(transformed_chunk, "usage", type('obj', (object,), {
                            "prompt_tokens": getattr(usage, "promptTokens", 0),
                            "completion_tokens": getattr(usage, "completionTokens", 0),
                            "total_tokens": getattr(usage, "totalTokens", 0)
                        }))
                else:
                    if hasattr(transformed_chunk, "usage"):
                        delattr(transformed_chunk, "usage")

                # Transform choices
                if hasattr(data, "choices"):
                    setattr(transformed_chunk, "choices", [])
                    for choice in getattr(data, "choices"):
                        transformed_choice = type('obj', (object,), {
                            k: v for k, v in choice.__dict__.items()
                            if not k.startswith('__')
                        })

                        if hasattr(choice, "delta"):
                            delta = getattr(choice, "delta")
                            delta_dict = {k: v for k, v in delta.__dict__.items()
                                        if not k.startswith('__')}
                            transformed_delta = type('obj', (object,), delta_dict)

                            if (hasattr(delta, "toolCalls") and
                                getattr(delta, "toolCalls") is not None and
                                not isinstance(getattr(delta, "toolCalls"), type('Unset', (), {}))):
                                tool_calls = getattr(delta, "toolCalls")
                                setattr(transformed_delta, "tool_calls", [
                                    type('obj', (object,), {
                                        k: v for k, v in tool_call.__dict__.items()
                                        if not k.startswith('__')
                                    })
                                    for tool_call in tool_calls
                                ])
                                if hasattr(transformed_delta, "toolCalls"):
                                    delattr(transformed_delta, "toolCalls")

                            setattr(transformed_choice, "delta", transformed_delta)

                        if hasattr(choice, "finishReason"):
                            setattr(transformed_choice, "finish_reason", getattr(choice, "finishReason"))
                            if hasattr(transformed_choice, "finishReason"):
                                delattr(transformed_choice, "finishReason")

                        getattr(transformed_chunk, "choices").append(transformed_choice)

                yield transformed_chunk

        except Exception as e:
            raise Exception(f"Error processing stream chunk: {e}")