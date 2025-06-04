import os
import json
import sqlite3
from datetime import datetime
from git import Repo, exc  # Import exc to handle Git exceptions
import sys
import traceback  # Import traceback for error logging

class SyncOperations:
    """
    Clase que maneja las operaciones de sincronización entre la base de datos local
    y un repositorio Git remoto.
    """

    def __init__(self):
        """
        Inicializa las rutas y directorios necesarios para la sincronización.
        Determina la ruta base según si la aplicación está empaquetada (.exe) o en desarrollo.
        """
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
        """
        Registra y formatea mensajes de error con marca de tiempo.
        
        Args:
            error_type (str): Tipo de error (ej: ERROR DB, ERROR GIT)
            error_msg (str): Mensaje descriptivo del error
            error_trace (str, opcional): Traza completa del error
        
        Returns:
            str: Mensaje de error formateado con timestamp
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_log = f"[{timestamp}] {error_type}: {error_msg}"
        if error_trace:
            error_log += f"\nStack Trace:\n{error_trace}"
        print(error_log)
        return error_log

    def init_sync(self, repo_url, token, db_path, usuario_id, tablas):
        """
        Inicializa el entorno de sincronización.
        
        Args:
            repo_url (str): URL del repositorio Git
            token (str): Token de autenticación de GitHub
            db_path (str): Ruta al archivo de base de datos
            usuario_id (str): Identificador único del usuario/máquina
            tablas (list): Lista de tablas a sincronizar
        
        Operaciones:
            1. Crea directorios de sincronización
            2. Agrega columna 'sincronizado' a las tablas si no existe
        """
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
        """
        Exporta registros no sincronizados de una tabla a archivo JSON en lotes.
        
        Args:
            tabla (str): Nombre de la tabla a exportar
        """
        carpeta = os.path.join(self.DATA_DIR, tabla)
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabla} WHERE sincronizado = 0")
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        conn.close()
    
        if not rows:
            return
    
        batch_size = 100  # Define the size of each batch
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            nombre = f"{ts}-{self.USUARIO_ID}-{i//batch_size}.json"
            path = os.path.join(carpeta, nombre)
    
            with open(path, "w", encoding="utf-8") as f:
                payload = [dict(zip(cols, r)) for r in batch]
                json.dump(payload, f, indent=2, ensure_ascii=False)
    
            # Mark records as synchronized
            conn = sqlite3.connect(self.DB_PATH)
            cur = conn.cursor()
            pk = cols[0]
            cur.executemany(
                f"UPDATE {tabla} SET sincronizado = 1 WHERE {pk} = ?",
                [(r[0],) for r in batch]
            )
            conn.commit()
            conn.close()

    def import_tabla(self, tabla):
        """
        Importa registros desde archivos JSON a la tabla especificada.
        
        Args:
            tabla (str): Nombre de la tabla donde importar los datos
        
        Operaciones:
            1. Lee todos los archivos JSON del directorio de la tabla
            2. Inserta registros en la base de datos ignorando duplicados
            3. Mantiene la estructura de columnas original de la tabla
        """
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
        try:
            # 1. Inicialización básica y creación de directorios
            self.init_sync(repo_url, token, db_path, usuario_id, tablas)
            print("Inicialización completada")
    
            # 2. Configuración de Git
            url_auth = repo_url.replace('https://', f'https://{token}@')
            try:
                if not os.path.exists(os.path.join(self.SYNC_DIR, '.git')):
                    # Initialize new repository
                    repo = Repo.init(self.SYNC_DIR)
                    repo.create_remote('origin', url_auth)
                    
                    # Create and commit README
                    open(os.path.join(self.SYNC_DIR, 'README.md'), 'w').write('Data Sync Repository')
                    repo.index.add(['README.md'])
                    repo.index.commit('Initial commit')
                    
                    # Set main branch
                    repo.git.branch('-M', 'main')
                    print(f"Repositorio Git inicializado en: {self.SYNC_DIR}")
                else:
                    repo = Repo(self.SYNC_DIR)
                    repo.remote('origin').set_url(url_auth)
                    print("Repositorio Git existente configurado")
    
                # Configure Git user for this repository
                repo.config_writer().set_value("user", "name", "Sync Bot").release()
                repo.config_writer().set_value("user", "email", "sync@acrilcar.com").release()
    
                # Ensure we're on main branch
                if repo.active_branch.name != 'main':
                    repo.git.checkout('-B', 'main')
    
                # Handle unstaged changes
                if repo.is_dirty() or len(repo.untracked_files) > 0:
                    print("Guardando cambios locales pendientes...")
                    repo.git.add(A=True)
                    commit_msg = f"sync (pre-pull) {datetime.now().isoformat()} by {usuario_id}"
                    repo.index.commit(commit_msg)
    
                try:
                    # Try to fetch and set upstream
                    origin = repo.remote('origin')
                    origin.fetch()
                    
                    # Set upstream and pull
                    repo.git.branch('--set-upstream-to=origin/main', 'main')
                    repo.git.pull('--allow-unrelated-histories')
                except exc.GitCommandError as e:
                    if "couldn't find remote ref" in str(e) or "no such branch" in str(e).lower():
                        # If remote is empty, push and set upstream
                        print("Configurando rama principal en remoto...")
                        repo.git.push('-u', 'origin', 'main')
                    else:
                        raise
    
                # Pull changes with better error handling
                try:
                    print("Obteniendo cambios remotos...")
                    origin = repo.remote('origin')
                    origin.fetch()
                    
                    if len(origin.refs):
                        repo.git.pull('origin', 'main', '--allow-unrelated-histories')
                    else:
                        print("Repositorio remoto vacío, preparando primer push")
                except exc.GitCommandError as e:
                    if "couldn't find remote ref" in str(e):
                        print("Repositorio remoto vacío, continuando...")
                    else:
                        raise
    
                # 4. Importar cambios remotos a SQLite
                print("Actualizando base de datos con cambios remotos...")
                for tabla in tablas:
                    self.import_tabla(tabla)
                print("Base de datos actualizada con cambios remotos")
    
                # 5. Exportar cambios locales
                print("Exportando cambios locales...")
                for tabla in tablas:
                    self.export_tabla(tabla)
                print("Cambios locales exportados")
    
                # 6 y 7. Add, commit y push
                if repo.is_dirty() or len(repo.untracked_files) > 0:
                    print("Preparando cambios para sincronización...")
                    repo.git.add(A=True)
                    commit_msg = f"sync {datetime.now().isoformat()} by {usuario_id}"
                    repo.index.commit(commit_msg)
                    print("Enviando cambios al repositorio remoto...")
                    repo.remote('origin').push()
                    print("Sincronización completada exitosamente")
                else:
                    print("No hay cambios locales para sincronizar")
    
            except exc.GitCommandError as e:
                error_msg = self.log_error(
                    "ERROR GIT",
                    f"Error en operación Git: {str(e)}",
                    traceback.format_exc()
                )
                raise
    
        except Exception as e:
            error_msg = self.log_error(
                "ERROR CRÍTICO",
                f"Error en sincronización: {str(e)}",
                traceback.format_exc()
            )
            raise
