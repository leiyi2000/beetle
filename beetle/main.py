import logging
import threading

from aerich import Command
from fastapi import FastAPI
from granian import Granian
from granian.constants import Interfaces
from tortoise.contrib.fastapi import register_tortoise

from beetle.api import router
from beetle.schedule import TaskScheduler
from beetle.settings import APP_NAME, TORTOISE_ORM


log = logging.getLogger(__name__)


async def lifespan(app: FastAPI):
    async with Command(
        tortoise_config=TORTOISE_ORM,
        app=APP_NAME,
        location="./migrations",
    ) as command:
        await command.init()
        await command.upgrade(run_in_transaction=True)
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        add_exception_handlers=False,
    )
    log.info("Started scheduler")
    scheduler = TaskScheduler()
    threading.Thread(target=scheduler.run, daemon=True).start()

    yield

    scheduler.stop()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    server = Granian(
        target="beetle:main:app",
        address="0.0.0.0",
        port=8000,
        interface=Interfaces.ASGI,
    )
    server.serve()
