import os
import asyncio
from threading import Thread
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.shared.utils.logger import logging as logger
from src.shared.database import Base
from src.shared.domain import LLMRepository, MetricRepository, BenchmarkRepository
from src.randomiser_service.database.seed import seed_data
from src.shared.database.session import engine, get_db
from src.randomiser_service.handlers.services.benchmark import BenchmarkService
from src.randomiser_service.config import config

load_dotenv()
SCHEDULE_INTERVAL = int(os.getenv("SCHEDULE_INTERVAL", "3"))
scheduler = AsyncIOScheduler()
main_loop = asyncio.get_event_loop()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    await seed_data(db)
    logger.info('📦  Models seeded!');

    llm_repo = LLMRepository(db)
    metric_repo = MetricRepository(db)
    benchmark_repo = BenchmarkRepository(db)
    benchmark_service = BenchmarkService(benchmark_repo, llm_repo, metric_repo)

    async def run_simulator():
        """Run the simulator/randomiser and retry upon failure"""
        await benchmark_service.initiate_simulation()

    def simulate_benchmarks():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        def schedule_task():
            asyncio.run_coroutine_threadsafe(run_simulator(), main_loop)

        scheduler.add_job(schedule_task, "interval", minutes=int(SCHEDULE_INTERVAL))
        scheduler.start()
        loop.run_forever()

    asyncio.create_task(run_simulator())

    simulator_thread = Thread(target=simulate_benchmarks)
    simulator_thread.start()

    yield

    scheduler.shutdown()
    simulator_thread.join(timeout=10)
    if simulator_thread.is_alive():
        logger.warning("Warning: Benchmark simulator thread running!")
    logger.info("Scheduler shutdown complete")

def start_worker() -> FastAPI:
    worker = FastAPI(
        title=config.APP_NAME,
        version=config.APP_VERSION,
        lifespan=lifespan,
    )

    Base.metadata.create_all(bind=engine)

    logger.info(f"🚀 {config.APP_NAME} running in {config.APP_ENV}. Listening on {config.PORT}")

    return worker

app = start_worker()
