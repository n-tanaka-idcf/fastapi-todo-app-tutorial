from api.migrate_db import migrate_db
from sqlalchemy import create_engine, inspect, text


def test_migrate_db_creates_tables_when_empty():
    engine = create_engine("sqlite:///:memory:")
    migrate_db(engine)

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    assert {"tasks", "dones"}.issubset(tables)


def test_migrate_db_adds_missing_column_without_dropping_data():
    engine = create_engine("sqlite:///:memory:")

    # 既存DBに tasks テーブルがある（ただし due_date 列が無い）状態を作る
    with engine.begin() as conn:
        conn.execute(
            text("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title VARCHAR(1024))")
        )
        conn.execute(text("INSERT INTO tasks (id, title) VALUES (1, 'keep')"))

    migrate_db(engine)

    inspector = inspect(engine)
    columns = {c["name"] for c in inspector.get_columns("tasks")}
    assert "due_date" in columns

    with engine.begin() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM tasks")).scalar_one()
    assert count == 1
