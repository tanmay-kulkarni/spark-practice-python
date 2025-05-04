# Spark Docker Justfile - Simplified Working Version

sparkImage := "bitnami/spark:latest"
pythonFile := "spark-app.py"

# Show available commands
default:
    @echo "Available commands:"
    @echo "  just run         - Run Spark locally (recommended method)"
    @echo "  just clean       - Clean output directory"

# Clean outputs
clean:
    @echo "Cleaning output directory..."
    -rm -rf output/*
    @echo "✓ Cleaned"

# Run Spark job locally (most reliable approach)
run:
    @echo "Running Spark job locally..."
    mkdir -p output
    chmod 777 output
    docker run --rm \
        -v "$(pwd)/src:/app" \
        -v "$(pwd)/output:/output" \
        {{sparkImage}} \
        spark-submit --master local[*] /app/{{pythonFile}}
    @echo "✓ Job completed. Results in the output directory."

