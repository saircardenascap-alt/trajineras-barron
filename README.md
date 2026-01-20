# Trajineras Barrón

Sistema de reservaciones para trajineras en Xochimilco.

## Deployment en Render

Esta aplicación está configurada para desplegarse en Render.

### Variables de Entorno Requeridas

- `PYTHON_VERSION`: 3.11.0
- `FLASK_ENV`: production (o development para modo debug)

### Comandos de Build

Build Command: `./build.sh`
Start Command: `gunicorn app:app`

## Desarrollo Local

```bash
pip install -r requirements.txt
python app.py
```

La aplicación estará disponible en http://localhost:5000
