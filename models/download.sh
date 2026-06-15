#!/bin/bash
# Digital Twin Model Download Helper
# Usage: bash models/download.sh [model_name|--list|--all]

MODELS_DIR="$(dirname "$0")"
CONFIG="$MODELS_DIR/config.yaml"

list_models() {
    echo "Available models:"
    grep "^  - name:" "$CONFIG" | sed 's/.*name: //'
}

download_model() {
    local name="$1"
    echo "Downloading $name via Ollama..."
    ollama pull "$name"
}

case "${1:-}" in
    --list|-l) list_models ;;
    --all|-a)
        grep "^  - name:" "$CONFIG" | sed 's/.*name: //' | while read -r model; do
            download_model "$model"
        done
        ;;
    *) 
        if [ -n "$1" ]; then
            download_model "$1"
        else
            echo "Usage: $0 [model_name|--list|--all]"
            list_models
        fi
        ;;
esac
