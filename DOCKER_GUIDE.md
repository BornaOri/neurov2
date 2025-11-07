# Docker Guide for NeuROV2

Complete guide to using NeuROV2 in Docker - no manual installation required!

## Prerequisites

### Install Docker

#### Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Install and restart your computer
3. Open Docker Desktop and wait for it to start

#### Mac
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Install and start Docker Desktop

#### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in

# Install docker-compose
sudo apt-get install docker-compose
```

### Verify Docker Installation
```bash
docker --version
docker-compose --version
```

---

## Quick Start (3 Steps!)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd neurov2
```

### 2. Build Docker Image
```bash
# Windows
docker-run.bat build

# Linux/Mac
chmod +x docker-run.sh
./docker-run.sh build
```

This will:
- Download Python 3.11
- Compile NEURON from source
- Install all dependencies
- Compile the mechanism files
- Set up the environment

**First build takes ~10-15 minutes** (only once!)

### 3. Test Installation
```bash
# Windows
docker-run.bat test

# Linux/Mac
./docker-run.sh test
```

You should see:
```
Python version: 3.11.x
NEURON version: 8.2.4
✓ NEURON is working!
```

---

## Usage

### Interactive Shell

Get a bash shell inside the container:

```bash
# Windows
docker-run.bat bash

# Linux/Mac
./docker-run.sh bash
```

Once inside, you can run any Python commands:
```bash
python -m simulations.run_simulation --n-cells 500 --duration 1000
python -m analysis.basic_analysis results/baseline_500cells.h5
```

### Run Simulations

#### Small test simulation (500 cells, 1 second):
```bash
# Windows
docker-run.bat simulate

# Linux/Mac
./docker-run.sh simulate
```

#### Custom simulation:
```bash
# Syntax: simulate [n_cells] [duration_ms]

# Windows
docker-run.bat simulate 1000 2000

# Linux/Mac
./docker-run.sh simulate 1000 2000
```

Results are saved to `./results/` on your host machine.

### Analyze Results

```bash
# Windows
docker-run.bat analyze results/baseline_500cells.h5

# Linux/Mac
./docker-run.sh analyze results/baseline_500cells.h5
```

### Jupyter Notebooks (Interactive Analysis)

Start Jupyter server:
```bash
# Windows
docker-run.bat jupyter

# Linux/Mac
./docker-run.sh jupyter
```

Then open browser to: **http://localhost:8888**

The example notebook is at: `notebooks/example_simulation.ipynb`

---

## Advanced Usage

### Running Custom Python Scripts

Create your script in the project directory, then:

```bash
# Windows
docker-compose run --rm neurov2 python your_script.py

# Linux/Mac
docker-compose run --rm neurov2 python your_script.py
```

### Accessing Python Shell

```bash
docker-compose run --rm neurov2 python
```

```python
>>> from neuron import h
>>> from network.build_network import build_l23_network
>>> network = build_l23_network(n_cells=100)
>>> # ... continue working
```

### Using Docker Compose Directly

```bash
# Build
docker-compose build

# Run simulation service
docker-compose run --rm neurov2 python -m simulations.run_simulation --n-cells 1000

# Start Jupyter
docker-compose up jupyter

# Stop all services
docker-compose down
```

### Mounting Additional Directories

Edit `docker-compose.yml` to add volumes:

```yaml
volumes:
  - ./results:/app/results
  - ./data:/app/data
  - ./my_scripts:/app/my_scripts  # Add this
```

---

## Example Workflows

### 1. Basic Simulation

```bash
# Build image (first time only)
./docker-run.sh build

# Run simulation
./docker-run.sh simulate 500 1000

# Analyze results
./docker-run.sh analyze results/baseline_500cells.h5
```

### 2. Cancer Study

```bash
# Interactive shell
./docker-run.sh bash

# Inside container:
python
```

```python
from network.build_network import build_l23_network
from simulations.run_simulation import run_baseline_simulation

# Control network
control = build_l23_network(n_cells=1000, seed=42)
run_baseline_simulation(control, duration=2000, output_file="results/control.h5")

# Cancer network
cancer = build_l23_network(n_cells=1000, seed=42)

# Apply modifications
for cell in cancer.cells:
    for sec in cell.all_sections:
        if hasattr(sec, 'gbar_nav16'):
            sec.gbar_nav16 *= 1.3  # Increase Nav

run_baseline_simulation(cancer, duration=2000, output_file="results/cancer.h5")
```

