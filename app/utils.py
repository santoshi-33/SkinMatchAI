import os
import pandas as pd
import cv2
import numpy as np
from typing import List, Dict, Union

# Load CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(BASE_DIR, 'dataset', 'cosmetics.csv'))
print(f"Reading CSV from: {csv_path}")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")

df = pd.read_csv(csv_path)


# 🔍 New function: Detect skin type using OpenCV
def analyze_skin_type(image_path: str) -> str:
    image = cv2.imread(image_path)
    if image is None:
        return "unknown"

    # Convert image to HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Focus on saturation (S) to guess skin type
    avg_saturation = np.mean(hsv[:, :, 1])
    print(f"Average Saturation: {avg_saturation}")

    # Simple rules to determine skin type
    if avg_saturation < 40:
        return 'dry'
    elif avg_saturation > 100:
        return 'oily'
    else:
        return 'normal'


# 🧴 Recommend products based on skin type
def get_recommendations(skin_type: str, data: pd.DataFrame = df) -> List[Dict[str, Union[str, List[str]]]]:
    tag_map = {
        'oily': ['oil-free', 'non-comedogenic', 'matte'],
        'dry': ['hydrating', 'moisturizing', 'ceramide'],
        'sensitive': ['fragrance-free', 'alcohol-free', 'hypoallergenic'],
        'normal': [],
        'combination': ['oil-free', 'hydrating']
    }

    keywords = tag_map.get(skin_type.lower(), [])

    if not keywords:
        matches = data.head(5)
    else:
        keyword_pattern = '|'.join(keywords)
        matches = data[data['Label Tags'].str.contains(keyword_pattern, case=False, na=False)]

    if matches.empty:
        return []

    return matches[['Brand', 'Name', 'Label', 'Ingredients']].head(5).to_dict(orient='records')
