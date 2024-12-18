from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from redis.exceptions import TimeoutError

from typica.connection import RedisConnectionMeta


class RedisConnector:

    _meta: RedisConnectionMeta
    _client: Redis

    def __init__(self, meta: RedisConnectionMeta) -> None:
        self._meta = meta

    def __enter__(self):
        self.connect()
        if self._client is None:
            raise ValueError("Redis not connected.")
        return self

    def __call__(self, *args, **kwds) -> bool:
        if self._client is None:
            raise ValueError("Redis not connected.")
        return True

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def connect(self, other_database: int | None = None) -> None:
        try:

            self._client = Redis(
                host=str(self._meta.host),
                port=int(self._meta.port),  # type: ignore
                username=self._meta.username,
                password=self._meta.password,
                db=other_database if other_database else self._meta.database,
            )

        except TimeoutError:
            raise ValueError("Redis connection timed out.")
        except Exception as e:
            raise e

    def close(self) -> None:
        if hasattr(self, "_client") and self._client:
            self._client.close()


class AsyncRedisConnector:

    _meta: RedisConnectionMeta
    _client: AsyncRedis

    def __init__(self, meta: RedisConnectionMeta) -> None:
        self._meta = meta

    async def __enter__(self):
        await self.connect()
        if self._client is None:
            raise ValueError("Redis not connected.")
        return self

    async def __call__(self, *args, **kwds) -> bool:
        if self._client is None:
            raise ValueError("Redis not connected.")
        return True

    async def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def connect(self, other_database: int | None = None) -> None:
        try:

            self._client = AsyncRedis(
                host=str(self._meta.host),
                port=int(self._meta.port),  # type: ignore
                username=self._meta.username,
                password=self._meta.password,
                db=other_database if other_database else self._meta.database,
            )
        except TimeoutError:
            raise ValueError("Redis connection timed out.")
        except Exception as e:
            raise e

    async def close(self) -> None:
        """
        Close the connection to the Redis server.

        This method is a no-op if the connection is already closed.
        """
        if hasattr(self, "_client") and self._client:
            await self._client.close()
