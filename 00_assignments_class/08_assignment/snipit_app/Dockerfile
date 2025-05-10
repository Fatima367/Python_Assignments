FROM python:3.11-slim
WORKDIR /app
# Update pip to avoid version issues
RUN pip install --upgrade pip
COPY 00_assignments_class/08_assignment/snipit_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY 00_assignments_class/08_assignment/snipit_app .
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]