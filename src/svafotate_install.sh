#!/usr/bin/env bash


env_exists() {
    local env_name="$1"
    conda env list | grep -q "^${env_name} " && return 0 || return 1
}

create_env() {
    local env_name="$1"
    if env_exists "$env_name"; then
        echo "Conda environment '$env_name' already exists."
    else
        echo "Creating conda environment '$env_name'"
        conda create --name "$env_name" python=3 -y
    fi
}


echo "Creating conda environment for SVAFotate"
create_env "svafotate-env"

echo "Initializing conda for bash shell"
eval "$(conda shell.bash hook)"

echo "Activating svafotate-env"
conda activate svafotate-env

# verify activation
if [[ "$CONDA_DEFAULT_ENV" == "svafotate-env" ]]; then
    echo "Activated svafotate-env successfully."
else
    echo "Failed to activate svafotate-env."
    exit 1
fi

echo "Installing dependencies from requirements.txt"
conda install --file https://raw.githubusercontent.com/fakedrtom/SVAFotate/master/requirements.txt

echo "Installing SVAFotate from GitHub repository"
pip install git+https://github.com/fakedrtom/SVAFotate.git

echo "Checking that SVAFotate installed Correctly"
svafotate --version
if [ $? -eq 0 ]; then
    echo "SVAFotate installed successfully!"
else
    echo "SVAFotate installation failed."
fi
