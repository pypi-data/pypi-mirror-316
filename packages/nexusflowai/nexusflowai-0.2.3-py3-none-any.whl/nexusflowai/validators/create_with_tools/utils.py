from typing import Any, Dict, List, Tuple, Optional, Union

from dataclasses import dataclass

from copy import deepcopy

from keyword import iskeyword

from ast import AST, parse as ast_parse
from ast import Call, Import, ImportFrom, NodeVisitor, Name

import json
import json_repair

from openai.types.chat import (
    ChatCompletionToolParam,
    ChatCompletionMessageToolCallParam,
    CompletionCreateParams,
    ChatCompletionMessageParam,
    ChatCompletionContentPartParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionContentPartInputAudioParam,
    ChatCompletionContentPartRefusalParam,
)
from openai.types.chat.chat_completion_tool_choice_option_param import (
    ChatCompletionNamedToolChoiceParam,
)

from nexusflowai.types.chat_completion_message import NexusflowAIChatCompletionMessage


ALLOWED_ROLES = [
    "system",
    "tool",
    "user",
    "assistant",
]

ALLOWED_IMPORTS = [
    "typing",
    "itertools",
    "collections",
    "tabulate",
    "dataclasses",
    "requests",
    "enum",
    "__future__",
]
DISALLOWED_FUNCTIONS = ["eval", "exec", "setattr", "locals", "globals"]


class SecurityVisitor(NodeVisitor):
    def visit_Call(self, node: Call):
        if isinstance(node.func, Name):
            func_name = node.func.id
            if func_name in DISALLOWED_FUNCTIONS:
                raise ValueError(
                    f"Found dangerous call to {func_name} at line {node.lineno}. Disallowed functions: {DISALLOWED_FUNCTIONS}"
                )

        self.generic_visit(node)

    def visit_Import(self, node: Import) -> Any:
        import_names = [a.name for a in node.names]
        self.check_imports(node, import_names)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ImportFrom) -> Any:
        import_names = [node.module]
        self.check_imports(node, import_names)

        self.generic_visit(node)

    def check_imports(
        self, node: Union[Import, ImportFrom], import_names: List[str]
    ) -> None:
        disallowed_import_names = [n for n in import_names if n not in ALLOWED_IMPORTS]
        if disallowed_import_names:
            raise ImportError(
                f"Not allowed to import {disallowed_import_names} at line {node.lineno}. Allowed imports include {ALLOWED_IMPORTS}"
            )


class CodeExecutionHelper:
    def clean_input(self, source: str) -> Tuple[str, Optional[AST]]:
        source = source.strip()
        if len(source) == 0:
            return source, None

        try:
            tree = ast_parse(source)
        except SyntaxError as e:
            new_source = self._try_fix_syntax_error(e, source)
            try:
                tree = ast_parse(new_source)
                source = new_source
            except:  # pylint: disable=bare-except
                tree = None
        except:  # pylint: disable=bare-except
            tree = None

        return source, tree

    @staticmethod
    def _try_fix_syntax_error(error: SyntaxError, source: str) -> str | None:
        res = None
        if not error.args:
            return res

        error_message = error.args[0]
        res = source
        if error_message == "'(' was never closed":
            res = f"{source})"
        elif error_message == "unmatched ')'":
            res = source.removesuffix(")")
        else:
            """
            Unescaped quotes can manifest as a variety of error messages including:
            - unterminated string literal
            - Perhaps you forgot a comma?

            Hence we use this as a fallback case
            """

            possible_first_quotes = {'="': '")', "='": "')"}
            for possible_first_quote, last_quote in possible_first_quotes.items():
                if possible_first_quote not in source:
                    continue

                res = source.split(possible_first_quote, maxsplit=1)
                res = "='''".join(res)
                res = res.split(last_quote, maxsplit=1)
                res = "''')".join(res)

        return res

    def check_security(self, tree: AST) -> None:
        security_visitor = SecurityVisitor()
        try:
            security_visitor.visit(tree)
        except ValueError as e:
            raise TypeError from e


