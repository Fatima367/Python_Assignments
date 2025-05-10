FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv pip install -r requirements.txt

EXPOSE 8501
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]