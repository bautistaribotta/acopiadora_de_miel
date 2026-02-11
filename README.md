# Southern Honey Group - Sistema de Gestión de Acopio

Sistema de gestión de escritorio ("Desktop Application") desarrollado en **Python** para la administración de operaciones de compra y venta de miel. La aplicación permite el control de clientes, gestión de productos, seguimiento de cuentas corrientes y registro de transacciones con soporte para múltiples divisas.

## 📋 Descripción Técnica

El proyecto sigue una arquitectura **MVC (Modelo-Vista-Controlador)** para garantizar la separación de responsabilidades, la escalabilidad del código y facilitar el mantenimiento.

* **Patrón de Diseño:** MVC.
* **Interfaz Gráfica (GUI):** Tkinter con estilos personalizados (`ttk`).
* **Persistencia:** Base de datos relacional (MySQL/MariaDB).
* **Concurrencia:** Implementación de *Lazy Loading* en módulos de vista para optimizar tiempos de carga.

## 🛠 Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Base de Datos:** MySQL / MariaDB
* **Librerías Principales:**
    * `mysql-connector-python`: Conexión y manejo de transacciones con BDD.
    * `tkinter`: Interfaz gráfica de usuario.
    * `Pillow (PIL)`: Manejo y renderizado de imágenes/iconos.
    * `requests` (Implícito): Para consulta de cotizaciones (Dólar Oficial/Blue).

## 🚀 Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/bautistaribotta/acopiadora_de_miel.git
    cd acopiadora_de_miel
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install mysql-connector-python pillow requests
    ```

3.  **Configuración de Base de Datos:**
    * Importar el script SQL inicial (si está disponible en `/db`).
    * Configurar credenciales en `model/conexion_db.py`:
    ```python
    db_configuracion = {
        "host": "localhost",
        "user": "root",
        "password": "tu_contraseña",
        "database": "southern_honey_group"
    }
    ```

4.  **Ejecución:**
    ```bash
    python login.py
    # O ejecutar directamente la vista principal durante desarrollo:
    python -m view.pantalla_principal_view
    ```

## ✅ Funcionalidades Implementadas

* **Autenticación:** Sistema de Login con roles (Administrador/Usuario) y validación segura.
* **Gestión de Operaciones:** Registro transaccional de compras/ventas con cálculo automático de totales.
* **Cotizaciones en Tiempo Real:** Visualización integrada del valor del Dólar (Oficial/Blue).
* **Manejo de Errores:** Sistema de logs visuales (`messagebox`) y gestión de excepciones en base de datos.
* **Navegación:** Menú principal dinámico basado en permisos de usuario.

## 🚧 Roadmap (Pendientes y Mejoras)

Las siguientes características se encuentran en fase de planificación o desarrollo:

* [ ] **Reportes:** Generación de comprobantes y remitos en formato PDF.
* [ ] **Módulo de Deudores:** Refactorización y finalización de la lógica de cuentas corrientes (`view/deudores_view.py`).
* [ ] **Tests Unitarios:** Implementación de cobertura de pruebas para los controladores críticos (especialmente `operaciones_controlador`).
* [ ] **Migración de Configuración:** Externalizar credenciales de BDD a variables de entorno (`.env`) para mayor seguridad.

## 📄 Licencia

Este proyecto es de uso académico y privado para **Southern Honey Group**.

---
*Desarrollado por Bautista Ribotta - Ing. en Software*
