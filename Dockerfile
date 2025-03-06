# Use official Python image as base
FROM python:3.11

# Set environment variables to prevent .pyc files and enable unbuffered logs
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Verify if manage.py exists (for debugging)
RUN ls -la /app

# Run makemigrations (but not push migrations)
RUN python manage.py makemigrations || echo "Skipping makemigrations (no DB configured)"
RUN python manage.py migrate || echo "Skipping makemigrations (no DB configured)"

# Expose port for Django
EXPOSE 8000

# Start the Django development server
CMD ["python", "meeting_config/manage.py", "runserver", "0.0.0.0:8002"]
