FROM python:3.11-slim
WORKDIR /app
# Copy requirements.txt from subdirectory
RUN pip install uv
RUN uv pip install --system --no-cache-dir -r requirements.txt
# Copy the entire subdirectory
COPY 00_assignments_class/08_assignment/snipit_app .
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
COPY requirements.txt .
COPY . .