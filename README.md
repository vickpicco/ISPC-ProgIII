# Django Backend API

API backend con Django REST Framework + JWT + PostgreSQL.

## Requisitos

- Python 3.10+
- PostgreSQL
- Virtual environment (recomendado)

## Instalación rápida

```powershell
cd d:\ISPC\ProgramacionIII\ISPC-ProgIII
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configurar PostgreSQL

Edita `backend/settings.py` si tu usuario/password/host/puerto difieren:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'backend_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Crea la base de datos si no existe:

```powershell
psql -U postgres -c "CREATE DATABASE backend_db;"
```

## Migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Ejecutar servidor

```powershell
python manage.py runserver
```

## Endpoints

### POST `/api/register/`

Body JSON:

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "Testpass123"
}
```

Respuesta (201):

```json
{
  "username": "user1",
  "email": "user1@example.com"
}
```

### POST `/api/login/`

Body JSON:

```json
{
  "username": "user1",
  "password": "Testpass123"
}
```

Respuesta (200):

```json
{
  "refresh": "...",
  "access": "...",
  "user": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  }
}
```

### Autenticación en APIs protegidas

Enviar header:

```
Authorization: Bearer <access token>
```

## Pruebas (tests)

```powershell
python manage.py test
```

## Notas de seguridad

- La contraseña se guarda como hash seguro (PBKDF2 por defecto).
- La app también usa `django-encrypted-model-fields` para campos sensibles.

## Estructura de carpetas

- `manage.py` — comandos Django
- `backend/` — configuración del proyecto
- `accounts/` — app con auth/registro/login
- `accounts/tests.py` — tests automáticos

## Para Angular

1) Registrar
2) Loguear y guardar `access`
3) Enviar `Authorization: Bearer <access>` en cada request
