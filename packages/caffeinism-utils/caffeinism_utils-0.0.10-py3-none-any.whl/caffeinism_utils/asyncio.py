import asyncio
import collections
import contextlib
import logging
from functools import partial

logger = logging.getLogger(__name__)


def run_in_threadpool(func, *args, **kwargs):
    return run_in_executor(None, func, *args, **kwargs)


def run_in_executor(pool, func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    func = partial(func, *args, **kwargs)
    return loop.run_in_executor(pool, func)


class LastManStanding:
    class __Defeat(Exception):
        pass

    def __init__(self):
        self.__locks = collections.defaultdict(asyncio.Lock)
        self.__counter = collections.defaultdict(int)

    @contextlib.asynccontextmanager
    async def join(self, key):
        try:
            yield self.__wait(key)
        except LastManStanding.__Defeat:
            logger.info(f"{key} skipped")

    @contextlib.asynccontextmanager
    async def __wait(self, key):
        self.__counter[key] += 1
        async with self.__locks[key]:
            self.__counter[key] -= 1
            if self.__counter[key]:
                raise LastManStanding.__Defeat
            else:
                yield
