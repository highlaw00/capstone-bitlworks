# train config location: (/wider-dataset-config/wider_face_train_bbx_gt.txt)
# train image location: (/wider-dataset/train/images/X--XXXX)

# config format
# file name example: "X--XXXX/image_name.jpg"
# bounding box number
# x1, y1, w, h, blur, expression, illumination, invalid, occlusion, pose

import json

def load_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        for i in range(len(content)):
            content[i] = content[i].strip()
        return content
    except Exception as e:
        print("Error while loading text file.")
        print(e)
        return None
    
def extract_dictionary(file_content):
    config_dict = dict()
    IMAGE_DETAIL_KEYS = ["x1", "y1", "w", "h", "blur", "expression", "illumination", "invalid", "occlusion", "pose"]
    # config_dict: {
    # "image_file1": {
    #       "name": "image_file_name"
    #       "bounding_num": 3
    #       "infos": {
    #           "0": {"x1": x1, "y1": y1, "w": w, "h": h},
    #           "1": {"x1": x1, "y1": y1, "w": w, "h": h}}
    # }, ...}
    
    for idx, line in enumerate(file_content):
    
        if line.endswith('.jpg'):
            bounding_info = dict()
            path = line
            bounding_info["path"] = path
            bounding_num = file_content[idx + 1]
            bounding_info["bounding_num"] = file_content[idx+1]
            detail_infos = dict()
            for i in range(idx + 2, idx + 2 + int(bounding_num)):
                info_key = i - (idx + 2)
                # x1, y1, w, h, blur, expression, illumination, invalid, occlusion, pose
                info_val_array = file_content[i].split(" ")
                face_detail = dict(zip(IMAGE_DETAIL_KEYS, info_val_array))
                detail_infos[info_key] = face_detail
                
            bounding_info["details"] = detail_infos
            config_dict[path] = bounding_info
    
    return config_dict

def dump_to_json(dictionary, path):
    with open(path, 'w') as json_file:
        json.dump(dictionary, json_file)

# TRAIN_CONFIG_FILE_PATH = "..\\wider-dataset-config\\wider_face_train_bbx_gt.txt"
TRAIN_CONFIG_FILE_PATH = "wider-dataset-config\\wider_face_train_bbx_gt.txt"
TRAIN_OUTPUT_PATH = "training_config.json"

VALID_CONFIG_FILE_PATH = "wider-dataset-config\wider_face_val_bbx_gt.txt"
VALID_OUTPUT_PATH = "valid_config.json"

paths = [(TRAIN_CONFIG_FILE_PATH, TRAIN_OUTPUT_PATH), (VALID_CONFIG_FILE_PATH, VALID_OUTPUT_PATH)]

for config_path, output_path in paths:
    content = load_text_file(config_path)
    result = extract_dictionary(content)
    dump_to_json(result, output_path)