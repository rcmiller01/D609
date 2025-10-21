import pandas as pd
import json
from pathlib import Path

# Load step trainer data and check for duplicates
data_files = list(Path('Data/step_trainer/landing').glob('*.json'))
all_data = []
for file_path in data_files:
    with open(file_path, 'r') as f:
        for line in f:
            record = json.loads(line.strip())
            all_data.append(record)

df = pd.DataFrame(all_data)
print(f'Total records: {len(df)}')
print(f'Unique by serialNumber + sensorReadingTime: {len(df.drop_duplicates(["serialNumber", "sensorReadingTime"]))}')