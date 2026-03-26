import os
import requests
from tqdm import tqdm

MODEL_URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
MODEL_FILENAME = "llama-2-7b-chat.Q4_K_M.gguf"
DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

def download_model():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
    
    dest_path = os.path.join(DEST_DIR, MODEL_FILENAME)
    if os.path.exists(dest_path):
        print(f"Model already exists at {dest_path}")
        return

    print(f"Downloading model to {dest_path}...")
    response = requests.get(MODEL_URL, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    
    with open(dest_path, 'wb') as f:
        for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB'):
            f.write(data)
    
    print("Download complete.")

if __name__ == "__main__":
    download_model()
