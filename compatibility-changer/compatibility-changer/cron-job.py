import requests
import logging
import os
import urllib.parse
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read helm values
host = os.getenv('SCHEMA_REGISTRY_HOST', 'localhost')
port = os.getenv('SCHEMA_REGISTRY_PORT', '8081')
base_url = f"http://{host}:{port}"

def url_encode(subject):
    return urllib.parse.quote(subject, safe='')

def get_subjects():
    url = f"{base_url}/subjects"
    response = requests.get(url)
    return response.json()

def get_subject_versions(subject):
    encoded_subject = url_encode(subject)
    url = f"{base_url}/subjects/{encoded_subject}/versions"
    response = requests.get(url)
    return response.json()

def get_subject_version_details(subject, version):
    encoded_subject = url_encode(subject)
    url = f"{base_url}/subjects/{encoded_subject}/versions/{version}"
    response = requests.get(url)
    return response.json()

def get_compatibility_level(subject):
    encoded_subject = url_encode(subject)
    url = f"{base_url}/config/{encoded_subject}"
    response = requests.get(url)
    return response.json().get('compatibilityLevel')

def set_compatibility_level(subject):
    encoded_subject = url_encode(subject)
    url = f"{base_url}/config/{encoded_subject}"
    logging.info(f"Setting compatibility level to NONE for subject: {subject} with URL: {url}")
    response = requests.put(url, json={"compatibilityLevel": "NONE"})
    logging.info(f"PUT {url} response: {response.json}")

def main():
    subjects = get_subjects()
    logging.info(f"All subjects: {subjects}")
    for subject in tqdm(subjects):
        versions = get_subject_versions(subject)
        if not versions:
            continue

        # Select the first version
        first_version = versions[0]
        details = get_subject_version_details(subject, first_version)

        if details.get('schemaType') == 'PROTOBUF':
            current_level = get_compatibility_level(subject)

            if current_level != 'NONE':
                set_compatibility_level(subject)
                logging.info(f"Set compatibility level to NONE for subject: {subject}")
            else:
                logging.info(f"Compatibility level already NONE for subject: {subject}")
        else:
            logging.info(f"Skipping subject {subject} as it is not of schemaType PROTOBUF")

if __name__ == "__main__":
    main()
