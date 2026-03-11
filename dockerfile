FROM python:3.14-slim

WORKDIR /app

# instalar uv una sola vez
RUN pip install --no-cache-dir uv

# copiar dependencias
COPY pyproject.toml uv.lock* ./

# instalar dependencias declaradas en uv.lock
RUN uv sync --frozen

# copiar código de la app
COPY app ./app

EXPOSE 8000

# ejecutar uvicorn usando uv
CMD ["uv", "run", "uvicorn", "app.asgi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]