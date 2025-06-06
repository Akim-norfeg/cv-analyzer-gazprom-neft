FROM python:3.10-slim

# ставим зависимости
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir psycopg2-binary

# копируем всё приложение
COPY . /app

# переменные окружения Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_THEME_BASE="light"

ENV STREAMLIT_SERVER_MAXUPLOADSIZE=10

EXPOSE 8501

# команда запуска
CMD ["streamlit", "run", "app.py"]
