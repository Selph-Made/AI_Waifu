# /model_loader.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from llama_cpp import Llama
import os
from typing import Union
from dataclasses import dataclass

@dataclass
class ModelConfig:
    name: str
    path: str
    type: str  # "gguf" or "transformers"
    params: dict

class ModelLoader:
    def __init__(self):
        self.loaded_models = {}
        self.current_model = None
        self.model_configs = {
            "chat": ModelConfig(
                name="Mistral-7B-Instruct",
                path="gguf/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
                type="gguf",
                params={"n_ctx": 2048, "n_gpu_layers": 33}
            ),
            "image": ModelConfig(
                name="Stable-Diffusion",
                path="CompVis/stable-diffusion-v1-4",
                type="transformers",
                params={"variant": "fp16", "torch_dtype": torch.float16}
            )
        }

    def load_model(self, model_key: str) -> Union[Llama, AutoModelForCausalLM]:
        if model_key not in self.model_configs:
            raise ValueError(f"Unknown model key: {model_key}")
        
        config = self.model_configs[model_key]
        
        if config.type == "gguf":
            if not os.path.exists(config.path):
                raise FileNotFoundError(f"GGUF model not found at {config.path}")
            
            model = Llama(
                model_path=config.path,
                n_ctx=config.params["n_ctx"],
                n_gpu_layers=config.params["n_gpu_layers"],
                verbose=False
            )
        elif config.type == "transformers":
            model = AutoModelForCausalLM.from_pretrained(
                config.path,
                **config.params
            ).to("cuda" if torch.cuda.is_available() else "cpu")
        else:
            raise ValueError(f"Unsupported model type: {config.type}")
        
        self.loaded_models[model_key] = model
        self.current_model = model
        return model

    def unload_model(self, model_key: str):
        if model_key in self.loaded_models:
            del self.loaded_models[model_key]
            if self.current_model == model_key:
                self.current_model = None
            torch.cuda.empty_cache()

    def get_model(self, model_key: str):
        if model_key in self.loaded_models:
            return self.loaded_models[model_key]
        return self.load_model(model_key)

    def switch_model(self, model_key: str):
        if model_key not in self.model_configs:
            raise ValueError(f"Unknown model key: {model_key}")
        if model_key not in self.loaded_models:
            self.load_model(model_key)
        self.current_model = self.loaded_models[model_key]

    def list_available_models(self):
        return [
            {
                "name": config.name,
                "key": key,
                "type": config.type,
                "path": config.path,
                "loaded": key in self.loaded_models
            }
            for key, config in self.model_configs.items()
        ]

if __name__ == "__main__":
    # Test loading
    ml = ModelLoader()
    print("Available models:", ml.list_available_models())
    
    # Load chat model
    chat_model = ml.load_model("chat")
    print("Chat model loaded:", type(chat_model))
    
    # Load image model
    image_model = ml.load_model("image")
    print("Image model loaded:", type(image_model))

