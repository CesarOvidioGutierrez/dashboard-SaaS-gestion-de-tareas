# Mini SaaS - Gestión de Tareas

Un mini proyecto de gestión de tareas construido con Flask (backend) y React (frontend) usando Docker.

## Características

- **Autenticación**: Sistema completo de registro e inicio de sesión usando JWT (JSON Web Tokens)
- **CRUD de Tareas**: Crear, leer, actualizar y eliminar tareas
- **Validación de Datos**: Validación robusta usando Marshmallow
- **API RESTful**: Endpoints bien definidos con formato JSON
- **Seguridad**: Protección de rutas, contraseñas hasheadas, y validación de propiedad de recursos

## Tecnologías Utilizadas

### Backend
- **Flask**: Framework web ligero para Python
- **SQLAlchemy**: ORM para interactuar con la base de datos
- **Flask-Migrate**: Gestión de migraciones de base de datos
- **Flask-Marshmallow**: Serialización y validación de datos
- **PyJWT**: Generación y verificación de tokens JWT
- **PostgreSQL**: Base de datos relacional

### Frontend
- **React**: Biblioteca para construir interfaces de usuario
- **Vite**: Herramienta de construcción para desarrollo frontend
- **Axios**: Cliente HTTP para realizar peticiones a la API

## Requisitos Previos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Instalación y Ejecución

1. **Configurar variables de entorno**

Crea un archivo `.env` en la carpeta `backend` con las siguientes variables:

```
# PostgreSQL
POSTGRES_DB=mini_saas
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_PORT=5435
POSTGRES_HOST=db

# Flask
FLASK_ENV=development
FLASK_APP=app
FLASK_DEBUG=1
FLASK_PORT=5000
DATABASE_URL=postgresql://admin:secret@db:5432/mini_saas

# Seguridad
SECRET_KEY=dev-secret-key-change-in-production

# Frontend
VITE_API_URL=http://localhost:5000
VITE_PORT=5173
VITE_HOST=0.0.0.0
```

2. **Iniciar los contenedores**

```bash
docker-compose up -d
```

3. **Verificar que los contenedores estén funcionando**

```bash
docker-compose ps
```

## Acceso a la Aplicación

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **API Backend**: [http://localhost:5000/api/hello](http://localhost:5000/api/hello)
- **API Health Check**: [http://localhost:5000/api/health](http://localhost:5000/api/health)
- **Base de datos PostgreSQL**: Accesible en el puerto 5435

## API Endpoints

### Autenticación

- **POST /api/auth/register**: Registrar un nuevo usuario
  ```json
  {
    "username": "usuario",
    "email": "usuario@ejemplo.com",
    "password": "contraseña"
  }
  ```

- **POST /api/auth/login**: Iniciar sesión
  ```json
  {
    "username": "usuario",
    "password": "contraseña"
  }
  ```

### Tareas (requieren autenticación)

- **GET /api/tasks**: Obtener todas las tareas del usuario
- **GET /api/tasks/:id**: Obtener una tarea específica
- **POST /api/tasks**: Crear una nueva tarea
  ```json
  {
    "title": "Título de la tarea",
    "description": "Descripción de la tarea",
    "status": "pendiente",
    "priority": "media",
    "due_date": "2023-12-31T23:59:59"
  }
  ```
- **PUT /api/tasks/:id**: Actualizar una tarea existente
- **DELETE /api/tasks/:id**: Eliminar una tarea

Para las rutas que requieren autenticación, se debe incluir el token JWT en el encabezado:
```
Authorization: Bearer <token>
```

## Comandos Útiles

### Ver logs de los contenedores

```bash
# Ver logs de todos los contenedores
docker-compose logs

# Ver logs de un contenedor específico
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Detener los contenedores

```bash
docker-compose down
```

### Reconstruir los contenedores

```bash
docker-compose up -d --build
```

### Ejecutar comandos dentro de los contenedores

```bash
# Ejecutar comandos en el backend
docker-compose exec backend flask --help

# Comandos para migraciones de base de datos
docker-compose exec backend flask db init     # Solo la primera vez
docker-compose exec backend flask db migrate -m "Descripción"
docker-compose exec backend flask db upgrade

# Ejecutar comandos en el frontend
docker-compose exec frontend npm run build
```

## Solución de Problemas

### Error de conexión entre frontend y backend

Si el frontend no puede conectarse al backend, verifica:

1. Que el backend esté funcionando correctamente: `curl http://localhost:5000/api/hello`
2. Que CORS esté configurado correctamente en el backend
3. Que la URL del backend en el frontend sea correcta (App.jsx)

### Error de conexión a la base de datos

Si el backend no puede conectarse a la base de datos:

1. Verifica que el contenedor de PostgreSQL esté funcionando
2. Verifica las credenciales en el archivo .env
3. Verifica los logs del backend: `docker-compose logs backend`

### Errores de autenticación

Si recibes errores 401 (No autorizado):

1. Verifica que estás enviando el token JWT correctamente en el encabezado
2. El token podría haber expirado (duración: 1 día)
3. Intenta iniciar sesión nuevamente para obtener un nuevo token

## Desarrollo

### Estructura del Backend

El backend está construido con Flask y sigue una estructura modular:

- **app/\_\_init\_\_.py**: Configura la aplicación Flask y registra las rutas
- **app/routes/**: Contiene los endpoints de la API
  - **app/routes/auth_routes.py**: Rutas de autenticación
  - **app/routes/task_routes.py**: Rutas para gestión de tareas
- **app/models/**: Define los modelos de datos usando SQLAlchemy
  - **app/models/user.py**: Modelo de usuario con métodos de autenticación
  - **app/models/task.py**: Modelo de tarea
- **app/schemas.py**: Define los esquemas para serialización y validación con Marshmallow
- **app/utils/**: Utilidades como el decorador de autenticación
- **migrations/**: Migraciones de base de datos generadas por Flask-Migrate

### Estructura del Frontend

El frontend está construido con React y Vite:

- **src/components/**: Componentes reutilizables
- **src/pages/**: Páginas de la aplicación
- **src/services/**: Servicios para comunicación con la API
- **src/App.jsx**: Componente principal
- **src/main.jsx**: Punto de entrada

## Licencia

[MIT](LICENSE)
