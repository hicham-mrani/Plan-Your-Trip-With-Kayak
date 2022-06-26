from pathlib import Path
import pandas as pd

def export_csv(data:list, rel_path:str, file_name:str):
    filepath = Path(rel_path + '/' + file_name)
    df = pd.DataFrame(data=data)
    df.to_csv(filepath)