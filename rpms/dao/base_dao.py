from rpms.util.db_connection import get_connection


class BaseDAO:
    def _generate_next_id(self, table_name, id_column, prefix, start_num):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = f"SELECT {id_column} FROM {table_name} WHERE {id_column} LIKE %s"
            cursor.execute(query, (f"{prefix}%",))
            rows = cursor.fetchall()
            max_num = start_num - 1
            for (existing_id,) in rows:
                suffix = str(existing_id)[len(prefix):]
                if suffix.isdigit():
                    num = int(suffix)
                    if num > max_num:
                        max_num = num
            return f"{prefix}{max_num + 1}"
        finally:
            cursor.close()
            conn.close()
