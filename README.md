# Spark Practice Project

A simple project for practicing Apache Spark (PySpark) locally.

## Setup

This project uses Docker to run Spark applications in a local environment. No Spark installation required.

### Prerequisites

- Docker
- Just command runner (`brew install just` on macOS)

## Project Structure

```
spark-practice-python/
├── Justfile        # Commands for running Spark applications
├── output/         # CSV output from Spark applications (auto-created)
└── src/            # Spark Python scripts
    ├── spark-app.py              # Main Spark application
    └── eda/
        └── simple_analysis.py    # Example EDA script
```

## Usage

List available scripts:
```bash
just list
```

Run a specific Spark script:
```bash
just run spark-app.py
```

Or run a script in a subdirectory:
```bash
just run eda/simple_analysis.py
```

View output from a script:
```bash
just view spark-app.py
```

Clean all output directories:
```bash
just clean
```

## Adding New Scripts

Create new Python scripts in the `src` directory. Each script should:

1. Create a Spark session
2. Perform data processing
3. Save results to `/output/` directory (this will map to `output/{script_path}/` on your host)

CSV output files from each script are automatically saved to a directory matching the script's path.

## Docker Details

The project uses the `bitnami/spark:latest` Docker image which includes:
- Spark with local execution mode
- Python with PySpark

No need to build custom images for basic Spark exploration.

## Examples

The project includes sample scripts:
- `src/spark-app.py`: Basic Spark operations with random data
- `src/eda/simple_analysis.py`: Simple exploratory data analysis