from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Literal, Optional, overload

from pydantic import BaseModel

from ._chat import Chat
from ._content import (
    Content,
    ContentImageInline,
    ContentImageRemote,
    ContentJson,
    ContentText,
    ContentToolRequest,
    ContentToolResult,
)
from ._logging import log_model_default
from ._provider import Provider
from ._tokens import tokens_log
from ._tools import Tool, basemodel_to_param_schema
from ._turn import Turn, normalize_turns, user_turn

if TYPE_CHECKING:
    from google.generativeai.types.content_types import (
        ContentDict,
        FunctionDeclaration,
        PartType,
    )
    from google.generativeai.types.generation_types import (
        AsyncGenerateContentResponse,
        GenerateContentResponse,
        GenerationConfig,
    )

    from .types.google import ChatClientArgs, SubmitInputArgs
else:
    GenerateContentResponse = object


def ChatGoogle(
    *,
    system_prompt: Optional[str] = None,
    turns: Optional[list[Turn]] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    kwargs: Optional["ChatClientArgs"] = None,
) -> Chat["SubmitInputArgs", GenerateContentResponse]:
    """
    Chat with a Google Gemini model.

    Prerequisites
    -------------

    ::: {.callout-note}
    ## API key

    To use Google's models (i.e., Gemini), you'll need to sign up for an account
    and [get an API key](https://ai.google.dev/gemini-api/docs/get-started/tutorial?lang=python).
    :::

    ::: {.callout-note}
    ## Python requirements

    `ChatGoogle` requires the `google-generativeai` package
    (e.g., `pip install google-generativeai`).
    :::

    Examples
    --------

    ```python
    import os
    from chatlas import ChatGoogle

    chat = ChatGoogle(api_key=os.getenv("GOOGLE_API_KEY"))
    chat.chat("What is the capital of France?")
    ```

    Parameters
    ----------
    system_prompt
        A system prompt to set the behavior of the assistant.
    turns
        A list of turns to start the chat with (i.e., continuing a previous
        conversation). If not provided, the conversation begins from scratch.
        Do not provide non-`None` values for both `turns` and `system_prompt`.
        Each message in the list should be a dictionary with at least `role`
        (usually `system`, `user`, or `assistant`, but `tool` is also possible).
        Normally there is also a `content` field, which is a string.
    model
        The model to use for the chat. The default, None, will pick a reasonable
        default, and warn you about it. We strongly recommend explicitly choosing
        a model for all but the most casual use.
    api_key
        The API key to use for authentication. You generally should not supply
        this directly, but instead set the `GOOGLE_API_KEY` environment variable.
    kwargs
        Additional arguments to pass to the `genai.GenerativeModel` constructor.

    Returns
    -------
    Chat
        A Chat object.

    Limitations
    -----------
    `ChatGoogle` currently doesn't work with streaming tools.

    Note
    ----
    Pasting an API key into a chat constructor (e.g., `ChatGoogle(api_key="...")`)
    is the simplest way to get started, and is fine for interactive use, but is
    problematic for code that may be shared with others.

    Instead, consider using environment variables or a configuration file to manage
    your credentials. One popular way to manage credentials is to use a `.env` file
    to store your credentials, and then use the `python-dotenv` package to load them
    into your environment.

    ```shell
    pip install python-dotenv
    ```

    ```shell
    # .env
    GOOGLE_API_KEY=...
    ```

    ```python
    from chatlas import ChatGoogle
    from dotenv import load_dotenv

    load_dotenv()
    chat = ChatGoogle()
    chat.console()
    ```

    Another, more general, solution is to load your environment variables into the shell
    before starting Python (maybe in a `.bashrc`, `.zshrc`, etc. file):

    ```shell
    export GOOGLE_API_KEY=...
    ```
    """

    if model is None:
        model = log_model_default("gemini-1.5-flash")

    turns = normalize_turns(
        turns or [],
        system_prompt=system_prompt,
    )

    return Chat(
        provider=GoogleProvider(
            turns=turns,
            model=model,
            api_key=api_key,
            kwargs=kwargs,
        ),
        turns=turns,
    )


