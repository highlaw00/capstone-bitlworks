# 이미지 로드
# 이미지 config 로드
# 이미지 config 참조하여 해당 이미지 crop
# crop한 이미지 저장

from PIL import Image
import json, os

def load_config(name):
    if name == "train":
        file_path = "image-process-scripts\\training_config.json"
    elif name == "valid":
        file_path = "image-process-scripts\\valid_config.json"
    try:
        with open(file_path, 'r') as file:
            data_dict = json.load(file)
        return data_dict
    except Exception as e:
        print("Error while loading text file.")
        print(e)
        return None
    
train_config = load_config("train")
valid_config = load_config("valid")


# 테스트: 이미지 하나 로드하여 특정 디렉토리에 저장하는 것 까지

def crop_and_save(img_root_dir, img_info, output_dir):
    path = img_root_dir + img_info["path"].replace("/", "\\")
    file_name = img_info["path"].split("/")[1]
    details = img_info["details"]
    try:
        image = Image.open(path)
        
        for idx, detail in enumerate(details.values()):
            x1, y1, h, w = map(int, (detail["x1"], detail["y1"], detail["h"], detail["w"]))
            if h*w < 400: continue
            detail_path = "occlusion" if detail["occlusion"] == "1" or detail["occlusion"] == "2" else "non-occlusion"
            result_path = output_dir + "\\" + detail_path
            sub_file_name = str(idx) + "_" + file_name
            crop_box = (x1, y1, x1 + w, y1 + h)
            cropped_image = image.crop(crop_box)
            
            output_path = os.path.join(result_path, sub_file_name)
            cropped_image.save(output_path)
    except Exception as e:
        print(e)
        print(img_info)
        
print("Crop with Train config")
TRAIN_IMAGE_DIR = "wider-dataset\\train\\images\\"
TRAIN_OUTPUT_DIR = "processed_img"
for img_name, img_info in train_config.items():
    crop_and_save(TRAIN_IMAGE_DIR, img_info, TRAIN_OUTPUT_DIR)

# print("Crop with Valid config")
# for img_name, img_info in valid_config.items():
#     crop_and_save(TRAIN_IMAGE_DIR, img_info, TRAIN_OUTPUT_DIR)