# ---- Builder Stage ----
# Use a slim Python image to build our dependencies into "wheels"
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies and build them into wheels
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# ---- Final Stage ----
# Use the same slim Python image for a small final image size
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user for better security
RUN addgroup --system app && adduser --system --group app

# Copy the pre-built wheels and requirements from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the dependencies from the local wheels
RUN pip install --no-cache /wheels/*

# --- CHANGE HERE: Correctly copy the nested 'app' directory ---
COPY ./app /app/app

# Change ownership of the app directory to our non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port the app runs on
EXPOSE 8001

# --- CHANGE HERE: Use the correct module path to run the app ---
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]