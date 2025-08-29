import os
import requests

def download_file(url, file_name, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    response = requests.get(url)
    with open(os.path.join(dest_dir, file_name), 'wb') as f:
        f.write(response.content)