"""
A smattering of symbols that are invalid for function and argument names
These are all replaced with "_" downstream.
This is a translation table used in `str.translate`.
"""
INVALID_NAME_CHARS = str.maketrans(dict.fromkeys(" !%&(*+,-/<=>@[^|~", "_"))


def clean_str(s: str) -> str:
    s = s.translate(INVALID_NAME_CHARS)
    if iskeyword(s):
        s = f"_{s}"
    return s


def clean_raw_response(raw_response: str) -> str:
    response = raw_response.split("Thought:")[0]
    response = response.strip()
    return response


@dataclass
class CleanedFunction:
    dirty_name: str
    dirty_argument_names: List[str]

    def __post_init__(self) -> None:
        self.clean_name = clean_str(self.dirty_name)
        self.clean_argument_names = list(map(clean_str, self.dirty_argument_names))

        self.argument_names_d2c = dict(
            zip(self.dirty_argument_names, self.clean_argument_names)
        )
        self.argument_names_c2d = dict(
            zip(self.clean_argument_names, self.dirty_argument_names)
        )

    def clean_tool_param(
        self, tool: ChatCompletionToolParam
    ) -> ChatCompletionToolParam:
        tool = deepcopy(tool)

        function = tool["function"]
        function["name"] = self.clean_name

        properties = function["parameters"].get("properties")
        if properties:
            properties = {
                self.argument_names_d2c.get(k, k): v for k, v in properties.items()
            }
            function["parameters"]["properties"] = properties

        required = function["parameters"].get("required")
        if required:
            function["parameters"]["required"] = [
                self.argument_names_d2c.get(k, k) for k in required
            ]

        return tool

    def clean_tool_call_param(
        self, tool_call: ChatCompletionMessageToolCallParam
    ) -> ChatCompletionMessageToolCallParam:
        tool_call = deepcopy(tool_call)

        function = tool_call["function"]
        function["name"] = self.clean_name

        arguments = json_repair.loads(function["arguments"])
        arguments = {self.argument_names_d2c.get(k, k): v for k, v in arguments.items()}
        function["arguments"] = json.dumps(arguments)

        return tool_call

    def dirty_function_call_dict(
        self, clean_name: str, clean_kwargs: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        assert self.clean_name == clean_name
        return self.dirty_name, {
            self.argument_names_c2d.get(k, k): v for k, v in clean_kwargs.items()
        }

    @classmethod
    def from_tool_param(cls, tool: ChatCompletionToolParam) -> "CleanedFunction":
        function = tool["function"]
        function_properties = function["parameters"].get("properties", dict())
        cf = cls(
            dirty_name=function["name"],
            dirty_argument_names=list(function_properties),
        )

        return cf


def resolve_tools_and_tool_choice(
    tools: List[ChatCompletionToolParam],
    tool_choice: ChatCompletionNamedToolChoiceParam,
) -> Tuple[List[ChatCompletionToolParam], ChatCompletionNamedToolChoiceParam]:
    """
    Supported tool choices:
    - `required`: [Not with OpenAI parity] The model will always output a function call except when it thinks the trajectory is finished (this is the way the model is trained).
    - `auto`: Same as `required`.
    - `none`: The model will see all of the tools but is forced to chat.
    - `{"type": "function": "function": {"name": <>}}`: Force a function call
    - `required_with_chat`: The model will see all of the tools and an additional chat function. Including the additional chat function, this tool choice then has the same behavior as `required`
    """
    if not tool_choice:
        return tools, tool_choice

    tools = tools.copy()
    if tool_choice in ["required_with_chat", "none"]:
        if tool_choice == "required_with_chat":
            tool_choice = "required"
        elif tool_choice == "none":
            tool_choice = {"type": "function", "function": {"name": "chat"}}
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": "chat",
                    "description": """This function is used to chat with the user. Use this function to communicate the required information to the user, ask the user for more information, or to let the user know that something has been accomplished.

Don't make assumptions about what values to plug into functions. Use this function to ask for clarification if a user request is ambiguous.

You must call at least one function. If you don't know which function to call, please call this chat function. You can use this function as an argument in nested calls to represent information that is necessary.""",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "A clear message that the user will read.",
                            },
                        },
                        "required": ["message"],
                        "additionalProperties": False,
                    },
                },
            }
        )

    return tools, tool_choice


