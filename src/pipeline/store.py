import sqlite3
from pathlib import Path

from .settings import RunSummary
from .fake_llm import Answer


def init_db(db_path: str | Path = "results.db") -> None:
    conn = sqlite3.connect(db_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            started_at REAL NOT NULL,
            elapsed_seconds REAL NOT NULL,
            n_questions INTEGER NOT NULL,
            n_succeeded INTEGER NOT NULL,
            n_retries_total INTEGER NOT NULL,
            total_cost_usd REAL NOT NULL,
            fail_rate REAL NOT NULL,
            use_fake INTEGER NOT NULL
        )
    """)

    conn.execute("""
       CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            retries INTEGER NOT NULL,
            cost_usd REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def save_run(
    summary: RunSummary,
    answers: list[Answer],
    db_path: str | Path = "results.db",
) -> None:
    conn = sqlite3.connect(db_path)

    conn.execute(
        """
        INSERT INTO runs (
            run_id,
            started_at,
            elapsed_seconds,
            n_questions,
            n_succeeded,
            n_retries_total,
            total_cost_usd,
            fail_rate,
            use_fake
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            summary.run_id,
            summary.started_at,
            summary.elapsed_seconds,
            summary.n_questions,
            summary.n_succeeded,
            summary.n_retries_total,
            summary.total_cost_usd,
            summary.fail_rate,
            int(summary.use_fake),
        ),
    )

    for a in answers:
        conn.execute(
            """
            INSERT INTO answers (
                run_id,
                question,
                answer,
                retries,
                cost_usd
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                summary.run_id,
                a.question,
                a.text,
                a.retries,
                a.cost_usd,
            ),
        )

    conn.commit()
    conn.close()

def load_run(
    run_id: str,
    db_path: str | Path = "results.db",
    ):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    run = conn.execute(
        "SELECT * FROM runs WHERE run_id = ?",
        (run_id,),
    ).fetchone()

    answers = conn.execute(
        "SELECT * FROM answers WHERE run_id = ?",
            (run_id,),
    ).fetchall()

    conn.close()

    return run, answers