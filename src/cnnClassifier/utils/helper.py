import os
from box.exceptions import BoxValueError
from box import Box
import tensorflow as tf
import yaml
from cnnClassifier.logger import logger
import json
import joblib
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64
import shutil



def read_yaml(path_to_yaml: Path) -> Box:

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            if not content:
                raise ValueError(f"The YAML file at {path_to_yaml} is empty.")
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return Box(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")




def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
    
def save_model(path: Path, model: tf.keras.Model):
        model.save(path)



def load_model(path: Path) -> tf.keras.Model:
    return tf.keras.models.load_model(path)





def save_score(score):
    loss, accuracy, precision, recall = score

    if precision + recall > 0:  
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    # Save all scores
    scores = {
        "loss": loss,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }
    
    save_path = Path("artifact/score/scores.json")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(save_path, "w") as f:
        json.dump(scores, f, indent=4)

    print("Scores saved successfully:", scores)

# def copy_model(source_path:Path,dest_path:Path):

    
#     if not os.path.exists(source_path):
#         logger.info(f"The source file does not exist at {source_path}")

#     os.makedirs(dest_path,exist_ok=True)

#     shutil.copy2(source_path,dest_path)

#     logger.info(f"Model is sucessifully saved at {dest_path}")


