# Multi-stage build for L2/3 Barrel Cortex Simulation
# Author: NeuroV2 Project
# Date: 2025

FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libncurses5-dev \
    libreadline-dev \
    libx11-dev \
    libxt-dev \
    bison \
    flex \
    automake \
    libtool \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install NEURON from source for better compatibility
WORKDIR /tmp
RUN wget https://github.com/neuronsimulator/nrn/releases/download/8.2.4/nrn-8.2.4.tar.gz && \
    tar xzf nrn-8.2.4.tar.gz && \
    cd nrn-8.2.4 && \
    mkdir build && cd build && \
    cmake .. \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DNRN_ENABLE_INTERVIEWS=OFF \
        -DNRN_ENABLE_MPI=OFF \
        -DNRN_ENABLE_RX3D=OFF \
        -DNRN_ENABLE_PYTHON=ON \
        -DPYTHON_EXECUTABLE=/usr/local/bin/python && \
    make -j$(nproc) && \
    make install && \
    cd / && rm -rf /tmp/nrn-8.2.4*

# Final stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libncurses5 \
    libreadline8 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Copy NEURON from builder
COPY --from=builder /usr/local /usr/local

# Set up environment
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages:$PYTHONPATH
ENV PATH=/usr/local/bin:$PATH

# Create working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir jupyter ipykernel ipywidgets

# Copy project files
COPY . .

# Compile NEURON mechanisms
RUN cd mechanisms && nrnivmodl && cd ..

# Install the package
RUN pip install -e .

# Create directories for outputs
RUN mkdir -p results data/experimental morphologies

# Set up Jupyter
RUN python -m ipykernel install --user --name=neurov2

# Default command
CMD ["bash"]

# Expose Jupyter port
EXPOSE 8888

# Add labels
LABEL maintainer="NeuroV2 Team"
LABEL description="Biorealistic L2/3 Barrel Cortex Simulation"
LABEL version="0.1.0"
