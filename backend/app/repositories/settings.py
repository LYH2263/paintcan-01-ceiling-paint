import sqlite3
def get_map(conn): return {r["key"]: r["value"] for r in conn.execute("SELECT * FROM settings").fetchall()}
def coverage_coats(conn):
    m = get_map(conn)
    return float(m.get("coverage", "8")), int(m.get("coats", "2"))
def ceiling_coverage_coats(conn):
    m = get_map(conn)
    return float(m.get("ceiling_coverage", "8")), int(m.get("ceiling_coats", "1"))
def upsert(conn, key, value):
    conn.execute("INSERT INTO settings(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, str(value)))
    conn.commit()
