from onnxruntime import InferenceSession
import onnxruntime as ort
from PIL import Image
import numpy as np
import csv
import os
from ...folder_path import get_root_folder_path

def get_tagging_model(model_name):
    return os.path.join(get_root_folder_path(),"models","tagger_models",f"{model_name}.onnx")

def ready_model(model_name):
    if model_name.endswith(".onnx"):
        model_name = model_name[0:-5]

    name = get_tagging_model(model_name)
    model = InferenceSession(name, providers=ort.get_available_providers())

    return model

async def do_tagging(image:Image.Image, model:InferenceSession, threshold=0.35, character_threshold=0.85, exclude_tags="", trigger_name=""):
    input = model.get_inputs()[0]
    height = input.shape[1]

    # Reduce to max size and pad with white
    ratio = float(height)/max(image.size)
    new_size = tuple([int(x*ratio) for x in image.size])
    image = image.resize(new_size, Image.LANCZOS)
    square = Image.new("RGB", (height, height), (255, 255, 255))
    square.paste(image, ((height-new_size[0])//2, (height-new_size[1])//2))

    image = np.array(square).astype(np.float32)
    image = image[:, :, ::-1]  # RGB -> BGR
    image = np.expand_dims(image, 0)

    # Read all tags from csv and locate start of each category
    tags = []
    general_index = None
    character_index = None
    with open(os.path.join(get_root_folder_path(),"models","tagger_models","tagger.csv")) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if general_index is None and row[2] == "0":
                general_index = reader.line_num - 2
            elif character_index is None and row[2] == "4":
                character_index = reader.line_num - 2
            tags.append(row[1])
    # with open(r"D:\ai\My_AI\dataset_edit\soyokaze_dataset_editor01\models\tagging\tags.txt") as f:
    #     for line in f:
    #         tags.append(line.replace("\n",""))

    label_name = model.get_outputs()[0].name
    probs = model.run([label_name], {input.name: image})[0]

    result = list(zip(tags, probs[0]))

    # rating = max(result[:general_index], key=lambda x: x[1])
    general = [item for item in result[general_index:character_index] if item[1] > threshold]
    character = [item for item in result[character_index:] if item[1] > character_threshold]

    all = character + general
    remove = [s.strip() for s in exclude_tags.lower().split(",")]
    all = [tag for tag in all if tag[0] not in remove]
    all.insert(0,[trigger_name]) if trigger_name != "" else print("No Trigger Word")

    res = ", ".join((item[0].replace("_"," ") for item in all))

    res = res.split(",")
    res = list(map(lambda word:word.strip(),res))

    return res