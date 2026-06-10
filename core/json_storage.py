from ast import TypeVar
from pathlib import Path
import json

from pydantic import BaseModel

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "issues.json" 
#DATA_FILE = f"{DATA_DIR}/issues.json" 


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            content = f.read()
            if content.strip():
                return json.loads(content)
    
    return []

## Definimos un tipo genérico basado en Pydantic
# T = TypeVar("T", bound=BaseModel)
# def load_data_model(model: Type[T] = None) -> list[T] | list[dict]:
#     if DATA_FILE.exists():
#         with open(DATA_FILE, "r") as f:
#             content = f.read()
#             if content.strip():
#                 raw_list = json.loads(content)
#                 # Si pasamos un modelo, convertimos cada dict en un objeto Pydantic
#                 if model is not None:
#                     return [model.model_validate(item) for item in raw_list]
#                 return raw_list
    
#     return []


def save_data(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)