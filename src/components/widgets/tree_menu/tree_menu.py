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

    def create_branch(self, title, sub_items):
        """Crea una rama con sub-elementos."""
        branch = QStandardItem(title)
        for item in sub_items:
            branch.appendRow(QStandardItem(item))
        return branch

    def init_ui(self):
        """Inicializa el menú con las ramas principales."""
        root_node = self.model.invisibleRootItem()

        # Definir estructura del árbol
        tree_structure = {
            'Inicio': ['ACRIL CAR', 'Alta de Cliente', 'Operaciones con Cliente', 'Tabla de Clientes'],
            'Planilla': ['Alta de Colaborador', 'Operaciones con Colaborador', 'Adelanto de Salario', 'Registro por Colaborador'],
            'Operaciones con Ordenes': ['Crear Orden', 'Actualizar Orden', 'Cerrar Orden'],
            'Operaciones de Caja': ['Ingresos de Caja', 'Salidas de Caja', 'Arqueo de Caja'],
            'Operaciones de Administración': ['Operaciones de Usuario', 'Aprobar Descuento', 'Eliminar Orden']
        }

        # Crear y agregar ramas al modelo
        self.branches = {}
        for title, sub_items in tree_structure.items():
            self.branches[title] = self.create_branch(title, sub_items)
            root_node.appendRow(self.branches[title])

        self.expandAll()

    def on_item_selected(self, index):
        """Emite el texto del ítem seleccionado."""
        item = self.model.itemFromIndex(index)
        if item and item.parent():  # Solo emitir si es un sub-elemento
            self.item_selected.emit(item.text())

    def set_role_visibility(self, role):
        """Oculta o muestra ramas según el rol del usuario."""
        root_node = self.model.invisibleRootItem()

        if role == 'user' and 'Operaciones de Administración' in self.branches:
            root_node.removeRow(self.branches['Operaciones de Administración'].row())
            del self.branches['Operaciones de Administración']

        elif role == 'admin' and 'Operaciones de Administración' not in self.branches:
            admin_branch = self.create_branch(
                'Operaciones de Administración',
                ['Operaciones de Usuario', 'Aprobar Descuento', 'Eliminar Orden']
            )
            root_node.appendRow(admin_branch)
            self.branches['Operaciones de Administración'] = admin_branch
