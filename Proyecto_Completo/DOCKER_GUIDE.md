# 🐳 Proyecto_Completo - Deployment con Docker

El proyecto Proyecto_Completo ya está automatizado con Docker. Aquí está todo lo que necesitas saber.

## Acceso Rápido

**Frontend:** http://localhost:5173  
**Backend API:** http://localhost:5000/api/transacciones/  
**Base de Datos:** MySQL en puerto 3307 (usuario: root, contraseña: root, base: empresa_db)

## Comando para Iniciar Todo

```powershell
cd Proyecto_Completo
docker compose up -d --pull always
```

Espera 20-30 segundos para que todos los servicios estén listos.

## Verificar el Estado

```powershell
docker compose ps
```

Deberías ver 3 contenedores corriendo:
- `empresa` (MySQL database) - **healthy**
- `backend_api` (Flask API) - puerto 5000
- `frontend_app` (React + Nginx) - puerto 5173

## Detener Todo

```powershell
docker compose down
```

## Tecnología Stack

| Componente | Imagen Base | Tecnología |
|---|---|---|
| **Database** | mysql:8.0 | MySQL 8.0 |
| **Backend** | python:3.11-slim | Flask + Prisma ORM |
| **Frontend** | node:20-alpine + nginx:alpine | React + Vite + Tailwind CSS |

## Archivos Generados

- `docker-compose.yml` - Orquestación de los 3 servicios
- `BACKEND/Dockerfile` - Imagen Python con Flask y Prisma
- `FRONTEND/Dockerfile` - Build multi-stage: Node → Nginx
- `.dockerignore` - En ambas carpetas para optimizar tamaño
- `BACKEND/app.py` - Modificado para generar cliente Prisma en startup

## Puertos

- **5173**: Frontend (React con Nginx reverse proxy a backend)
- **5000**: Backend Flask API
- **3307**: MySQL (3306 está ocupado, se usa 3307)

## Cómo Funcionan los Contenedores

1. **MySQL** - Inicia primero, espera healthcheck
2. **Backend** - Espera a que MySQL esté saludable, genera cliente Prisma en startup, luego inicia Flask
3. **Frontend** - Inicia en paralelo, incluye reverse proxy para /api/ → backend:5000

## Detalles del Build

- **Backend**: ~400MB (Python 3.11-slim + dependencias + Node para Prisma)
- **Frontend**: ~30MB (Nginx alpine con React compilado)
- **Database**: ~600MB (MySQL 8.0)

## Próximos Pasos

✅ Todo está listo - accede a http://localhost:5173 en el navegador y usa la aplicación

Para modificaciones:
- Cambios en el backend → edita `BACKEND/app.py`, luego `docker compose build backend`
- Cambios en el frontend → edita archivos en `FRONTEND/`, luego `docker compose build frontend`
- Cambios en la BD → edita `BACKEND/schema.prisma`, luego `docker exec backend_api prisma db push`
