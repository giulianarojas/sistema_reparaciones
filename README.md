# Sistema de Reparaciones

Aplicación web para la gestión de un servicio técnico de reparaciones. 
Permite administrar clientes, equipos, reparaciones y finanzas (ingresos, 
gastos y control del límite de facturación), con una base de conocimiento 
generada a partir del historial de reparaciones.

## Características

- 🔐 Autenticación de usuarios
- 👥 Gestión de clientes (alta, listado, búsqueda y detalle)
- 💻 Gestión de equipos (alta, listado, búsqueda y detalle)
- 🔧 Gestión de reparaciones (alta, listado, búsqueda, detalle, 
  actualización de estado, registro de pagos e historial)
- 💰 Módulo de finanzas: ingresos, gastos y control del límite de 
  facturación (Monotributo)
- 📊 Dashboard con métricas generales
- 📚 Base de conocimiento a partir del historial de reparaciones
- 📤 Exportación de datos a CSV
- 🎨 Interfaz basada en la plantilla SB Admin 2 (Bootstrap)

> ℹ️ **Nota sobre operaciones**: por integridad del historial fiscal y 
> trazabilidad de las reparaciones, este sistema **no elimina** clientes, 
> equipos, reparaciones ni movimientos financieros. En su lugar, permite 
> editar información específica (como el estado de una reparación o las 
> notas) y agregar nuevos registros cuando sea necesario. Esto es una 
> decisión de diseño orientada a la auditoría y el cumplimiento 
> fiscal, no una limitación técnica.

## Stack

- **Backend:** Python 3.10+ + Django 6.0.6
- **Base de datos:** PostgreSQL 13+
- **Frontend:** HTML, CSS, JavaScript (Bootstrap 4, SB Admin 2, Font Awesome)
- **Variables de entorno:** python-dotenv
- **Dependencias principales** (ver `requirements.txt`):
  - asgiref
  - Django
  - psycopg2-binary (driver PostgreSQL)
  - python-dotenv (gestión de variables de entorno)
  - sqlparse
  - tzdata

## Estructura del proyecto

```
sistema_reparaciones/
├── apps/
│   ├── users/          # Autenticación y usuarios
│   ├── customers/      # Clientes
│   ├── devices/        # Equipos, tipos y marcas
│   ├── repairs/        # Reparaciones e historial
│   └── finances/       # Ingresos, gastos y facturación
├── config/             # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/             # Archivos estáticos (CSS, JS, imágenes, vendor)
├── templates/          # Plantillas HTML
├── manage.py
├── requirements.txt
└── .env                # Variables de entorno (NO se sube a Git)
```

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL 13 o superior
- Git
- pip (incluido con Python)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/giulianarojas/sistema_reparaciones.git
cd sistema_reparaciones
```

### 2. Crear y activar un entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos PostgreSQL

El proyecto está configurado para usar PostgreSQL con el usuario `postgres`. Crea la base de datos:

```sql
CREATE DATABASE sistema_reparaciones_db;
```

> ⚠️ **Nota:** Asegúrate de que PostgreSQL esté instalado y que el usuario `postgres` tenga acceso. Si necesitas configurar un usuario diferente, modifica `config/settings.py` (líneas 85-94).

### 5. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
SECRET_KEY=tu_clave_secreta_aqui
DB_PASSWORD=tu_password_postgres
```

Las variables requeridas son:
- `SECRET_KEY`: Clave secreta de Django (obligatoria)
- `DB_PASSWORD`: Contraseña del usuario `postgres` de PostgreSQL (obligatoria)

💡 Para generar una `SECRET_KEY` nueva puedes usar:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Aplicar las migraciones

```bash
python manage.py migrate
```

### 7. Crear un superusuario (para acceder al admin)

```bash
python manage.py createsuperuser
```

### 8. Levantar el servidor

```bash
python manage.py runserver
```

Abre tu navegador en http://127.0.0.1:8000 y listo.

El panel de administración de Django está en http://127.0.0.1:8000/admin.

## Uso

1. **Iniciar sesión:** Accede a http://127.0.0.1:8000 e inicia sesión con el superusuario creado.
2. **Dashboard:** La página principal muestra métricas generales (facturación total, equipos pendientes/terminados, límite de facturación monotributo).
3. **Secciones disponibles:**
   - **Reparaciones:** Crear, listar, actualizar estado, registrar pagos y ver historial.
   - **Clientes:** Alta, búsqueda y detalle de clientes.
   - **Equipos:** Alta, búsqueda y detalle (con tipo y marca).
   - **Finanzas:** Gestión de ingresos, gastos y control del límite de facturación monotributo.
4. **Base de conocimiento:** Al crear una nueva reparación, el sistema sugiere reparaciones previas similares basándose en el historial.
5. **Panel de administración:** Accede a http://127.0.0.1:8000/admin para gestión directa de modelos.

## Comandos útiles

```bash
# Crear migraciones después de modificar modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Abrir shell de Django
python manage.py shell

# Recolectar archivos estáticos (para producción)
python manage.py collectstatic
```

## Solución de problemas

### Error de conexión a PostgreSQL

Si obtienes un error de conexión a la base de datos:
- Verifica que PostgreSQL esté ejecutándose
- Confirma que el usuario `postgres` existe y tiene la contraseña correcta en `.env`
- Asegúrate de que la base de datos `sistema_reparaciones_db` existe

### Error de SECRET_KEY

Si el proyecto no inicia porque falta `SECRET_KEY`:
- Asegúrate de crear el archivo `.env` en la raíz del proyecto
- Genera una clave nueva con el comando indicado en la sección de instalación


## Autora

Giuliana Rojas — @giulianarojas
