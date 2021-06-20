import asyncio
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Protocol, Union

import httpx


@dataclass
class PypiProject:
    name: str
    version: str
    summary: Optional[str]
    homepage: Optional[str]
    documentation: Optional[str]
    release_notes: Optional[str]
    author: Optional[str]

    @classmethod
    def from_response(clazz: "PypiProject", data: Dict) -> "PypiProject":
        info = data["info"]
        urls = info.get("project_urls") or {}
        return clazz(
            name=info["name"],
            version=info["version"],
            summary=info.get("summary"),
            homepage=urls.get("Homepage"),
            documentation=urls.get("Documentation"),
            release_notes=urls.get("Release notes"),
            author=info.get("author"),
        )


@dataclass
class PypiError:
    name: str
    exc: Exception


PypiReturn = Union[PypiProject, PypiError]


class ProtoWarehouse(Protocol):
    async def query_project(self, name: str) -> PypiReturn:
        ...

    async def query_projects(self, names: Iterable[str]) -> List[PypiReturn]:
        ...


class PypiRepo:
    def __init__(self, base_url: str = "https://pypi.org/pypi/"):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def query_project(self, name: str) -> PypiReturn:
        try:
            res = await client.get(f"{name}/json")
        except Exception as exc:
            return PypiError(name, exc)
        return PypiProject.from_response(res.json())

    async def query_projects(self, names: Iterable[str]) -> List[PypiReturn]:
        return await asyncio.gather(
            *[self.query_project(name) for name in names], return_exceptions=True
        )
