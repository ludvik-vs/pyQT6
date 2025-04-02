### Crear entorno virtual con py
py -3.9 -m venv .venv
py -3.10 -m venv .venv
py -3.11 -m venv .venv
py -3.12 -m venv .venv
py -3.13 -m venv .venv

windows
.venv\Scripts\activate    
.venv\Scripts\deactivate

ubuntu
source .venv/bin/activate

pip install PyQt6 pyqt6-tools

pip install -r requirements.txt

pip freeze > requirements.txt

pyuic6 Login.ui -o login_ui.py
pyuic6 MainWindow.ui -o main_window_ui.py



db = DatabaseManager()
db.connect()

# Probar usuarios predeterminados
admin_data = db.get_user("admin", "admin")
print(admin_data)  # {'username': 'admin', 'role': 'admin'}

user_data = db.get_user("user", "user")
print(user_data)  # {'username': 'user', 'role': 'user'}

fail_data = db.get_user("admin", "wrongpass")
print(fail_data)  # None

db.close()

pyinstaller --onefile --icon=assets/icons/icono.ico main.py
pyinstaller --onefile --icon=assets/icons/icono.ico --add-data "src/styles;src/styles" --add-data "assets;assets" main.py