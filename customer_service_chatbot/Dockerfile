# Use Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

ENV PYTHONPATH=/app

# Install dependencies globally (no venv!)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]