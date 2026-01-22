import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from api.db import Base

from api.models import task as _task_models  # noqa: F401


def _get_sync_db_url() -> str:
    db_user = os.environ.get("DB_USER", "root")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_host = os.environ.get("DB_HOST", "db")
    db_port = os.environ.get("DB_PORT", "3306")
    return (
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/demo?charset=utf8"
    )


def migrate_db(engine: Engine) -> None:
    """テーブルが存在する場合は非破壊で差分を反映する。

    - 未作成テーブルは `create_all` で作成
    - 既存テーブルには「不足カラムの追加」のみ行う

    NOTE: 既存カラムの型変更や削除はこのスクリプトでは扱わない。
    """

    target_table_names = set(Base.metadata.tables.keys())
    if not target_table_names:
        raise RuntimeError(
            "モデルが読み込まれておらず、マイグレーション対象テーブルが空です。"
            "例えば `api.models.task` をインポートしてからこのスクリプトを実行してください。"
        )

    with engine.begin() as conn:
        inspector = inspect(conn)
        existing_tables_before = set(inspector.get_table_names())
        any_target_table_exists = bool(existing_tables_before & target_table_names)

        # テーブルが無い/不足している場合は作る（既存は壊さない）
        Base.metadata.create_all(bind=conn)

        # 既存テーブルが1つも無い＝初回作成なので、差分ALTERは不要
        if not any_target_table_exists:
            return

        # 既に存在していたテーブルだけを対象に、不足カラムを追加
        inspector = inspect(conn)
        preparer = engine.dialect.identifier_preparer
        for table in Base.metadata.sorted_tables:
            if table.name not in existing_tables_before:
                continue

            existing_columns = {c["name"] for c in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name in existing_columns:
                    continue

                if column.primary_key:
                    raise RuntimeError(
                        "既存テーブルに主キー列を追加するマイグレーションは未対応です: "
                        f"{table.name}.{column.name}"
                    )

                if (not column.nullable) and column.server_default is None:
                    raise RuntimeError(
                        "NOT NULL列を既存テーブルへ追加するには server_default が必要です: "
                        f"{table.name}.{column.name}"
                    )

                column_type_sql = column.type.compile(dialect=engine.dialect)
                quoted_table = preparer.quote(table.name)
                quoted_column = preparer.quote(column.name)

                nullable_sql = "NULL" if column.nullable else "NOT NULL"
                default_sql = ""
                if column.server_default is not None:
                    # SQLAlchemyのDefaultClauseをそのままコンパイルする
                    compiled_default = str(
                        column.server_default.compile(dialect=engine.dialect)
                    )
                    default_sql = f" {compiled_default}"

                sql = (
                    f"ALTER TABLE {quoted_table} "
                    f"ADD COLUMN {quoted_column} {column_type_sql}"
                    f" {nullable_sql}{default_sql}"
                )
                conn.execute(text(sql))


def main() -> None:
    engine = create_engine(_get_sync_db_url(), echo=True)
    migrate_db(engine)


if __name__ == "__main__":
    main()
