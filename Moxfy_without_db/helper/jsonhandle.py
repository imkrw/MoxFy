import os
import json


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def save_value(data_dir, data_file, key, value):
    mkdir(data_dir)
    data = {}
    file_path = os.path.join(data_dir, data_file)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    data[key] = value
    with open(file_path, "w") as f:
        json.dump(data, f)


def load_value(data_dir, data_file, key):
    mkdir(data_dir)
    data = {}
    file_path = os.path.join(data_dir, data_file)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    if "permissions" in data:
        permissions = data["permissions"]
        if key in permissions:
            return permissions[key]

    return data.get(key, "")


def delete_value(data_dir, data_file, key):
    mkdir(data_dir)
    data = {}
    file_path = os.path.join(data_dir, data_file)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    if key in data:
        del data[key]
    with open(file_path, "w") as f:
        json.dump(data, f)
