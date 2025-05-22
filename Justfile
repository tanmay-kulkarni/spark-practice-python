# Spark Justfile for Multiple Scripts

sparkImage := "bitnami/spark:latest"

# Show available commands
default:
    @echo "Available commands:"
    @echo "  just list        - List available Spark scripts"
    @echo "  just run SCRIPT  - Run a specific script (e.g., just run spark-app.py)"
    @echo "  just clean       - Clean all output directories"

# List available scripts
list:
    @echo "Available Spark scripts:"
    @find src -name "*.py" | sort

# Run a specific Spark script
run script:
    @echo "Running {{script}}..."
    @basename="$(basename "{{script}}" .py)" && \
    mkdir -p "output/$basename" && \
    docker run --rm \
        -v "$(pwd)/src:/app" \
        -v "$(pwd)/data:/data" \
        -v "$(pwd)/output/$basename:/output" \
        {{sparkImage}} \
        spark-submit --master local[*] /app/{{script}} && \
    echo "✓ Job completed. Results in output/$basename/"

# Clean all output directories
clean:
    @echo "Cleaning output directories..."
    -rm -rf output/*
    @echo "✓ Cleaned"

# Show contents of an output directory
view script:
    @basename="$(basename "{{script}}" .py)" && \
    if [ -d "output/$basename" ]; then \
        echo "Contents of output/$basename:"; \
        find "output/$basename" -name "*.csv" | while read file; do \
            echo "\n--- $(basename "$file") ---"; \
            head -10 "$file" | column -t -s,; \
            echo "..."; \
        done; \
    else \
        echo "No output found for $basename. Run 'just run {{script}}' first."; \
    fi