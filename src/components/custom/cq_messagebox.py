from PyQt6.QtWidgets import QMessageBox

class CQMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()

    def show_message(self, message, title, icon):
        self.setIcon(icon)
        self.setText(message)
        self.setWindowTitle(title)
        self.exec()

    def success_message(self, message):
        self.setIcon(QMessageBox.Icon.Information)
        self.setText(message)
        self.setWindowTitle("Success")
        self.exec()

    def error_message(self, message):
        self.setIcon(QMessageBox.Icon.Critical)
        self.setText(message)
        self.setWindowTitle("Error")
        self.exec()
    
    def warning_message(self, message):
        self.setIcon(QMessageBox.Icon.Warning)
        self.setText(message)
        self.setWindowTitle("Warning")
        self.exec()
    
    def info_message(self, message):
        self.setIcon(QMessageBox.Icon.Information)
        self.setText(message)
        self.setWindowTitle("Information")
        self.exec()

    def question_message(self, message):
        self.setIcon(QMessageBox.Icon.Question)
        self.setText(message)
        self.setWindowTitle("Question")
        self.exec()
    
