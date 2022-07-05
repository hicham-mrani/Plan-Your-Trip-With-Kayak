from pathlib import Path
import pandas as pd
import json

def export_csv(data:list, rel_path:str, file_name:str):
    filepath = Path(rel_path + '/' + file_name)
    df = pd.DataFrame(data=data)
    df.to_csv(filepath)

def export_json(dictionary:dict, rel_path:str, file_name:str):
    json_object = json.dumps(dictionary, indent = 4)
    with open(f"{rel_path}{file_name}.json", "w") as outfile:
        outfile.write(json_object)
