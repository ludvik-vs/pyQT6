py -3.10 -m venv .venv

.venv\Scripts\activate

pip install PyQt6 pyqt6-tools

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