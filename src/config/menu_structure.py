class MenuStructure:
    @staticmethod
    def get_menu_structure():
        return {
            '1 - Inicio': [
                'ACRIL CAR', 
                'Cambiar Contraseña'
                ],
            '2 - Administración de Usuarios': [
                'Crear Usuario', 
                'Operaciones de Usuario', 
                'Tabla Usuario'
                ],
            '3 - Clientes': [
                'Alta de Cliente', 
                'Operaciones con Cliente', 
                'Tabla de Clientes'
                ],
            '4 - Órdenes de Trabajo': [
                'Crear Orden T', 
                'Detalle Orden T', 
                'Tabla Orden T'
                ],
            '5 - Órdenes de Producción': [
                'Crear Orden P', 
                'Detalle Orden P'
                ],
            '6 - Operaciones de Caja': [
                'Ingresos de Caja', 
                'Egresos de Caja', 
                'Arqueo de Efectivo'
            ],
            '7 - Reportes Operativos': [
                'Movimientos del Dia', 
                'Moviminetos Rango de Fecha'
                ],
            '8 - Planilla': [
                'Alta de Colaborador', 
                'Operaciones con Colaborador', 
                'Detalle por Colaborador', 
                'Tabla Planilla'
            ],
            '9 - Operaciones de Administración': [
                'Aprobar Descuento', 
                'Anular Orden', 
                'Catalogo de Movimientos',
            ],
            '10 - Reportes Administrativos': [
                'Balance (I/E)', 
                'Balance Rango de Fecha'
                ]
        }

    @staticmethod
    def get_all_branches():
        return list(MenuStructure.get_menu_structure().keys())