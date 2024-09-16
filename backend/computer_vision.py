from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import requests

def download_image(url):
    return Image.open(requests.get(url, stream=True).raw)

class VisionTransformer:
    def __init__(self, model_path):
        self.model = pipeline("image-classification", model=model_path)

    def classify(self, image: Image):
        return self.model(image)
    
class BLIPImageCaptioning:
    def __init__(self, model_path, max_length=300):
        self.max_length = max_length
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"BLIPImageCaptioning - Using device: {self.device}")

        self.processor = BlipProcessor.from_pretrained(model_path)
        self.model = BlipForConditionalGeneration.from_pretrained(model_path).to(self.device)

    def caption(self, image: Image):
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs, max_length=self.max_length)
        return self.processor.decode(out[0], skip_special_tokens=True)