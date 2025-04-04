from PyQt6.QtWidgets import QTreeView
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from src.config.menu_structure import MenuStructure

class TreeMenu(QTreeView):
    item_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Transacciones'])
        self.setModel(self.model)
        self.tree_structure = MenuStructure.get_menu_structure()
        self.init_ui()
        self.clicked.connect(self.on_item_selected)
        self.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            current_index = self.currentIndex()
            self.on_item_selected(current_index)
        super().keyPressEvent(event)

    def create_branch(self, title, sub_items):
        branch = QStandardItem(title)
        for item in sub_items:
            branch.appendRow(QStandardItem(item))
        return branch

    def on_item_selected(self, index):
        item = self.model.itemFromIndex(index)
        if item and item.parent():
            self.item_selected.emit(item.text())

    def init_ui(self):
        root_node = self.model.invisibleRootItem()
        sorted_keys = sorted(self.tree_structure.keys(), key=lambda x: int(x.split(' - ')[0]))
        for title in sorted_keys:
            sub_items = self.tree_structure[title]
            branch = self.create_branch(title, sub_items)
            root_node.appendRow(branch)
        self.expandAll()

    def set_user_access(self, user_access):
        """Construye el árbol basado en los accesos del usuario."""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Transacciones'])
        root_node = self.model.invisibleRootItem()
        self.branches = {}

        # Ordenar las claves numéricamente antes de procesar user_access
        sorted_keys = sorted(self.tree_structure.keys(), key=lambda x: int(x.split(' - ')[0]))

        for title in sorted_keys:
            if title in self.tree_structure:
                self.branches[title] = self.create_branch(title, [])
                root_node.appendRow(self.branches[title])

        for branch_name, sub_branch_name in user_access:
            if branch_name in self.branches:
                if sub_branch_name:
                    self.branches[branch_name].appendRow(QStandardItem(sub_branch_name))
                else:
                    for sub_item in self.tree_structure[branch_name]:
                        if sub_item not in [self.branches[branch_name].child(i).text() for i in range(self.branches[branch_name].rowCount())]:
                            self.branches[branch_name].appendRow(QStandardItem(sub_item))
