@echo off
REM Helper script to run simulations in Docker on Windows
REM Usage: docker-run.bat [command]

setlocal enabledelayedexpansion

echo =====================================
echo   NeuROV2 Docker Runner (Windows)
echo =====================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Build image if it doesn't exist
docker images neurov2:latest 2>nul | find "neurov2" >nul
if errorlevel 1 (
    echo Building Docker image (first time only)...
    docker-compose build neurov2
    echo Image built successfully!
    echo.
)

REM Parse command
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=help

if "%COMMAND%"=="bash" goto bash
if "%COMMAND%"=="shell" goto bash
if "%COMMAND%"=="test" goto test
if "%COMMAND%"=="simulate" goto simulate
if "%COMMAND%"=="analyze" goto analyze
if "%COMMAND%"=="jupyter" goto jupyter
if "%COMMAND%"=="build" goto build
if "%COMMAND%"=="clean" goto clean
if "%COMMAND%"=="help" goto help
goto help

:bash
echo Starting interactive shell...
docker-compose run --rm neurov2 bash
goto end

:test
echo Running installation test...
docker-compose run --rm neurov2 python -c "from neuron import h; import sys; print('Python:', sys.version); print('NEURON:', h.nrnversion()); print('OK: NEURON is working!')"
goto end

:simulate
set N_CELLS=%2
set DURATION=%3
if "%N_CELLS%"=="" set N_CELLS=500
if "%DURATION%"=="" set DURATION=1000
echo Running simulation: %N_CELLS% cells, %DURATION% ms
docker-compose run --rm neurov2 python -m simulations.run_simulation --n-cells %N_CELLS% --duration %DURATION% --background-rate 5.0 --output results/baseline_%N_CELLS%cells.h5
goto end

:analyze
set RESULT_FILE=%2
if "%RESULT_FILE%"=="" set RESULT_FILE=results/baseline_500cells.h5
echo Analyzing results: %RESULT_FILE%
docker-compose run --rm neurov2 python -m analysis.basic_analysis %RESULT_FILE%
goto end

:jupyter
echo Starting Jupyter notebook server...
echo Access at: http://localhost:8888
echo.
docker-compose up jupyter
goto end

:build
echo Rebuilding Docker image...
docker-compose build --no-cache neurov2
goto end

:clean
echo Cleaning up Docker resources...
docker-compose down
docker rmi neurov2:latest 2>nul
echo Cleaned up!
goto end

:help
echo.
echo Usage: docker-run.bat [command] [options]
echo.
echo Commands:
echo   bash^|shell              - Start interactive shell
echo   test                    - Test NEURON installation
echo   simulate [n] [dur]      - Run simulation (default: 500 cells, 1000ms)
echo   analyze [file]          - Analyze results file
echo   jupyter                 - Start Jupyter notebook server
echo   build                   - Rebuild Docker image
echo   clean                   - Remove Docker image and containers
echo   help                    - Show this help
echo.
echo Examples:
echo   docker-run.bat test
echo   docker-run.bat simulate 1000 2000
echo   docker-run.bat analyze results/baseline_1000cells.h5
echo   docker-run.bat jupyter
echo.

:end
endlocal
