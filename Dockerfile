# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies required for building kissat and sbva
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    cmake \
    clang \
    && rm -rf /var/lib/apt/lists/*

# Clone and build Kissat from source
RUN git clone https://github.com/arminbiere/kissat.git /app/kissat \
    && cd /app/kissat \
    && ./configure \
    && make

# Setup SBVA: Assuming you need to download Eigen and compile SBVA from source
RUN git clone https://github.com/hgarrereyn/SBVA.git /app/SBVA \
    && cd /app/SBVA \
    && curl -L https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz -o /app/SBVA/eigen-3.4.0.tar.gz \
    && tar -xzf /app/SBVA/eigen-3.4.0.tar.gz \
    && make

# Expose the port the app runs on
EXPOSE 8501

# Set env variables
ENV PORT=8501
ENV HOST=0.0.0.0


# Run app.py when the container launches
CMD streamlit run app.py --server.port $PORT --server.address $HOST

