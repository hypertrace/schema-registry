import requests
import logging
import os
import urllib.parse
from pyhocon import ConfigFactory, ConfigTree
from config import SCHEMA_REGISTRY_URL, COMPATIBILITY_MAP, SUBJECTS_URL, VERSIONS_URL_TEMPLATE, VERSION_DETAILS_URL_TEMPLATE, COMPATIBILITY_LEVEL_URL_TEMPLATE, LOGGING_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOGGING_LEVEL, format=LOG_FORMAT)

def url_encode(subject):
    return urllib.parse.quote(subject, safe='')

def get_subjects():
    logging.info(f"Fetching subjects from URL: {SUBJECTS_URL}")
    response = requests.get(SUBJECTS_URL)
    if response.status_code != 200:
        logging.warning(f"Failed to fetch subjects: {response.status_code} - {response.text}")
        exit(1)
        return []
    return response.json()

def get_subject_versions(subject):
    encoded_subject = url_encode(subject)
    url = VERSIONS_URL_TEMPLATE(encoded_subject)
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(f"Failed to fetch versions for subject {subject}: {response.status_code} - {response.text}")
        return []
    return response.json()

def get_subject_version_details(subject, version):
    encoded_subject = url_encode(subject)
    url = VERSION_DETAILS_URL_TEMPLATE(encoded_subject, version)
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(f"Failed to fetch version details for subject {subject}: {response.status_code} - {response.text}")
        return {}
    return response.json()

def get_compatibility_level(subject):
    encoded_subject = url_encode(subject)
    url = COMPATIBILITY_LEVEL_URL_TEMPLATE(encoded_subject)
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(f"Failed to fetch compatibility level for subject {subject}: {response.status_code} - {response.text}")
        return None
    return response.json().get('compatibilityLevel')

def set_compatibility_level(subject, level):
    encoded_subject = url_encode(subject)
    url = COMPATIBILITY_LEVEL_URL_TEMPLATE(encoded_subject)
    logging.info(f"Setting compatibility level to {level} for subject {subject} with URL: {url}")
    response = requests.put(url, json={"compatibilityLevel": level})
    if response.status_code != 200:
        logging.error(f"Failed to set compatibility level for subject {subject}: {response.status_code} - {response.text}")
    else:
        logging.info(f"PUT {url} response: {response.json()}")

def get_override_compatibility(config, schema_type, subject):
    schema_type_config = config.get(schema_type, {})
    overrides = schema_type_config.get('overrides', {})
    return overrides.get(subject, schema_type_config.get('default'))

def main():
    config_file_path = "/app/resources/configs/compatibility-changer/application.conf"
    try:
        config: ConfigTree = ConfigFactory.parse_file(config_file_path)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        config = ConfigTree()

    subjects = get_subjects()
    logging.info(f"Total number of subjects: {len(subjects)}")

    for subject in subjects:
        print()
        logging.info(f"{subject}")
        versions = get_subject_versions(subject)
        if not versions:
            continue

        first_version = versions[0]
        details = get_subject_version_details(subject, first_version)

        schema_type = details.get('schemaType', 'AVRO')  # Default to AVRO if schemaType not specified

        compatibility_level = COMPATIBILITY_MAP.get(schema_type, {}).get('overrides', {}).get(subject)

        if not compatibility_level:
            compatibility_level = COMPATIBILITY_MAP.get(schema_type, {}).get('default')

        if not compatibility_level:
            continue

        current_level = get_compatibility_level(subject)

        if current_level != compatibility_level:
            set_compatibility_level(subject, compatibility_level)

if __name__ == "__main__":
    base_url = os.getenv('SCHEMA_REGISTRY_URL', SCHEMA_REGISTRY_URL)
    main()
