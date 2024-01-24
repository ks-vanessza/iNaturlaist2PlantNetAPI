import requests
import pandas as pd
import time


def get_image_data(url):
    id = url.split('/')[-1]
    api_endpoint = f"https://api.inaturalist.org/v1/observations/{id}"

    while True:
        response = requests.get(api_endpoint)

        if response.status_code == 200:
            break
        else:
            print(f"⚠️⚠️⚠️ Retrying for {url}")
            time.sleep(2)

    response = response.json()
    result = response.get('results', [])[0]
    desc_id = result.get('description', 'No description available')

    # Replace line breaks with a space
    desc_id = desc_id.replace('\n', ' ')

    image_urls = [obs_photo['photo']['url'].replace('square', 'large')
                  for obs_photo in result.get('observation_photos', [])
                  if 'photo' in obs_photo and 'url' in obs_photo['photo']]

    return id, api_endpoint, url, desc_id, image_urls


# Read the CSV file
df = pd.read_csv('../Data_processing/df_inat.csv')

data = []
for index, row in df.iterrows():
    id, api_endpoint, url, desc_id, image_urls = get_image_data(row['x'])

    # Print info
    print(f"Images for {url}")
    print(f"\tObservation ID: {id}")
    print(f"\tAPI Endpoint: {api_endpoint}")
    print(f"\tDescription: {desc_id}")
    print("\tImage URLs:")
    for image_url in image_urls:
        print("\t\t" + image_url)
    print()
    data.append({
        'Observation id': id,
        'API': api_endpoint,
        'URL': url,
        'Desc': desc_id,
        'Image': image_urls
    })

# Convert the data to a DataFrame
df_result = pd.DataFrame(data)
df_result.to_csv('observation_images.csv', index=False)
