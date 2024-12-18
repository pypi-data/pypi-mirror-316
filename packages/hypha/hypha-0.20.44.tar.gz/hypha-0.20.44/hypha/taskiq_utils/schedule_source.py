"""This file contains modules from the taskiq-redis package
We need to patch it so we can use fakeredis when redis is not available.
The library was created by Pavel Kirilin, released under the MIT license.
"""
from fakeredis import aioredis
from typing import List, Optional

from taskiq import ScheduleSource
from taskiq.abc.serializer import TaskiqSerializer
from taskiq.compat import model_dump, model_validate
from taskiq.scheduler.scheduled_task import ScheduledTask
from taskiq.serializers import PickleSerializer


class RedisScheduleSource(ScheduleSource):
    """
    Source of schedules for redis.

    This class allows you to store schedules in redis.
    Also it supports dynamic schedules.

    :param url: url to redis.
    :param prefix: prefix for redis schedule keys.
    :param buffer_size: buffer size for redis scan.
        This is how many keys will be fetched at once.
    :param max_connection_pool_size: maximum number of connections in pool.
    :param serializer: serializer for data.
    :param connection_kwargs: additional arguments for redis BlockingConnectionPool.
    """

    def __init__(
        self,
        redis: aioredis.FakeRedis,
        prefix: str = "schedule",
        buffer_size: int = 50,
        serializer: Optional[TaskiqSerializer] = None,
    ) -> None:
        self.prefix = prefix
        self.redis = redis
        self.buffer_size = buffer_size
        if serializer is None:
            serializer = PickleSerializer()
        self.serializer = serializer

    async def delete_schedule(self, schedule_id: str) -> None:
        """Remove schedule by id."""
        await self.redis.delete(f"{self.prefix}:{schedule_id}")

    async def add_schedule(self, schedule: ScheduledTask) -> None:
        """
        Add schedule to redis.

        :param schedule: schedule to add.
        :param schedule_id: schedule id.
        """
        await self.redis.set(
            f"{self.prefix}:{schedule.schedule_id}",
            self.serializer.dumpb(model_dump(schedule)),
        )

    async def get_schedules(self) -> List[ScheduledTask]:
        """
        Get all schedules from redis.

        This method is used by scheduler to get all schedules.

        :return: list of schedules.
        """
        schedules = []

        buffer = []
        async for key in self.redis.scan_iter(f"{self.prefix}:*"):
            buffer.append(key)
            if len(buffer) >= self.buffer_size:
                schedules.extend(await self.redis.mget(buffer))
                buffer = []
        if buffer:
            schedules.extend(await self.redis.mget(buffer))
        return [
            model_validate(ScheduledTask, self.serializer.loadb(schedule))
            for schedule in schedules
            if schedule
        ]

    async def post_send(self, task: ScheduledTask) -> None:
        """Delete a task after it's completed."""
        if task.time is not None:
            await self.delete_schedule(task.schedule_id)

    async def shutdown(self) -> None:
        """Shut down the schedule source."""
        pass
