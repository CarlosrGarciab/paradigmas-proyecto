# TODO App - Aplicación de Gestión de Tareas

Una aplicación web profesional para la gestión de tareas construida con Flask, Bootstrap y JavaScript vanilla.

## Características

- **Gestión completa de tareas**: Crear, editar, eliminar y marcar como completadas
- **Sistema de prioridades**: Organiza tus tareas por prioridad (Alta, Media, Baja)
- **Fechas de vencimiento**: Establece fechas límite para tus tareas
- **Filtros y ordenación**: Filtra por estado y ordena por diferentes criterios
- **Estadísticas en tiempo real**: Visualiza tu progreso con gráficos y métricas
- **Interfaz responsive**: Funciona perfectamente en desktop, tablet y móvil
- **Modo oscuro**: Interfaz que se adapta a las preferencias del sistema
- **Auto-guardado**: Los borradores se guardan automáticamente
- **Atajos de teclado**: Navega rápidamente con shortcuts
- **Notificaciones**: Feedback inmediato de las acciones realizadas

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Un navegador web moderno

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd todo_app
```

### 2. Crear un entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\\Scripts\\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno (opcional)

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-super-segura
DATABASE_URL=sqlite:///todo_app.db
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Estructura del Proyecto

```
todo_app/
├── app.py                 # Aplicación principal Flask
├── models.py              # Modelos de base de datos
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── add_task.html     # Formulario para agregar tareas
│   └── edit_task.html    # Formulario para editar tareas
└── static/              # Archivos estáticos
    ├── css/
    │   └── style.css     # Estilos personalizados
    └── js/
        └── script.js     # JavaScript de la aplicación
```

## Uso de la Aplicación

### Agregar una Tarea

1. Haz clic en "Nueva Tarea" en la navegación
2. Completa el formulario con:
   - **Título**: Nombre descriptivo de la tarea (obligatorio)
   - **Descripción**: Detalles adicionales (opcional)
   - **Prioridad**: Baja, Media o Alta
   - **Fecha de vencimiento**: Fecha límite (opcional)
3. Haz clic en "Guardar Tarea"

### Gestionar Tareas

- **Marcar como completada**: Haz clic en el checkbox junto a la tarea
- **Editar**: Haz clic en el menú de tres puntos y selecciona "Editar"
- **Eliminar**: Haz clic en el menú de tres puntos y selecciona "Eliminar"

### Filtrar y Ordenar

- **Filtros**: Usa el menú "Filtros" para mostrar todas, pendientes o completadas
- **Ordenación**: Usa el menú "Ordenar" para organizar por fecha, prioridad, etc.

### Atajos de Teclado

- `Ctrl + N`: Nueva tarea
- `Ctrl + H`: Ir al inicio
- `Ctrl + F`: Buscar (si está disponible)
- `Escape`: Cerrar modales
- `Ctrl + S`: Guardar formulario (en páginas de edición)

## Configuración Avanzada

### Base de Datos

Por defecto, la aplicación usa SQLite. Para usar PostgreSQL o MySQL:

1. Instala el driver correspondiente:
   ```bash
   # PostgreSQL
   pip install psycopg2-binary
   
   # MySQL
   pip install PyMySQL
   ```

2. Modifica la variable `DATABASE_URL` en tu archivo `.env`:
   ```env
   # PostgreSQL
   DATABASE_URL=postgresql://usuario:contraseña@localhost/todo_db
   
   # MySQL
   DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/todo_db
   ```

### Personalización de Estilos

Los estilos están en `static/css/style.css`. Puedes modificar:

- **Colores**: Cambia las variables CSS en `:root`
- **Fuentes**: Modifica `--font-family-primary`
- **Animaciones**: Ajusta `--transition` y las animaciones CSS

### Funcionalidades Adicionales

Para habilitar funcionalidades adicionales, descomenta las dependencias relevantes en `requirements.txt`:

- **Migración de BD**: Flask-Migrate
- **Autenticación**: Flask-Login
- **API REST**: Flask-RESTful
- **Testing**: pytest, pytest-flask

## Solución de Problemas

### Error: "No module named 'flask'"

```bash
pip install Flask
```

### Error: "Port 5000 already in use"

Cambia el puerto en `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### La base de datos no se crea

Asegúrate de que la carpeta tenga permisos de escritura y ejecuta:

```python
from app import app, db
with app.app_context():
    db.create_all()
```

### Problemas con estilos CSS

1. Verifica que los archivos estén en `static/css/`
2. Limpia la caché del navegador (Ctrl+F5)
3. Verifica que no haya errores en la consola del navegador

## Despliegue en Producción

### Heroku

1. Crea un archivo `Procfile`:
   ```
   web: python app.py
   ```

2. Agrega las dependencias de producción:
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

3. Configura las variables de entorno en Heroku

### PythonAnywhere

1. Sube los archivos al servidor
2. Crea una nueva aplicación web
3. Configura el WSGI file
4. Instala las dependencias

### Docker

Crea un `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

## Métricas y Analytics

La aplicación incluye:

- **Estadísticas básicas**: Total, completadas, pendientes
- **Tasa de completación**: Porcentaje de progreso
- **Filtros por prioridad**: Distribución de tareas por importancia
- **API endpoints**: `/api/stats` y `/api/tasks` para integraciones

## Seguridad

### Recomendaciones

1. **Cambia la SECRET_KEY** en producción
2. **Usa HTTPS** en producción
3. **Valida inputs** del usuario
4. **Mantén dependencias actualizadas**

### Variables de Entorno Importantes

```env
SECRET_KEY=clave-super-secreta-y-unica
FLASK_ENV=production
DATABASE_URL=tu-url-de-base-de-datos-produccion
```

## Contribuciones

1. Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para detalles.

## Soporte

Si tienes problemas o preguntas:

1. Revisa la sección de solución de problemas
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## Agradecimientos

- **Flask**: Framework web de Python
- **Bootstrap**: Framework CSS para UI responsive
- **Font Awesome**: Iconos
- **SQLAlchemy**: ORM para Python

---

Si te gusta este proyecto, no olvides darle una estrella!

**Contacto**: [tu-email@ejemplo.com]
**Demo**: [https://tu-demo.herokuapp.com]