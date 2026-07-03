#!/bin/bash
# watchdog-auto-switch.sh

# ---- Configuration -----------------------------------------------------------
# Path to Hermes config file
HERMES_CONFIG="${HOME}/.hermes/config.yaml"

# Function to extract a value from the YAML config (simple grep + sed approach)
# Usage: get_config_value <key_path> where key_path is e.g. 'auxiliary.vision.model'
get_config_value() {
    local key_path=$1
    # Extract the line that starts with the key, then capture the value after ':'
    grep -E "^\s*${key_path}:\s*\"?([^\"]+)\"?\s*$" "${HERMES_CONFIG}" | \
        sed -E 's/^[[:space:]]*${key_path}:\s*\"?([^\"]+)\"?\s*$/\1/'
}

# ---- Health Check -----------------------------------------------------------
# Get the currently configured vision model
CURRENT_MODEL=$(get_config_value 'auxiliary.vision.model')

# If we couldn't parse the model, abort with an error
if [[ -z "${CURRENT_MODEL}" ]]; then
    echo "Failed to read auxiliary.vision.model from ${HERMES_CONFIG}"
    exit 1
fi

# Perform a lightweight health‑check request against the current model
if ! curl -s -X POST http://127.0.0.1:11434/api/generate \
      -d '{"model":"'"${CURRENT_MODEL}"'","prompt":"health-check","stream":false}' \
      | grep -q '"response"'; then
    echo "Vision model ${CURRENT_MODEL} failed health check."

    # ---- List of known free models in order of preference --------------------
    # NOTE: Adjust this list if new free models become available.
    FREE_MODELS=("llama3.2-vision:11b" "google/gemma-4-31b-it:free" "google/gemma-4-26b-a4b-it:free")

    # ---- Try each free model until one works ---------------------------------
    for MODEL in "${FREE_MODELS[@]}"; do
        # Quick health‑check for the candidate model
        if curl -s -X POST http://127.0.0.1:11434/api/generate \
              -d '{"model":"'"${MODEL}"'","prompt":"health-check","stream":false}' \
              | grep -q '"response"'; then
            # Switch to the working free model
            hermes config set auxiliary.vision.model "${MODEL}"
            # Restart the Hermes gateway service – must be done from an external process
            systemctl --user restart hermes-gateway.service
            echo "Automatically switched to free model ${MODEL}"
            # Verify that the restart succeeded and the new model passes health check
            if curl -s -X POST http://127.0.0.1:11434/api/generate \
                  -d '{"model":"'"${MODEL}"'","prompt":"health-check","stream":false}' \
                  | grep -q '"response"'; then
                echo "Switch to ${MODEL} confirmed successful."
                exit 0
            else
                echo "Health check failed after switching to ${MODEL}; continue trying next model."
                continue
            fi
        fi
    done

    # ---- If no free model succeeded, prompt the user -------------------------
    QUESTION="Current vision model is failing and no free model is available.
Would you like to switch to a paid model?"
    clarify --question "$${QUESTION}" --choices "Yes, switch to paid model" "No, abort"

    # If the user selects Yes, additional logic would invoke model‑switcher for a paid model.
fi