from PyQt6.QtWidgets import QTreeView
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class TreeMenu(QTreeView):
    item_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Operaciones'])
        self.setModel(self.model)
        self.init_ui()
        self.clicked.connect(self.on_item_selected)
        self.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        self.tree_structure = {
            '1 - Inicio': ['ACRIL CAR', 'Cambiar Contraseña'],
            'Clientes': ['Alta de Cliente', 'Operaciones con Cliente', 'Tabla de Clientes'],
            'Ordenes de Trabajo': ['Crear Orden', 'Actualizar Orden'],
            'Ordenes de Prduccion': ['Crear Orden', 'Actualizar Orden'],
            'Operaciones de Caja': ['Ingresos de Caja', 'Salidas de Caja', 'Arqueo de Caja'],
            'Planilla': ['Alta de Colaborador', 'Operaciones con Colaborador', 'Detalle por Colaborador', 'Tabla Planilla'],
            'Reportes Operativos': ['RO 1', 'RO 2', 'RO 3'],
            'Reportes Administrativos': ['RA 1', 'RA 2', 'RA 3'],
            'Administración de Usuarios': ['Crear Usuario', 'Operaciones de Usuario', 'Tabla Usuario'],
            'Operaciones de Administración': ['Aprobar Descuento', 'Eliminar Orden']
        }

    def create_branch(self, title, sub_items):
        branch = QStandardItem(title)
        for item in sub_items:
            branch.appendRow(QStandardItem(item))
        return branch

    def init_ui(self):
        self.expandAll()

    def on_item_selected(self, index):
        item = self.model.itemFromIndex(index)
        if item and item.parent():
            self.item_selected.emit(item.text())

    def set_user_access(self, user_access):
        """Construye el árbol basado en los accesos del usuario."""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Operaciones'])
        root_node = self.model.invisibleRootItem()
        self.branches = {}

        for branch_name, sub_branch_name in user_access:
            if branch_name not in self.branches:
                if branch_name in self.tree_structure:
                    self.branches[branch_name] = self.create_branch(branch_name, [])
                    root_node.appendRow(self.branches[branch_name])
                else:
                    continue # rama no existe en la estructura del arbol.

            if sub_branch_name:
                self.branches[branch_name].appendRow(QStandardItem(sub_branch_name))
            else:
                if branch_name in self.tree_structure:
                    for sub_item in self.tree_structure[branch_name]:
                        if sub_item not in [self.branches[branch_name].child(i).text() for i in range(self.branches[branch_name].rowCount())]:
                            self.branches[branch_name].appendRow(QStandardItem(sub_item))
        self.expandAll()
