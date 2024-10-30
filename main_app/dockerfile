# Use the official Alpine Linux image
FROM python:3.9-alpine

# Install tini
RUN apk add --no-cache tini

# Set tini as the init system
ENTRYPOINT ["/sbin/tini", "--"]

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the image
COPY . .

# Command to run the application
CMD ["python", "main.py"]
