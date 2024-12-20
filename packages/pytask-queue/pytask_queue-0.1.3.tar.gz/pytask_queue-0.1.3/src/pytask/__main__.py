from pytask.queue import Queue
from pytask.job import Job
from pytask.worker import Worker

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def func(job: Job):
    logger.info(f"Processing job: {job.task_id}, {job.data}")
    job.data["foo"] += 1


def main():
    queue = Queue(schema=[("foo", "INTEGER"), ("bar", "TEXT")])
    worker = Worker(queue, func, logger, interval=1)

    queue.insert(Job(data={"foo": 1, "bar": "test"}))
    queue.insert(Job(data={"foo": 2, "bar": "test2"}))
    queue.insert(Job(data={"foo": 3, "bar": "test3"}))

    print("Requested Jobs are: ", queue.get_all(conditions={"foo": 1}))

    worker.run()


if __name__ == "__main__":
    main()
