# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install  -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 8432 available to the world outside this container
EXPOSE 8432

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "rest_api:app", "--host", "0.0.0.0", "--port", "8432", "--reload"]