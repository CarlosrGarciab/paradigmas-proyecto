@echo off
echo ==========================================
echo      TODO APP - SCRIPT DE INICIALIZACION
echo ==========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado...
echo.

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo Entorno virtual creado exitosamente.
    echo.
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo Dependencias instaladas exitosamente.
echo.

REM Verificar si existe archivo .env
if not exist ".env" (
    echo Creando archivo de configuración .env...
    echo SECRET_KEY=tu-clave-secreta-super-segura > .env
    echo DATABASE_URL=sqlite:///todo_app.db >> .env
    echo FLASK_ENV=development >> .env
    echo FLASK_DEBUG=True >> .env
    echo.
    echo Archivo .env creado. Puedes modificar la configuración si es necesario.
    echo.
)

REM Ejecutar la aplicación
echo ==========================================
echo      INICIANDO TODO APP
echo ==========================================
echo.
echo La aplicación estará disponible en:
echo http://localhost:5000
echo.
echo Presiona Ctrl+C para detener la aplicación
echo.

python app.py

pause