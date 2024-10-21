# Use the official Ubuntu 22.04 image as the base
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install required packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev libmysqlclient-dev default-mysql-client && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY data_gen.py /app/

# Install the required Python packages
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Set the entrypoint for the container
ENTRYPOINT ["python3", "data_gen.py"]