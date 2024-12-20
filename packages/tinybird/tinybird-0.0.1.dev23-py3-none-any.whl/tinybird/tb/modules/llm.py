import asyncio
import json
import urllib.parse
from copy import deepcopy
from typing import Awaitable, Callable, List, Optional

from openai import OpenAI
from pydantic import BaseModel

from tinybird.client import TinyB


class DataFile(BaseModel):
    name: str
    content: str


class DataProject(BaseModel):
    datasources: List[DataFile]
    pipes: List[DataFile]


class TestExpectation(BaseModel):
    name: str
    description: str
    parameters: str


class TestExpectations(BaseModel):
    tests: List[TestExpectation]


class LLM:
    def __init__(self, user_token: str, client: TinyB, api_key: Optional[str] = None):
        self.user_client = deepcopy(client)
        self.user_client.token = user_token

        self.openai = OpenAI(api_key=api_key) if api_key else None

    async def _execute(self, action_fn: Callable[[], Awaitable[str]], checker_fn: Callable[[str], bool]):
        is_valid = False
        times = 0

        while not is_valid and times < 5:
            result = await action_fn()
            if asyncio.iscoroutinefunction(checker_fn):
                is_valid = await checker_fn(result)
            else:
                is_valid = checker_fn(result)
            times += 1

        return result

    async def create_project(self, prompt: str) -> DataProject:
        try:
            response = await self.user_client._req(
                "/v0/llm/create",
                method="POST",
                data=f'{{"prompt": {json.dumps(prompt)}}}',
                headers={"Content-Type": "application/json"},
            )

            return DataProject.model_validate(response.get("result", {}))
        except Exception:
            return DataProject(datasources=[], pipes=[])

    async def generate_sql_sample_data(self, schema: str, rows: int = 20, prompt: str = "") -> str:
        response = await self.user_client._req(
            "/v0/llm/mock",
            method="POST",
            data=f'{{"schema": "{urllib.parse.quote(schema)}", "rows": {rows}, "context": "{prompt}"}}',
            headers={"Content-Type": "application/json"},
        )
        result = response.get("result", "")
        return result.replace("elementAt", "arrayElement")

    async def create_tests(self, pipe_content: str, pipe_params: set[str], prompt: str = "") -> TestExpectations:
        response = await self.user_client._req(
            "/v0/llm/create/tests",
            method="POST",
            data=json.dumps({"pipe_content": pipe_content, "pipe_params": list(pipe_params), "prompt": prompt}),
            headers={"Content-Type": "application/json"},
        )
        result = response.get("result", "")
        return TestExpectations.model_validate(result)
