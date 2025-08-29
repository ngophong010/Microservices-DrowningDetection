# ---- Builder Stage ----
# Use a slim Python image to build our dependencies into "wheels"
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Set an environment variable to prevent writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies and build them into wheels.
# This is the Python equivalent of Go's build step. It pre-compiles
# dependencies so the final stage is just a fast installation.
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# ---- Final Stage ----
# Use the same slim Python image for a small final image size
FROM python:3.11-slim

WORKDIR /app

# Set the same environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user for better security
# This is a best practice equivalent to using a distroless image
RUN addgroup --system app && adduser --system --group app

# Copy the pre-built wheels and requirements from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the dependencies from the local wheels.
# This is much faster than downloading and building from scratch.
RUN pip install --no-cache /wheels/*

# Copy the application source code
COPY ./app ./src/app

# Set the PYTHONPATH environment variable.
# This tells Python to ALSO look for modules inside the /app/src directory.
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# Change ownership of the app directory to our non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port the app runs on (FastAPI/Uvicorn default is 8000)
EXPOSE 8000

# The command to run our application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]