Exit container (`Ctrl+D`), then analyze:

```bash
./docker-run.sh analyze results/control.h5
./docker-run.sh analyze results/cancer.h5
```

### 3. Interactive Analysis with Jupyter

```bash
# Start Jupyter
./docker-run.sh jupyter

# Open http://localhost:8888 in browser
# Open: notebooks/example_simulation.ipynb
# Run all cells (Cell -> Run All)
```

---

## File Persistence

### What Gets Saved

These directories are **mounted** from your host machine:
- `./results/` - Simulation outputs (.h5 files)
- `./data/` - Input data
- `./morphologies/` - Neuron morphology files
- `./notebooks/` - Jupyter notebooks

Changes in these directories persist after container stops.

### What Doesn't Get Saved

Everything else inside the container is temporary. To save modifications:
1. Edit files on your host machine (they're mounted into container)
2. Or copy files out: `docker cp neurov2_simulation:/app/file.py ./`

---

## Troubleshooting

### Docker not found
```bash
# Install Docker Desktop from docker.com
# Make sure Docker Desktop is running
```

### Permission denied (Linux)
```bash
# Add your user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

### Port 8888 already in use (Jupyter)
```bash
# Stop other Jupyter instances
# Or edit docker-compose.yml to use different port:
ports:
  - "8889:8888"  # Use port 8889 on host
```

### Container won't start
```bash
# Check Docker logs
docker-compose logs neurov2

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
```

### Slow simulation
```bash
# Edit docker-compose.yml to allocate more resources:
deploy:
  resources:
    limits:
      cpus: '8'      # Increase CPUs
      memory: 16G    # Increase memory
```

### Compilation errors
```bash
# Rebuild image from scratch
docker-compose build --no-cache neurov2
```

### Results not showing up
```bash
# Make sure results directory exists
mkdir -p results

# Check that volumes are mounted
docker-compose run --rm neurov2 ls -la /app/results
```

---

## Performance Tips

### Resource Allocation

Edit `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '8'        # Use more CPU cores
      memory: 16G      # Use more RAM
```

### Simulation Size

Start small, scale up:
- **Testing**: 100-500 cells
- **Development**: 500-1000 cells
- **Production**: 2000-5000 cells

### Parallel Simulations

Run multiple containers:

```bash
# Terminal 1
docker-compose run --rm neurov2 python -m simulations.run_simulation --n-cells 1000 --seed 1

# Terminal 2
docker-compose run --rm neurov2 python -m simulations.run_simulation --n-cells 1000 --seed 2
```

---

## Updating the Project

```bash
# Pull latest changes
git pull origin main

# Rebuild Docker image
docker-compose build neurov2

# Or rebuild from scratch
docker-compose build --no-cache neurov2
```

---

## Cleaning Up

### Remove containers
```bash
docker-compose down
```

### Remove image (frees ~2GB)
```bash
docker rmi neurov2:latest
```

### Remove all Docker data (nuclear option)
```bash
docker system prune -a
# Warning: removes ALL unused images and containers
```

---

## Docker Commands Cheat Sheet

```bash
# Build image
docker-compose build

# Run simulation
docker-compose run --rm neurov2 [command]

# Interactive shell
docker-compose run --rm neurov2 bash

# Start Jupyter
docker-compose up jupyter

# Stop all services
docker-compose down

# View logs
docker-compose logs

# List running containers
docker ps

# List images
docker images

# Remove container
docker rm [container_id]

# Remove image
docker rmi [image_id]
```

---

## Getting Help

### Inside Container

```bash
# Get into container
./docker-run.sh bash

# Python help
python -c "from network.build_network import build_l23_network; help(build_l23_network)"

# List available scripts
ls simulations/
ls analysis/
```

### Check Installation

```bash
./docker-run.sh test
```

### View Logs

```bash
docker-compose logs neurov2
```

---

## Next Steps

1. ✅ **Test installation**: `./docker-run.sh test`
2. ✅ **Run first simulation**: `./docker-run.sh simulate 500 1000`
3. ✅ **Analyze results**: `./docker-run.sh analyze results/baseline_500cells.h5`
4. ✅ **Try Jupyter**: `./docker-run.sh jupyter`
5. ✅ **Read docs**: Check `docs/QUICKSTART.md` and `docs/CANCER_MODIFICATIONS.md`

**You're ready to simulate! No manual installation needed.** 🎉
