# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types.beta import (
    BetaMessage,
    BetaMessageTokensCount,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMessages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: Anthropic) -> None:
        message = client.beta.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
        )
        assert_matches_type(BetaMessage, message, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Anthropic) -> None:
        message = client.beta.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string"],
            stream=False,
            system=[
                {
                    "text": "Today's date is 2024-06-01.",
                    "type": "text",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            temperature=1,
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tools=[
                {
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                    "name": "x",
                    "cache_control": {"type": "ephemeral"},
                    "description": "Get the current weather in a given location",
                    "type": "custom",
                }
            ],
            top_k=5,
            top_p=0.7,
            betas=["string"],
        )
        assert_matches_type(BetaMessage, message, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: Anthropic) -> None:
        response = client.beta.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(BetaMessage, message, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: Anthropic) -> None:
        with client.beta.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(BetaMessage, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_2(self, client: Anthropic) -> None:
        message_stream = client.beta.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            stream=True,
        )
        message_stream.response.close()

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Anthropic) -> None:
        message_stream = client.beta.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            stream=True,
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string"],
            system=[
                {
                    "text": "Today's date is 2024-06-01.",
                    "type": "text",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            temperature=1,
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tools=[
                {
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                    "name": "x",
                    "cache_control": {"type": "ephemeral"},
                    "description": "Get the current weather in a given location",
                    "type": "custom",
                }
            ],
            top_k=5,
            top_p=0.7,
            betas=["string"],
        )
        message_stream.response.close()

    @parametrize
    def test_raw_response_create_overload_2(self, client: Anthropic) -> None:
        response = client.beta.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_create_overload_2(self, client: Anthropic) -> None:
        with client.beta.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_count_tokens(self, client: Anthropic) -> None:
        message = client.beta.messages.count_tokens(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="string",
        )
        assert_matches_type(BetaMessageTokensCount, message, path=["response"])

    @parametrize
    def test_method_count_tokens_with_all_params(self, client: Anthropic) -> None:
        message = client.beta.messages.count_tokens(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="string",
            system=[
                {
                    "text": "Today's date is 2024-06-01.",
                    "type": "text",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tools=[
                {
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                    "name": "x",
                    "cache_control": {"type": "ephemeral"},
                    "description": "Get the current weather in a given location",
                    "type": "custom",
                }
            ],
            betas=["string"],
        )
        assert_matches_type(BetaMessageTokensCount, message, path=["response"])

    @parametrize
    def test_raw_response_count_tokens(self, client: Anthropic) -> None:
        response = client.beta.messages.with_raw_response.count_tokens(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(BetaMessageTokensCount, message, path=["response"])

    @parametrize
    def test_streaming_response_count_tokens(self, client: Anthropic) -> None:
        with client.beta.messages.with_streaming_response.count_tokens(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = response.parse()
            assert_matches_type(BetaMessageTokensCount, message, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMessages:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        message = await async_client.beta.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
        )
        assert_matches_type(BetaMessage, message, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncAnthropic) -> None:
        message = await async_client.beta.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string"],
            stream=False,
            system=[
                {
                    "text": "Today's date is 2024-06-01.",
                    "type": "text",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            temperature=1,
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tools=[
                {
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                    "name": "x",
                    "cache_control": {"type": "ephemeral"},
                    "description": "Get the current weather in a given location",
                    "type": "custom",
                }
            ],
            top_k=5,
            top_p=0.7,
            betas=["string"],
        )
        assert_matches_type(BetaMessage, message, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(BetaMessage, message, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(BetaMessage, message, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        message_stream = await async_client.beta.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            stream=True,
        )
        await message_stream.response.aclose()

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncAnthropic) -> None:
        message_stream = await async_client.beta.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            stream=True,
            metadata={"user_id": "13803d75-b4b5-4c3e-b2a2-6f21399b021b"},
            stop_sequences=["string"],
            system=[
                {
                    "text": "Today's date is 2024-06-01.",
                    "type": "text",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            temperature=1,
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tools=[
                {
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                    "name": "x",
                    "cache_control": {"type": "ephemeral"},
                    "description": "Get the current weather in a given location",
                    "type": "custom",
                }
            ],
            top_k=5,
            top_p=0.7,
            betas=["string"],
        )
        await message_stream.response.aclose()

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[
                {
                    "content": "Hello, world",
                    "role": "user",
                }
            ],
            model="claude-3-5-sonnet-20241022",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_count_tokens(self, async_client: AsyncAnthropic) -> None:
        message = await async_client.beta.messages.count_tokens(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="string",
        )
        assert_matches_type(BetaMessageTokensCount, message, path=["response"])

    @parametrize
    async def test_method_count_tokens_with_all_params(self, async_client: AsyncAnthropic) -> None:
        message = await async_client.beta.messages.count_tokens(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="string",
            system=[
                {
                    "text": "Today's date is 2024-06-01.",
                    "type": "text",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tools=[
                {
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "description": "The city and state, e.g. San Francisco, CA",
                                "type": "string",
                            },
                            "unit": {
                                "description": "Unit for the output - one of (celsius, fahrenheit)",
                                "type": "string",
                            },
                        },
                    },
                    "name": "x",
                    "cache_control": {"type": "ephemeral"},
                    "description": "Get the current weather in a given location",
                    "type": "custom",
                }
            ],
            betas=["string"],
        )
        assert_matches_type(BetaMessageTokensCount, message, path=["response"])

    @parametrize
    async def test_raw_response_count_tokens(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.messages.with_raw_response.count_tokens(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        message = response.parse()
        assert_matches_type(BetaMessageTokensCount, message, path=["response"])

    @parametrize
    async def test_streaming_response_count_tokens(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.messages.with_streaming_response.count_tokens(
            messages=[
                {
                    "content": "string",
                    "role": "user",
                }
            ],
            model="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            message = await response.parse()
            assert_matches_type(BetaMessageTokensCount, message, path=["response"])

        assert cast(Any, response.is_closed) is True
