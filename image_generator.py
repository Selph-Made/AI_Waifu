# /image_generator.py
import torch
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
from PIL import Image
import os
from datetime import datetime
from database import DatabaseManager
import json

class ImageGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {
            "stable_diffusion": self._load_sd_model(),
            "waifu_diffusion": self._load_wd_model()
        }
        self.output_dir = "generated_images"
        self.db = DatabaseManager()
        os.makedirs(self.output_dir, exist_ok=True)

    def _load_sd_model(self):
        return StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float16,
            safety_checker=None,
            requires_safety_checker=False
        ).to(self.device)

    def _load_wd_model(self):
        pipe = StableDiffusionPipeline.from_pretrained(
            "hakurei/waifu-diffusion",
            torch_dtype=torch.float16
        )
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
        return pipe.to(self.device)

    def generate_image(self, prompt, negative_prompt="", model_name="stable_diffusion", 
                      steps=30, cfg_scale=7.5, width=512, height=512, seed=None):
        # Validate input
        if model_name not in self.models:
            raise ValueError(f"Invalid model name: {model_name}")
        if steps < 1 or steps > 100:
            raise ValueError("Steps must be between 1-100")
        
        # Set up generator
        generator = torch.Generator(self.device)
        if seed is None:
            seed = generator.seed()
        generator = generator.manual_seed(seed)
        
        # Generate image
        pipe = self.models[model_name]
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=int(steps),
            guidance_scale=cfg_scale,
            width=width,
            height=height,
            generator=generator
        ).images[0]
        
        # Save and log
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}_{hash(prompt) % 1000}.png"
        path = os.path.join(self.output_dir, filename)
        image.save(path)
        
        # Store metadata
        self.db.conn.cursor().execute('''
            INSERT INTO generated_images 
            (prompt, negative_prompt, model, parameters, path, created_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            prompt,
            negative_prompt,
            model_name,
            json.dumps({
                "steps": steps,
                "cfg_scale": cfg_scale,
                "width": width,
                "height": height,
                "seed": seed
            }),
            path
        ))
        self.db.conn.commit()
        
        return image, path

    def get_generation_history(self, limit=10):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT prompt, model, path, created_at 
            FROM generated_images 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

if __name__ == "__main__":
    # Test generation
    ig = ImageGenerator()
    test_image, path = ig.generate_image(
        "A cybernetic warrior in a neon-lit cityscape",
        model_name="waifu_diffusion",
        steps=25
    )
    print(f"Generated test image saved to: {path}")

