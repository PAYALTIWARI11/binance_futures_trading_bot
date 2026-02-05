# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create a directory for logs
RUN mkdir -p logs

# Set environment variables (can be overridden at runtime)
ENV BINANCE_ENV=testnet
ENV PYTHONUNBUFFERED=1

# Run the bot in interactive mode by default 
# Or you can override the CMD to run specific orders
CMD ["python", "cli.py"]
