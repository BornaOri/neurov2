from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="neurov2",
    version="0.1.0",
    author="NeuroV2 Team",
    description="Biorealistic L2/3 barrel cortex simulation for studying cancer effects on cortical dynamics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BornaOri/neurov2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "pandas>=1.3.0",
        "neuron>=8.0",
        "networkx>=2.6",
        "h5py>=3.0.0",
        "seaborn>=0.11.0",
        "tqdm>=4.62.0",
        "pyyaml>=5.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "ipython>=7.30.0",
            "jupyter>=1.0.0",
        ],
        "parallel": [
            "mpi4py>=3.1.0",
        ],
        "morphology": [
            "morph-tool>=2.9.0",
            "neurom>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "neurov2-run=simulations.run_simulation:main",
            "neurov2-analyze=analysis.analyze_results:main",
        ],
    },
)
