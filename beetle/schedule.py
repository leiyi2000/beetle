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
        while not self._stop.is_set():
            async with self.lock:
                task_ids = set()
                async for task in Task.all():
                    if task.id in self.watch_tasks:
                        watcher = self.watch_tasks[task.id]
                        watcher.task = task
                    elif task.status == TaskStatus.running:
                        watcher = Watcher(self.lock, task, self.watch_tasks)
                        self.watch_tasks[task.id] = watcher
                        asyncio.create_task(watcher.run())
                    task_ids.add(task.id)

                for task_id, watcher in self.watch_tasks.items():
                    if task_id not in task_ids:
                        watcher.stop()
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
        while dirs:
            current_dir = dirs.pop()
            response = await self.client.list(current_dir, refresh=True)
            for entry in response.content:
                entry.path = os.path.join(current_dir, entry.name)
                if entry.is_dir:
                    dirs.append(entry.path)
                else:
                    files.append(entry)
        return files

    async def _diff(self, src_path: str, dst_path: str) -> List[PathEntry]:
        src_files = await self._get_files(src_path)
        dst_files = await self._get_files(dst_path)
        map = {file.path.removeprefix(dst_path): file for file in dst_files}
        sync_files = []
        for file in src_files:
            path = file.path.removeprefix(src_path)
            if path not in map or map[path].size != file.size:
                sync_files.append(file)
        return sync_files

    async def clean(self, src_path: str, file: PathEntry):
        src_path = src_path.rstrip("/")
        remove = [os.path.split(file.path)]
        while remove:
            path, name = remove.pop()
            await self.client.remove(path, names=[name])
            response = await self.client.list(path, refresh=True)
            if len(response.content) == 0:
                parent_path, name = os.path.split(path)
                if name and parent_path.startswith(src_path):
                    remove.append((parent_path, name))

    async def sync(
        self,
        src_path: str,
        dst_path: str,
        file: PathEntry,
        cleanup: bool,
    ):
        dir, filename = os.path.split(file.path)
        upload_path = os.path.join(dst_path, file.path.removeprefix(src_path))
        aiter = self.client.download(file.sign, file.path)
        async with semaphore:
            log.info(f"Sync {upload_path} Start")
            result = await self.client.upload(upload_path, aiter, overwrite=True)

        if cleanup and result:
            await self.clean(src_path, file)

        log.info(f"Sync {upload_path} Over")

    async def run(self):
        task_id = self.task.id
        src_path = self.task.src
        dst_path = self.task.dst
        cleanup = self.task.cleanup
        while not self._stop.is_set() and self.task.status == TaskStatus.running:
            try:
                tasks = [
                    self.sync(src_path, dst_path, file, cleanup)
                    for file in await self._diff(src_path, dst_path)
                ]
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception:
                log.error(traceback.format_exc())
            finally:
                await asyncio.sleep(self.task.interval)

        async with self.lock:
            if task_id in self.watch_tasks:
                self.watch_tasks.pop(task_id)

        await self.client.aclose()
