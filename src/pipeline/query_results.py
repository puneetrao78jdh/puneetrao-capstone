import argparse
import sqlite3


def show_summary(db_path: str):
    conn = sqlite3.connect(db_path)

    rows = conn.execute("""
        SELECT
            run_id,
            n_questions,
            n_succeeded,
            n_retries_total,
            total_cost_usd,
            elapsed_seconds
        FROM runs
        ORDER BY started_at DESC
    """).fetchall()

    conn.close()

    for row in rows:
        print(row)


def show_slowest(db_path: str, limit: int):
    conn = sqlite3.connect(db_path)

    rows = conn.execute("""
        SELECT
            question,
            retries,
            cost_usd
        FROM answers
        ORDER BY cost_usd DESC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    for row in rows:
        print(row)


def show_most_retried(db_path: str, limit: int):
    conn = sqlite3.connect(db_path)

    rows = conn.execute("""
        SELECT
            question,
            retries,
            cost_usd
        FROM answers
        ORDER BY retries DESC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    for row in rows:
        print(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--db", default="results.db")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--slowest", type=int)
    parser.add_argument("--most-retried", type=int)

    args = parser.parse_args()

    if args.summary:
        show_summary(args.db)

    if args.slowest:
        show_slowest(args.db, args.slowest)

    if args.most_retried:
        show_most_retried(args.db, args.most_retried)