# The dictionary form of ChatCompletion (TODO: stronger typing)?
GenerateContentDict = dict[str, Any]


class GoogleProvider(
    Provider[GenerateContentResponse, GenerateContentResponse, GenerateContentDict]
):
    def __init__(
        self,
        *,
        turns: list[Turn],
        model: str,
        api_key: str | None,
        kwargs: Optional["ChatClientArgs"],
    ):
        try:
            from google.generativeai import GenerativeModel
        except ImportError:
            raise ImportError(
                f"The {self.__class__.__name__} class requires the `google-generativeai` package. "
                "Install it with `pip install google-generativeai`."
            )

        if api_key is not None:
            import google.generativeai as genai

            genai.configure(api_key=api_key)

        system_prompt = None
        if len(turns) > 0 and turns[0].role == "system":
            system_prompt = turns[0].text

        kwargs_full: "ChatClientArgs" = {
            "model_name": model,
            "system_instruction": system_prompt,
            **(kwargs or {}),
        }

        self._client = GenerativeModel(**kwargs_full)

    @overload
    def chat_perform(
        self,
        *,
        stream: Literal[False],
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]] = None,
        kwargs: Optional["SubmitInputArgs"] = None,
    ): ...

    @overload
    def chat_perform(
        self,
        *,
        stream: Literal[True],
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]] = None,
        kwargs: Optional["SubmitInputArgs"] = None,
    ): ...

    def chat_perform(
        self,
        stream: bool,
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]] = None,
        kwargs: Optional["SubmitInputArgs"] = None,
    ):
        kwargs = self._chat_perform_args(stream, turns, tools, data_model, kwargs)
        return self._client.generate_content(**kwargs)

    @overload
    async def chat_perform_async(
        self,
        *,
        stream: Literal[False],
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]] = None,
        kwargs: Optional["SubmitInputArgs"] = None,
    ): ...

    @overload
    async def chat_perform_async(
        self,
        *,
        stream: Literal[True],
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]] = None,
        kwargs: Optional["SubmitInputArgs"] = None,
    ): ...

    async def chat_perform_async(
        self,
        stream: bool,
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]] = None,
        kwargs: Optional["SubmitInputArgs"] = None,
    ):
        kwargs = self._chat_perform_args(stream, turns, tools, data_model, kwargs)
        return await self._client.generate_content_async(**kwargs)

    def _chat_perform_args(
        self,
        stream: bool,
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]] = None,
        kwargs: Optional["SubmitInputArgs"] = None,
    ) -> "SubmitInputArgs":
        kwargs_full: "SubmitInputArgs" = {
            "contents": self._google_contents(turns),
            "stream": stream,
            "tools": self._gemini_tools(list(tools.values())) if tools else None,
            **(kwargs or {}),
        }

        if data_model:
            config = kwargs_full.get("generation_config", {})
            params = basemodel_to_param_schema(data_model)

            if "additionalProperties" in params:
                del params["additionalProperties"]

            mime_type = "application/json"
            if isinstance(config, dict):
                config["response_schema"] = params
                config["response_mime_type"] = mime_type
            elif isinstance(config, GenerationConfig):
                config.response_schema = params
                config.response_mime_type = mime_type

            kwargs_full["generation_config"] = config

        return kwargs_full

    def stream_text(self, chunk) -> Optional[str]:
        if chunk.parts:
            return chunk.text
        return None

    def stream_merge_chunks(self, completion, chunk):
        # The .resolve() in .stream_turn() does the merging for us
        return {}

    def stream_turn(
        self, completion, has_data_model, stream: GenerateContentResponse
    ) -> Turn:
        stream.resolve()
        return self._as_turn(
            stream,
            has_data_model,
        )

    async def stream_turn_async(
        self, completion, has_data_model, stream: AsyncGenerateContentResponse
    ) -> Turn:
        await stream.resolve()
        return self._as_turn(
            stream,
            has_data_model,
        )

    def value_turn(self, completion, has_data_model) -> Turn:
        return self._as_turn(completion, has_data_model)

    def token_count(
        self,
        *args: Content | str,
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
    ):
        kwargs = self._token_count_args(
            *args,
            tools=tools,
            data_model=data_model,
        )

        res = self._client.count_tokens(**kwargs)
        return res.total_tokens

    async def token_count_async(
        self,
        *args: Content | str,
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
    ):
        kwargs = self._token_count_args(
            *args,
            tools=tools,
            data_model=data_model,
        )

        res = await self._client.count_tokens_async(**kwargs)
        return res.total_tokens

    def _token_count_args(
        self,
        *args: Content | str,
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
    ) -> dict[str, Any]:
        turn = user_turn(*args)

        kwargs = self._chat_perform_args(
            stream=False,
            turns=[turn],
            tools=tools,
            data_model=data_model,
        )

        args_to_keep = ["contents", "tools"]

        return {arg: kwargs[arg] for arg in args_to_keep if arg in kwargs}

    def _google_contents(self, turns: list[Turn]) -> list["ContentDict"]:
        contents: list["ContentDict"] = []
        for turn in turns:
            if turn.role == "system":
                continue  # System messages are handled separately
            elif turn.role == "user":
                parts = [self._as_part_type(c) for c in turn.contents]
                contents.append({"role": turn.role, "parts": parts})
            elif turn.role == "assistant":
                parts = [self._as_part_type(c) for c in turn.contents]
                contents.append({"role": "model", "parts": parts})
            else:
                raise ValueError(f"Unknown role {turn.role}")
        return contents

    def _as_part_type(self, content: Content) -> "PartType":
        from google.generativeai.types.content_types import protos

        if isinstance(content, ContentText):
            return protos.Part(text=content.text)
        elif isinstance(content, ContentJson):
            return protos.Part(text="<structured data/>")
        elif isinstance(content, ContentImageInline):
            return protos.Part(
                inline_data={
                    "mime_type": content.content_type,
                    "data": content.data,
                }
            )
        elif isinstance(content, ContentImageRemote):
            raise NotImplementedError(
                "Remote images aren't supported by Google (Gemini). "
                "Consider downloading the image and using content_image_file() instead."
            )
        elif isinstance(content, ContentToolRequest):
            return protos.Part(
                function_call={
                    "name": content.id,
                    "args": content.arguments,
                }
            )
        elif isinstance(content, ContentToolResult):
            return protos.Part(
                function_response={
                    "name": content.id,
                    "response": {"value": content.get_final_value()},
                }
            )
        raise ValueError(f"Unknown content type: {type(content)}")

    def _as_turn(
        self,
        message: "GenerateContentResponse | AsyncGenerateContentResponse",
        has_data_model: bool,
    ) -> Turn:
        contents = []

        msg = message.candidates[0].content

        for part in msg.parts:
            if part.text:
                if has_data_model:
                    contents.append(ContentJson(json.loads(part.text)))
                else:
                    contents.append(ContentText(part.text))
            if part.function_call:
                func = part.function_call
                contents.append(
                    ContentToolRequest(
                        func.name,
                        name=func.name,
                        arguments=dict(func.args),
                    )
                )
            if part.function_response:
                func = part.function_response
                contents.append(
                    ContentToolResult(
                        func.name,
                        value=func.response,
                    )
                )

        usage = message.usage_metadata
        tokens = (
            usage.prompt_token_count,
            usage.candidates_token_count,
        )

        tokens_log(self, tokens)

        finish = message.candidates[0].finish_reason

        return Turn(
            "assistant",
            contents,
            tokens=tokens,
            finish_reason=finish.name,
            completion=message,
        )

    def _gemini_tools(self, tools: list[Tool]) -> list["FunctionDeclaration"]:
        from google.generativeai.types.content_types import FunctionDeclaration

        res: list["FunctionDeclaration"] = []
        for tool in tools:
            fn = tool.schema["function"]
            params = None
            if "parameters" in fn and fn["parameters"]["properties"]:
                params = {
                    "type": "object",
                    "properties": fn["parameters"]["properties"],
                    "required": fn["parameters"]["required"],
                }

            res.append(
                FunctionDeclaration(
                    name=fn["name"],
                    description=fn.get("description", ""),
                    parameters=params,
                )
            )

        return res