def get_tool_choice_prefix(
    tool_choice: ChatCompletionNamedToolChoiceParam | None,
    dirty_function_name_to_cf: Dict[str, CleanedFunction],
) -> str | None:
    if not isinstance(tool_choice, dict):
        return None

    tool_choice: ChatCompletionNamedToolChoiceParam
    dirty_function_name = tool_choice["function"]["name"]

    assert (
        dirty_function_name in dirty_function_name_to_cf
    ), f"Did not find any tools with the `tool_choice` function name `{dirty_function_name}`"

    cleaned_name = dirty_function_name_to_cf[dirty_function_name].clean_name

    return cleaned_name


def _parse_content_parts(
    content_parts: List[
        Union[ChatCompletionContentPartParam, ChatCompletionContentPartRefusalParam]
    ]
) -> List[str]:
    if content_parts == []:
        return []

    content_strs = []

    for part in content_parts:
        part_type = part["type"]

        match part_type:
            case "text":
                text = part["text"]
                content_strs.append(text)

            case "image_url":
                raise NotImplementedError(
                    f"{ChatCompletionContentPartImageParam} is not supported!"
                )

            case "input_audio":
                raise NotImplementedError(
                    f"{ChatCompletionContentPartInputAudioParam} is not supported!"
                )

            case "refusal":
                raise NotImplementedError(
                    f"{ChatCompletionContentPartRefusalParam} ist not supported!"
                )

    return content_strs


def _flatten_chat_completion_create_params_messages_content_parts(
    create_params: CompletionCreateParams,
) -> CompletionCreateParams:
    """
    Expands ContentPartParams to individual messages.
    Used for chat flows in backend.
    """

    def _parse_chat_message_content_parts(
        message: ChatCompletionMessageParam,
        content_parts: List[
            Union[ChatCompletionContentPartParam, ChatCompletionContentPartRefusalParam]
        ],
    ) -> List[ChatCompletionMessageParam]:
        # Expanded messages:
        # The last message is original message iwth all calls / inputs.
        # The other messages only have the role and content information.
        messages: List[ChatCompletionMessageParam] = [
            *[
                {
                    "content": None,
                    "role": message["role"],
                }
                for _ in range(len(content_parts) - 1)
            ],
            message,
        ]
        if "name" in message:
            for sub_message in messages:
                sub_message["name"] = message["name"]

        for i, content_str in enumerate(_parse_content_parts(content_parts)):
            messages[i]["content"] = content_str

        return messages

    def _expand_chat_message_content(
        message: ChatCompletionMessageParam,
    ) -> List[ChatCompletionMessageParam]:
        content = message.get("content")

        if isinstance(content, str):
            return [message]

        if content is None:
            content = []

        result = _parse_chat_message_content_parts(message, content)

        return result

    def _expand_chat_messages(
        messages: List[ChatCompletionMessageParam],
    ) -> List[ChatCompletionMessageParam]:
        conversation = []

        for message in messages:
            sub_messages = _expand_chat_message_content(message)
            conversation.extend(sub_messages)

        return conversation

    create_params["messages"] = _expand_chat_messages(create_params["messages"])

    return create_params


# Tool call ID to nexusflowai_extras
tci_to_nexusflowai_extras: Dict[str, Dict[str, Any]] = dict()


def add_nexusflowai_extras_to_messages(
    messages: List[ChatCompletionMessageParam],
) -> List[ChatCompletionMessageParam]:
    messages = deepcopy(messages)
    for message in messages:
        if message["role"] != "assistant" or not message.get("tool_calls"):
            continue

        for tool_call in message["tool_calls"]:
            if tci_to_nexusflowai_extras.get(tool_call["id"]):
                message["nexusflowai_extras"] = tci_to_nexusflowai_extras[
                    tool_call["id"]
                ]
                break

    return messages


def store_nexusflowai_extras_in_memory(
    message: NexusflowAIChatCompletionMessage,
) -> None:
    tool_calls = message.tool_calls or []
    for tool_call in tool_calls:
        tci_to_nexusflowai_extras[tool_call.id] = message.nexusflowai_extras
