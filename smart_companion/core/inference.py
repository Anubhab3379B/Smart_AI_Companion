import os
from typing import Optional, Dict, Any, Generator
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

class ModelManager:
    """
    Manages the lifecycle and inference of the local LLM using llama.cpp.
    """
    def __init__(self, model_path: str, n_ctx: int = 2048, n_gpu_layers: int = 0):
        """
        Initialize the ModelManager.

        Args:
            model_path (str): Absolute path to the .gguf model file.
            n_ctx (int): Context window size.
            n_gpu_layers (int): Number of layers to offload to GPU. Set to -1 for all.
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        self.llm: Optional[Llama] = None

        if not Llama:
             raise ImportError("llama-cpp-python is not installed. Please install it with `pip install llama-cpp-python`.")

    def load_model(self) -> None:
        """
        Loads the model into memory.
        """
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")
        
        print(f"Loading model from {self.model_path}...")
        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_gpu_layers=self.n_gpu_layers,
                verbose=False
            )
            print("Model loaded successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def generate(self, prompt: str, max_tokens: int = 128, stop: list = ["User:", "\n\n"], temperature: float = 0.7) -> str:
        """
        Generates text based on the prompt.

        Args:
            prompt (str): The input prompt.
            max_tokens (int): Maximum number of tokens to generate.
            stop (list): List of stop sequences.
            temperature (float): Sampling temperature.

        Returns:
            str: The generated text.
        """
        if not self.llm:
            self.load_model()
        
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            stop=stop,
            temperature=temperature,
            echo=False
        )
        return output['choices'][0]['text']

    def stream_generate(self, prompt: str, max_tokens: int = 128, stop: list = ["User:", "\n\n"], temperature: float = 0.7) -> Generator[str, None, None]:
        """
        Streams generated text.

        Args:
            prompt (str): The input prompt.
            max_tokens (int): Maximum number of tokens to generate.
            stop (list): List of stop sequences.
            temperature (float): Sampling temperature.

        Yields:
            str: Chunks of generated text.
        """
        if not self.llm:
            self.load_model()

        stream = self.llm(
            prompt,
            max_tokens=max_tokens,
            stop=stop,
            temperature=temperature,
            stream=True,
            echo=False
        )
        for output in stream:
            yield output['choices'][0]['text']

if __name__ == "__main__":
    # Example usage (requires a valid model path)
    # manager = ModelManager("path/to/model.gguf")
    # print(manager.generate("Hello, how are you?"))
    pass
