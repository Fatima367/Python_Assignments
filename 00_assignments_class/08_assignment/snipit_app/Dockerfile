FROM python:3.11-slim
WORKDIR /main
# Copy requirements.txt from subdirectory
RUN pip install uv
RUN uv pip install --system --no-cache-dir -r requirements.txt
# Copy the entire subdirectory
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
COPY requirements.txt .
COPY . .