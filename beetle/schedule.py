from typing import Dict, List

import os
import logging
import asyncio
import traceback

from beetle.models import Task
from beetle.constants import TaskStatus
from beetle.sdk import OpenListClient, PathEntry
from beetle.settings import (
    OPENLIST_HOST,
    OPENLIST_TOKEN,
    SYNCHRONIZER_COUNT,
    TASK_POLL_INTERVAL,
)


log = logging.getLogger(__name__)
semaphore = asyncio.Semaphore(SYNCHRONIZER_COUNT)


class TaskScheduler:
    def __init__(self):
        self.lock = asyncio.Lock()
        self._stop = asyncio.Event()
        self.watch_tasks: Dict[int, Watcher] = {}

    async def _run(self):
        async with asyncio.TaskGroup() as tg:
            while not self._stop.is_set():
                async with self.lock:
                    async for task in Task.all():
                        if task.id in self.watch_tasks:
                            watcher = self.watch_tasks[task.id]
                            watcher.task = task
                        elif task.status == TaskStatus.running:
                            watcher = Watcher(self.lock, task, self.watch_tasks)
                            self.watch_tasks[task.id] = watcher
                            tg.create_task(watcher.run())

                await asyncio.sleep(TASK_POLL_INTERVAL)

            self._stop_tasks()

    def _stop_tasks(self):
        for _, watcher in self.watch_tasks.items():
            watcher.stop()

        for _, synchronizer in self.sync_tasks.items():
            synchronizer.stop()
            self.sync_tasks.pop(synchronizer.id)

        log.info("Stopped all tasks")

    def stop(self):
        self._stop.set()

    def run(self):
        asyncio.run(self._run())


class Watcher:
    def __init__(
        self,
        lock: asyncio.Lock,
        task: Task,
        watch_tasks: Dict[int, "Watcher"],
    ):
        self.lock = lock
        self.task = task
        self._stop = asyncio.Event()
        self.watch_tasks = watch_tasks
        self.client = OpenListClient(OPENLIST_HOST, OPENLIST_TOKEN)

    def stop(self):
        self._stop.set()

    async def _get_files(self, path: str) -> List[PathEntry]:
        files = []
        dirs = [path]
        replace_path = None
        while dirs:
            response = await self.client.list(dirs.pop())
            for entry in response.content:
                if entry.is_dir:
                    dirs.append(entry.path)
                else:
                    files.append(entry)

            if replace_path is None and len(files) > 0:
                entry = files[-1]
                replace_path = entry.path.removesuffix(entry.name)

        for file in files:
            file.path = file.path.replace(replace_path, path)

        return files

    async def _diff(self) -> List[PathEntry]:
        src_files = await self._get_files(self.task.src)
        dst_files = await self._get_files(self.task.dst)
        map = {file.path.removeprefix(self.task.dst): file for file in dst_files}
        sync_files = []
        for file in src_files:
            path = file.path.removeprefix(self.task.src)
            if path not in map or map[path].size != file.size:
                sync_files.append(file)
        return sync_files

    async def sync(self, file: PathEntry):
        dir, filename = os.path.split(file.path)
        upload_path = os.path.join(self.task.dst, filename)
        aiter = self.client.download(file.sign, file.path)
        async with semaphore:
            result = await self.client.upload(upload_path, aiter, overwrite=True)
        if result and self.task.cleanup:
            await self.client.remove(dir, names=[filename])
        log.info(f"Sync {file.name} Over")

    async def run(self):
        while not self._stop.is_set() and self.task.status == TaskStatus.running:
            try:
                for file in await self._diff():
                    await self.sync(file)
            except Exception:
                log.error(traceback.format_exc())
            finally:
                await asyncio.sleep(self.task.interval)

        async with self.lock:
            if self.task.id in self.watch_tasks:
                self.watch_tasks.pop(self.task.id)

        await self.client.aclose()
