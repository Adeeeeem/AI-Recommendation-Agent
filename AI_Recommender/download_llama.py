"""
download_llama.py

This script downloads the Meta LLaMA 2 model from Hugging Face
and saves it locally into the folder: "models/llama".
"""

# Import the snapshot_download function from huggingface_hub
# - This function lets us download an entire repository (a model in this case)
#   from the Hugging Face Hub, including all model weights, config files, and tokenizer.
from huggingface_hub import snapshot_download

# Download the LLaMA 2 7B model from Hugging Face
# - repo_id: the exact name of the model on Hugging Face Hub
# - local_dir: the destination folder where files will be stored locally
# 
snapshot_download(
	repo_id="meta-llama/Llama-2-7b-hf",  # Model repository ID
	local_dir="models/llama"             # Local folder where files will be saved
)
