import asyncio
from typing import Any, Awaitable, Optional, Self, TypeAlias, cast

import pymongo.results  # type: ignore[import-untyped]
from pydantic_mongo_document.document.base import DocumentBase
from pydantic_mongo_document.types import (
    AsyncPyMongoClient,
    AsyncPyMongoCollection,
    AsyncPyMongoDatabase,
)


_ASYNC_CLIENTS: dict[str, AsyncPyMongoClient] = {}


CountReturnType: TypeAlias = Awaitable[int]
DeleteReturnType: TypeAlias = Awaitable[pymongo.results.DeleteResult]
CommitReturnType: TypeAlias = Awaitable[pymongo.results.UpdateResult | None]


class Document(
    DocumentBase[
        AsyncPyMongoClient,
        AsyncPyMongoDatabase,
        AsyncPyMongoCollection,
        CountReturnType,
        DeleteReturnType,
        CommitReturnType,
    ],
):
    """Async document model."""

    @classmethod
    def client(cls) -> AsyncPyMongoClient:
        if cls.__replica__ not in _ASYNC_CLIENTS:
            _ASYNC_CLIENTS[cls.__replica__] = AsyncPyMongoClient(
                host=str(cls.get_replica_config().uri),
                **cls.get_replica_config().client_options,
            )

        return _ASYNC_CLIENTS[cls.__replica__]

    @classmethod
    async def create_indexes(cls) -> None:
        """Creates indexes for collection."""

    async def noop(self) -> None:
        """No operation. Does nothing."""

    @classmethod
    async def one(
        cls,
        /,
        document_id: str | None = None,
        add_query: dict[str, Any] | None = None,
        required: bool = True,
        **kwargs: Any,
    ) -> Optional[Self]:
        result = await cast(
            Awaitable[Optional[dict[str, Any]]],
            cls._inner_one(document_id, add_query, **kwargs),
        )

        if result is not None:
            return cls.model_validate(result)
        if required:
            raise cls.NotFoundError()

        return None

    async def insert(self) -> Self:
        """Insert document into collection."""

        result = await self.collection().insert_one(
            self.encoder.encode_dict(
                self.model_dump(by_alias=True, exclude_none=True),
                reveal_secrets=True,
            )
        )

        if getattr(self, self.__primary_key__, None) is None:
            setattr(self, self.__primary_key__, result.inserted_id)

        return self
