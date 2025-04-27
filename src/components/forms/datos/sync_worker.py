import os
from PyQt6.QtCore import QThread, pyqtSignal
import uuid
import sqlite3
import sys
import traceback
from datetime import datetime
from git import exc  # Add this import
from src.components.forms.datos.sync_operations import SyncOperations

class GitSyncWorker(QThread):
    """
    Worker thread para manejar la sincronización con Git.
    Gestiona la sincronización de datos entre la base de datos local y un repositorio remoto.
    """
    
    # Señal que se emite cuando finaliza la sincronización
    # Parámetros: (éxito: bool, mensaje: str)
    finished = pyqtSignal(bool, str)

    def __init__(self, db_path, repo_url, token, tablas):
        """
        Inicializa el worker de sincronización.
        
        Args:
            db_path (str): Ruta al archivo de la base de datos
            repo_url (str): URL del repositorio Git
            token (str): Token de autenticación de GitHub
            tablas (list): Lista de nombres de tablas a sincronizar
        """
        super().__init__()
        self.db_path = db_path
        self.repo_url = repo_url
        self.token = token
        self.tablas = tablas
        self.machine_id = str(uuid.getnode())  # Identificador único de la máquina
        self.sync_ops = SyncOperations()
    
    def log_error(self, error_type, error_msg, error_trace=None):
        """
        Registra y formatea errores del proceso de sincronización.
        
        Args:
            error_type (str): Tipo de error
            error_msg (str): Mensaje de error
            error_trace (str, opcional): Traza del error
        
        Returns:
            str: Mensaje de error formateado con timestamp
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_log = f"[{timestamp}] {error_type}: {error_msg}"
        if error_trace:
            error_log += f"\nStack Trace:\n{error_trace}"
        print(error_log)
        return error_log

    def initialize_sync_columns(self):
        """
        Inicializa las columnas de sincronización en las tablas.
        Agrega la columna 'sincronizado' a cada tabla si no existe.
        
        Returns:
            bool: True si la inicialización fue exitosa, False en caso contrario
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for tabla in self.tablas:
                try:
                    cursor.execute(f"PRAGMA table_info({tabla})")
                    columnas = [col[1] for col in cursor.fetchall()]
                    if "sincronizado" not in columnas:
                        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN sincronizado INTEGER DEFAULT 0")
                except sqlite3.OperationalError as e:
                    error_msg = self.log_error(
                        "ERROR DB",
                        f"Tabla inexistente o inaccesible: {tabla}",
                        traceback.format_exc()
                    )
                    conn.close()
                    return False

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            error_msg = self.log_error(
                "ERROR CRÍTICO",
                f"Error general en initialize_sync_columns: {str(e)}",
                traceback.format_exc()
            )
            return False

    def initialize_sync_directory(self):
        """
        Crea y verifica el directorio de sincronización.
        Determina la ruta base según si la aplicación está empaquetada o en desarrollo.
        
        Returns:
            bool: True si el directorio se creó/existe, False si hubo error
        """
        try:
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.abspath(os.path.dirname(__file__))
                base_path = os.path.dirname(os.path.dirname(os.path.dirname(base_path)))
            
            sync_dir = os.path.join(base_path, 'sync')
            os.makedirs(sync_dir, exist_ok=True)
            return True
        except Exception as e:
            error_msg = self.log_error(
                "ERROR SISTEMA",
                f"No se pudo crear el directorio de sincronización: {str(e)}",
                traceback.format_exc()
            )
            return False

    def run(self):
        """
        Método principal que ejecuta el proceso de sincronización.
        """
        try:
            # 1. Verificar base de datos
            if not os.path.exists(self.db_path):
                error_msg = self.log_error("ERROR SISTEMA", f"La base de datos no existe en: {self.db_path}")
                self.finished.emit(False, error_msg)
                return

            # 2. Verificar que las tablas existan
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            for tabla in self.tablas:
                try:
                    cur.execute(f"SELECT 1 FROM {tabla} LIMIT 1")
                except sqlite3.OperationalError:
                    error_msg = self.log_error("ERROR DB", f"La tabla {tabla} no existe en la base de datos")
                    conn.close()
                    self.finished.emit(False, error_msg)
                    return
            conn.close()

            # 3. Verificar directorio de sincronización
            if not self.initialize_sync_directory():
                error_msg = self.log_error("ERROR SISTEMA", "Error al crear directorio de sincronización")
                self.finished.emit(False, error_msg)
                return

            # 4. Verificar columnas de sincronización
            if not self.initialize_sync_columns():
                error_msg = self.log_error("ERROR DB", "Error al inicializar columnas de sincronización")
                self.finished.emit(False, error_msg)
                return

            # 5. Ejecutar sincronización
            try:
                self.sync_ops.sincronizar_completo(
                    repo_url=self.repo_url,
                    token=self.token,
                    db_path=self.db_path,
                    usuario_id=self.machine_id,
                    tablas=self.tablas
                )
                self.finished.emit(True, "Sincronización completada exitosamente")
            except exc.GitCommandError as e:
                error_msg = self.log_error("ERROR GIT", str(e))
                self.finished.emit(False, error_msg)
            except Exception as e:
                error_msg = self.log_error(
                    "ERROR CRÍTICO",
                    f"Error en sincronización: {str(e)}",
                    traceback.format_exc()
                )
                self.finished.emit(False, error_msg)

        except Exception as e:
            error_msg = self.log_error(
                "ERROR CRÍTICO",
                f"Error inesperado: {str(e)}",
                traceback.format_exc()
            )
            self.finished.emit(False, error_msg)