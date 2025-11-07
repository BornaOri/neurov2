#!/bin/bash
# Helper script to run simulations in Docker
# Usage: ./docker-run.sh [command]

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  NeuROV2 Docker Runner${NC}"
echo -e "${BLUE}=====================================${NC}"

# Build image if it doesn't exist
if [[ "$(docker images -q neurov2:latest 2> /dev/null)" == "" ]]; then
    echo -e "${YELLOW}Building Docker image (first time only)...${NC}"
    docker-compose build neurov2
    echo -e "${GREEN}✓ Image built successfully${NC}"
fi

# Parse command
COMMAND=${1:-bash}

case $COMMAND in
    bash|shell)
        echo -e "${GREEN}Starting interactive shell...${NC}"
        docker-compose run --rm neurov2 bash
        ;;

    test)
        echo -e "${GREEN}Running installation test...${NC}"
        docker-compose run --rm neurov2 python -c "
from neuron import h
import sys
print('Python version:', sys.version)
print('NEURON version:', h.nrnversion())
print('✓ NEURON is working!')
"
        ;;

    simulate)
        N_CELLS=${2:-500}
        DURATION=${3:-1000}
        echo -e "${GREEN}Running simulation: $N_CELLS cells, $DURATION ms${NC}"
        docker-compose run --rm neurov2 python -m simulations.run_simulation \
            --n-cells $N_CELLS \
            --duration $DURATION \
            --background-rate 5.0 \
            --output results/baseline_${N_CELLS}cells.h5
        ;;

    analyze)
        RESULT_FILE=${2:-results/baseline_500cells.h5}
        echo -e "${GREEN}Analyzing results: $RESULT_FILE${NC}"
        docker-compose run --rm neurov2 python -m analysis.basic_analysis $RESULT_FILE
        ;;

    jupyter)
        echo -e "${GREEN}Starting Jupyter notebook server...${NC}"
        echo -e "${YELLOW}Access at: http://localhost:8888${NC}"
        docker-compose up jupyter
        ;;

    build)
        echo -e "${GREEN}Rebuilding Docker image...${NC}"
        docker-compose build --no-cache neurov2
        ;;

    clean)
        echo -e "${YELLOW}Cleaning up Docker resources...${NC}"
        docker-compose down
        docker rmi neurov2:latest 2>/dev/null || true
        echo -e "${GREEN}✓ Cleaned up${NC}"
        ;;

    help|*)
        echo ""
        echo "Usage: ./docker-run.sh [command] [options]"
        echo ""
        echo "Commands:"
        echo "  bash|shell              - Start interactive shell"
        echo "  test                    - Test NEURON installation"
        echo "  simulate [n] [dur]      - Run simulation (default: 500 cells, 1000ms)"
        echo "  analyze [file]          - Analyze results file"
        echo "  jupyter                 - Start Jupyter notebook server"
        echo "  build                   - Rebuild Docker image"
        echo "  clean                   - Remove Docker image and containers"
        echo "  help                    - Show this help"
        echo ""
        echo "Examples:"
        echo "  ./docker-run.sh test"
        echo "  ./docker-run.sh simulate 1000 2000"
        echo "  ./docker-run.sh analyze results/baseline_1000cells.h5"
        echo "  ./docker-run.sh jupyter"
        echo ""
        ;;
esac
