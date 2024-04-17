import time
import pandas as pd
import requests
import ast

from tqdm import tqdm

# Constants
API_KEY = "YOUR API KEY HERE"
PROJECT = "k-northern-europe"
API_ENDPOINT = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"
TOP_X_PREDICTION = 5
MAX_RETRIES = 50  # Maximum number of retries for API requests

def get_prediction(row):
    desc_id = row['Desc']
    image_urls = ast.literal_eval(row['Image'])
    url = row['URL']

    # Parameters
    organs = ['auto' for _ in image_urls]
    no_reject = True
    include_related_images = True
    params = {"images": image_urls, "organs": organs, "no-reject": no_reject,
              "include-related-images": include_related_images}

    retries = 0
    while retries < MAX_RETRIES:
        response = requests.get(API_ENDPOINT, params=params)

        if response.status_code == 200:
            break
        else:
            print(f"⚠️⚠️⚠️ Retrying for {url}")
            time.sleep(2)
            retries += 1

    if retries == MAX_RETRIES:
        print(f"Failed to get a response for {url}")
        return [], []

    response_json = response.json()
    predictions_line_by_line = []
    predictions_one_line = []

    combined_dict = {"Desc ID": desc_id, "URL": url}
    for i in range(TOP_X_PREDICTION):
        # Check if 'i' is within the range of 'results' length
        if i < len(response_json['results']):
            score = response_json['results'][i]['score']
            name = response_json['results'][i]['species']['scientificName']

            # Further check if there is at least one image in 'images' list
            if 'images' in response_json['results'][i] and response_json['results'][i]['images']:
                image = response_json['results'][i]['images'][0]['url']['o']
            else:
                image = "No image available"
            predictions_line_by_line.append({
                "Desc ID": desc_id,
                "URL": url,
                "Score": score,
                "Name": name,
                "Predic. Img": image
            })
            # Add new keys to the combined dictionary
            combined_dict.update({
                f"Score{i}": score,
                f"Name{i}": name,
                f"Predic. Img{i}": image
            })
        else:
            break  # Break the loop if 'i' is out of range for 'results'

    # Add the combined dictionary to predictions_one_line
    predictions_one_line.append(combined_dict)

    return predictions_line_by_line, predictions_one_line


prediction_per_line = []
one_line_prediction = []
# Read the CSV file
df = pd.read_csv('observation_images.csv')
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    predictions_line_by_line, predictions_one_line = get_prediction(row)
    prediction_per_line.extend(predictions_line_by_line)
    one_line_prediction.extend(predictions_one_line)

# Convert the list of dictionaries to a DataFrame
df_per_line = pd.DataFrame(prediction_per_line)
df_one_line = pd.DataFrame(one_line_prediction)

df_per_line.to_csv('prediction_per_line.csv', index=False)
df_one_line.to_csv('prediction_one_line_prediction.csv', index=False)
