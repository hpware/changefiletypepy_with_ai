import requests

import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM 
import os
import yaml
import io
import logging

num = 1
output_dir = "output_yaml/"

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-large", torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large", trust_remote_code=True)

prompt = "<OD>"

url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"
image = Image.open(requests.get(url, stream=True).raw)

def processyaml(prompt, image, model, processor):
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)

    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        num_beams=3,
        do_sample=False
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

    parsed_answer = processor.post_process_generation(generated_text, task="<OD>", image_size=(image.width, image.height))

    return parsed_answer
data = [
    {
        "answer": parsed_answer
    }
]

newfile = str(num) + ".yaml"
output_p = os.path.join(output_dir, newfile)
with io.open(output_p, 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

