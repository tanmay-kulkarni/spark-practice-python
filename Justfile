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
    @mkdir -p "output/{{script}}"
    docker run --rm \
        -v "$(pwd)/src:/app" \
        -v "$(pwd)/output/{{script}}:/output" \
        {{sparkImage}} \
        spark-submit --master local[*] /app/{{script}}
    @echo "✓ Job completed. Results in output/{{script}}/"

# Clean all output directories
clean:
    @echo "Cleaning output directories..."
    -rm -rf output/*
    @echo "✓ Cleaned"

# Show contents of an output directory
view script:
    @if [ -d "output/{{script}}" ]; then \
        echo "Contents of output/{{script}}:"; \
        find "output/{{script}}" -name "*.csv" | while read file; do \
            echo "\n--- $(basename "$file") ---"; \
            head -10 "$file" | column -t -s,; \
            echo "..."; \
        done; \
    else \
        echo "No output found for {{script}}. Run 'just run {{script}}' first."; \
    fi