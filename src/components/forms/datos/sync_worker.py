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
    # Define signals
    finished = pyqtSignal(bool, str)
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)  # Add this signal
    
    BATCH_SIZE = 10

    def __init__(self, db_path, repo_url, token, tablas):
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
        try:
            self.status_updated.emit("Iniciando proceso de sincronización...")  # Changed from log_message to status_updated
            self.progress_updated.emit(0)

            # 1. Verificar base de datos
            if not os.path.exists(self.db_path):
                error_msg = self.log_error("ERROR SISTEMA", f"La base de datos no existe en: {self.db_path}")
                self.finished.emit(False, error_msg)
                return

            self.progress_updated.emit(10)
            self.status_updated.emit("Verificando tablas...")  # Changed from log_message to status_updated

            # 2. Verificar que las tablas existan
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            for tabla in self.tablas:
                try:
                    cur.execute(f"SELECT 1 FROM {tabla} LIMIT 1")
                    self.status_updated.emit(f"Tabla {tabla} verificada correctamente")  # Changed from log_message to status_updated
                except sqlite3.OperationalError:
                    error_msg = self.log_error("ERROR DB", f"La tabla {tabla} no existe en la base de datos")
                    conn.close()
                    self.finished.emit(False, error_msg)
                    return
            conn.close()

            self.progress_updated.emit(30)
            self.status_updated.emit("Inicializando directorio de sincronización...")  # Changed from log_message

            # 3. Verificar directorio de sincronización
            if not self.initialize_sync_directory():
                error_msg = self.log_error("ERROR SISTEMA", "Error al crear directorio de sincronización")
                self.finished.emit(False, error_msg)
                return

            self.progress_updated.emit(50)
            self.status_updated.emit("Preparando columnas de sincronización...")  # Changed from log_message

            # 4. Verificar columnas de sincronización
            if not self.initialize_sync_columns():
                error_msg = self.log_error("ERROR DB", "Error al inicializar columnas de sincronización")
                self.finished.emit(False, error_msg)
                return

            self.progress_updated.emit(70)
            self.status_updated.emit("Iniciando sincronización con repositorio remoto...")  # Changed from log_message

            # 5. Ejecutar sincronización
            try:
                self.sync_ops.sincronizar_completo(
                    repo_url=self.repo_url,
                    token=self.token,
                    db_path=self.db_path,
                    usuario_id=self.machine_id,
                    tablas=self.tablas
                )
                self.progress_updated.emit(100)
                self.status_updated.emit("¡Sincronización completada exitosamente!")  # Changed from log_message
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

    def commit_batch(self, repo, tabla, batch):
        """Commit a batch of records"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        commit_message = f"Sync {tabla} - Batch {timestamp}"
        
        # Here you would write the batch data to files
        # Implementation depends on your specific data format needs
        
        repo.index.add('*')
        repo.index.commit(commit_message)