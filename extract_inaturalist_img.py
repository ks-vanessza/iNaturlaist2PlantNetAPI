import requests
import pandas as pd
import time
from tqdm import tqdm
"""Retrieve image data from the iNaturalist API."""


def get_image_data(url):
    observation_id = url.split('/')[-1]
    api_endpoint = f"https://api.inaturalist.org/v1/observations/{observation_id}"
    MAX_RETRIES = 50
    retries_counter = 0

    while retries_counter < MAX_RETRIES:
        response = requests.get(api_endpoint)

        if response.status_code == 200:
            break
        else:
            print(f"⚠️⚠️⚠️ Retrying for {url}")
            time.sleep(2)
            retries_counter += 1

    if retries_counter == MAX_RETRIES:
        print(f"Failed to get a response for {url}")
        return observation_id, api_endpoint, url, 'No description available', []

    response_json = response.json()
    result = response_json.get('results', [])[0]
    desc_id = result.get('description', 'No description available').replace('\n', ' ')

    image_urls = [obs_photo['photo']['url'].replace('square', 'large') for obs_photo in
                  result.get('observation_photos', []) if 'photo' in obs_photo and 'url' in obs_photo['photo']]

    location = result.get('location', None)

    return observation_id, api_endpoint, url, desc_id, image_urls, location


# Process and export data
data = []
df = pd.read_csv('../Data_processing/output_data/inat_url_ST.csv', encoding='utf-8')

for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    id, api_endpoint, url, desc_id, image_urls, location = get_image_data(row['x'])
    data.append({'Observation id': id, 'API': api_endpoint, 'URL': url, 'Desc': desc_id, 'Image': image_urls, 'Location': location})

df_result = pd.DataFrame(data)
df_result.to_csv('observation_images.csv', index=False, encoding='utf-8')
