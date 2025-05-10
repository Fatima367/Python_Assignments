FROM python:3.11-slim
WORKDIR /app
# Update pip and install uv
RUN pip install --upgrade pip
RUN pip install uv
# Copy requirements.txt from subdirectory
COPY 00_assignments_class/08_assignment/snipit_app/requirements.txt .
# Install dependencies with uv, using --system to avoid virtual environment
RUN uv pip install --system --no-cache-dir -r requirements.txt
# Copy the entire subdirectory
COPY 00_assignments_class/08_assignment/snipit_app .
EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]