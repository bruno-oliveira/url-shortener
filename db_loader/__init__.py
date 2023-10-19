import sqlite3

conn = sqlite3.connect('db_loader/example.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS url_mapping
             (hash_key text unique not null, url text, created_at timestamp default current_timestamp)''')

c.execute('''create index if not exists url_mapping_ts_idx on url_mapping(created_at)''')

c.execute('''CREATE TRIGGER if not exists delete_old_entries
AFTER INSERT ON url_mapping
BEGIN
    DELETE FROM url_mapping WHERE created_at-strftime('%s', datetime('now', '-10 minutes')) <= 0;
END;''')

ans = c.execute('select * from url_mapping')
print(ans)
