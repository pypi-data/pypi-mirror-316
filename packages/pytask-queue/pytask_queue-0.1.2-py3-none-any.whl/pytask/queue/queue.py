import os
import sqlite3
from datetime import datetime
from typing import Any, Union

from pytask.queue.constants import BASE_SCHEMA, DEFAULT_PATH
from pytask.job.job import Job
from pytask.job.types import JobStatus


class Queue:
    """
    A queue is a collection of jobs that are waiting to be processed. Using the default path,
    the queue will be stored in the current working directory, under ./data/queue.db.

    The queue is stored in a SQLite database, and the table is named "job". Creating more than one object will result in accessing the same queue, unless the path is changed.
    """

    def __init__(self, schema: list[tuple[str, str]] = [], path: str = DEFAULT_PATH):
        self.schema: list[tuple[str, str]] = schema
        self.path: str = path
        self.base_schema: str = BASE_SCHEMA
        self.sql_schema: str = self.__create_sql_schema()
        self.insert_schema: str = self.__create_insert_schema()

        _ = self.__create_table()

    def insert(self, job: Job):
        with sqlite3.connect(self.path) as conn:
            _ = conn.execute(self.insert_schema, job.to_dict())

    def update(
        self,
        job: Job,
    ):
        update_schema = self.__create_update_schema(job.data)

        with sqlite3.connect(self.path) as conn:
            _ = conn.execute(update_schema, job.to_dict())

    def delete(self, task_id: str):
        with sqlite3.connect(self.path) as conn:
            _ = conn.execute("DELETE FROM job WHERE task_id = ?", (task_id,))

        return True

    def get(self, task_id: str) -> Job | None:
        with self.__connect() as conn:
            cursor = conn.execute("SELECT * FROM job WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()

            if row:
                return Job.create_from_row(row)

            return None

    def get_all(self, conditions: dict[str, Any] = {}) -> list[Job]:
        conditions_str = " AND ".join([f"{key} = :{key}" for key in conditions])
        where_clause = f"WHERE {conditions_str}" if conditions_str else ""

        with self.__connect() as conn:
            cursor = conn.execute(
                f"SELECT * FROM job {where_clause}",
                conditions,
            )

            rows = cursor.fetchall()

            return [Job.create_from_row(row) for row in rows]

    def get_oldest_pending(self) -> Job | None:
        with self.__connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM job WHERE status = 'pending' ORDER BY created_at ASC LIMIT 1"
            )
            row = cursor.fetchone()

            if row:
                return Job.create_from_row(row)

            return None

    def __connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def __create_sql_schema(self) -> str:
        schema_parts: list[str] = []

        for column in self.schema:
            column_name, column_type = column
            schema_parts.append(f"{column_name} {column_type}")

        schema = ", ".join(schema_parts)
        job_schema = self.base_schema

        if schema:
            job_schema += f", {schema}"

        return f"""CREATE TABLE IF NOT EXISTS job (       
            {job_schema}
        )"""

    def __create_table(self):
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path))

        try:
            with sqlite3.connect(self.path) as conn:
                _ = conn.execute(self.sql_schema)
        except Exception:
            return False

        return True

    def __create_insert_schema(self) -> str:
        other_columns: list[str] = []

        for column in self.schema:
            column_name, _ = column
            other_columns.append(column_name)

        other_columns_str = ", ".join(other_columns)
        other_columns_values = ", ".join([f":{col}" for col in other_columns])

        return f"""
        INSERT INTO job (task_id, status, created_at, updated_at, {other_columns_str}) 
        VALUES (:task_id, :status, :created_at, :updated_at, {other_columns_values});
        """

    def __create_update_schema(self, extra_columns: dict[str, Any] = {}) -> str:
        extra_columns_str = ", ".join([f"{col} = :{col}" for col in extra_columns])

        return f"""
        UPDATE job SET 
            status = :status, 
            updated_at = :updated_at{f", {extra_columns_str}" if extra_columns_str else ""}
        WHERE task_id = :task_id;
        """
