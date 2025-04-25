import os
import json
import sqlite3
from datetime import datetime
from git import Repo, exc  # Import exc to handle Git exceptions
import sys
import traceback  # Import traceback for error logging

class SyncOperations:
    def __init__(self):
        # Determine base path
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(base_path)))

        # Set sync directory outside the frozen application directory
        self.SYNC_DIR = os.path.join(base_path, "sync")
        self.DATA_DIR = os.path.join(self.SYNC_DIR, "data")
        self.TABLAS = []
        self.DB_PATH = None
        self.USUARIO_ID = None

    def log_error(self, error_type, error_msg, error_trace=None):
        """Helper method to format error messages"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_log = f"[{timestamp}] {error_type}: {error_msg}"
        if error_trace:
            error_log += f"\nStack Trace:\n{error_trace}"
        print(error_log)
        return error_log

    def init_sync(self, repo_url, token, db_path, usuario_id, tablas):
        self.TABLAS = tablas
        self.DB_PATH = db_path
        self.USUARIO_ID = usuario_id
        
        # Create sync directories
        os.makedirs(self.DATA_DIR, exist_ok=True)
        for tabla in self.TABLAS:
            os.makedirs(os.path.join(self.DATA_DIR, tabla), exist_ok=True)
        
        # Add sincronizado column if it doesn't exist
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        
        for tabla in self.TABLAS:
            cur.execute(f"PRAGMA table_info({tabla})")
            columns = [col[1] for col in cur.fetchall()]
            
            if 'sincronizado' not in columns:
                try:
                    cur.execute(f"ALTER TABLE {tabla} ADD COLUMN sincronizado INTEGER DEFAULT 0")
                except sqlite3.OperationalError:
                    pass
        
        conn.commit()
        conn.close()

    def export_tabla(self, tabla):
        carpeta = os.path.join(self.DATA_DIR, tabla)
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabla} WHERE sincronizado = 0")
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        conn.close()

        if not rows:
            return

        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        nombre = f"{ts}-{self.USUARIO_ID}.json"
        path = os.path.join(carpeta, nombre)

        with open(path, "w", encoding="utf-8") as f:
            payload = [dict(zip(cols, r)) for r in rows]
            json.dump(payload, f, indent=2, ensure_ascii=False)

        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        pk = cols[0]
        cur.executemany(
            f"UPDATE {tabla} SET sincronizado = 1 WHERE {pk} = ?",
            [(r[0],) for r in rows]
        )
        conn.commit()
        conn.close()

    def import_tabla(self, tabla):
        carpeta = os.path.join(self.DATA_DIR, tabla)
        if not os.path.isdir(carpeta):
            return

        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({tabla})")
        cols = [info[1] for info in cur.fetchall()]

        for fname in sorted(os.listdir(carpeta)):
            if not fname.endswith('.json'):
                continue
            full = os.path.join(carpeta, fname)
            with open(full, encoding='utf-8') as f:
                data = json.load(f)
            for record in data:
                placeholders = ','.join('?' for _ in cols)
                cols_str = ','.join(cols)
                sql = f"INSERT OR IGNORE INTO {tabla} ({cols_str}) VALUES ({placeholders})"
                vals = [record.get(c) for c in cols]
                cur.execute(sql, vals)
        conn.commit()
        conn.close()

    def sincronizar_completo(self, repo_url, token, db_path, usuario_id, tablas):
        self.init_sync(repo_url, token, db_path, usuario_id, tablas)

        for tabla in tablas:
            self.export_tabla(tabla)

        url_auth = repo_url.replace('https://', f'https://{token}@')

        if not os.path.exists(os.path.join(self.SYNC_DIR, '.git')):
            repo = Repo.init(self.SYNC_DIR)
            repo.create_remote('origin', url_auth)
        else:
            repo = Repo(self.SYNC_DIR)

        try:
            repo.remote('origin').pull(rebase=True)
        except exc.GitCommandError as e:
            error_msg = self.log_error(
                "ERROR GIT",
                f"Git pull failed: {str(e)}",
                traceback.format_exc()
            )
            print(f"Command: {e.command}, Status: {e.status}, Stderr: {e.stderr}")
            raise e

        repo.git.add(A=True)
        repo.index.commit(f"sync {datetime.now().isoformat()} by {usuario_id}")
        repo.remote('origin').push()

        for tabla in tablas:
            self.import_tabla(tabla)
