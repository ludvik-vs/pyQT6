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
                'Tabla de Usuarios'
                ],
            '3 - Clientes': [
                'Alta de Cliente', 
                'Operaciones de Cliente', 
                'Tabla de Clientes'
                ],
            '4 - Órdenes de Trabajo': [
                'Crear Orden de Trabajo', 
                'Detalle de Orden', 
                'Tabla de Órdenes'
                ],
            '5 - Órdenes de Producción': [
                'Crear Orden de Producción', 
                'Detalle de Producción'
                ],
            '6 - Operaciones de Caja': [
                'Ingresos de Caja', 
                'Egresos de Caja', 
                'Arqueo de Efectivo'
            ],
            '7 - Reportes Operativos': [
                'Movimientos por Fecha',
                'Balance de Caja',
                'Resumen de Arqueo',
                'Reporte de Órdenes',
                ],
            '8 - Planilla': [
                'Alta de Colaborador', 
                'Operaciones de Colaborador', 
                'Detalle de Colaborador', 
                'Tabla de Planilla'
            ],
            '9 - Operaciones de Administración': [
                'Aprobar Descuento', 
                'Anular Orden', 
                'Catálogo de Movimientos'
            ],
            '10 - Reportes Administrativos': [
                'Registro de Descuentos',
                ]
        }

    @staticmethod
    def get_all_branches():
        return list(MenuStructure.get_menu_structure().keys())