import requests
import logging
import os
import urllib.parse
from pyhocon import ConfigFactory, ConfigTree
from config import SCHEMA_REGISTRY_URL, COMPATIBILITY_MAP, LOGGING_LEVEL, LOG_FORMAT


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
        logging.error(f"Exiting. Failed to fetch versions for subject {subject}: {response.status_code} - {response.text}")
        exit(1)
    return response.json()

def get_schema(subject, version):
    encoded_subject = url_encode(subject)
    url = VERSION_DETAILS_URL_TEMPLATE(encoded_subject, version)
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Exiting. Failed to fetch schema for subject {subject}: {response.status_code} - {response.text}")
        exit(1)
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
    request_json = {"compatibility": level}
    response = requests.put(url, json=request_json)
    if response.status_code != 200:
        logging.error(f"Exiting. Failed to set compatibility level for subject {subject}: {response.status_code} - {response.text}")
        logging.info(f"Request json: {request_json}")
        exit(1)
    else:
        logging.info(f"PUT {url} response: {response.json()}")

def get_override_compatibility(config, schema_type, subject):
    schema_type_config = config.get(schema_type, {})
    overrides = schema_type_config.get('overrides', {})
    return overrides.get(subject, schema_type_config.get('default'))

def main():
    config_file_path = "/app/resources/configs/schema-compatibility/application.conf"
    try:
        config: ConfigTree = ConfigFactory.parse_file(config_file_path)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        config = ConfigTree()

    # Query Endpoints
    global SUBJECTS_URL, VERSIONS_URL_TEMPLATE, VERSION_DETAILS_URL_TEMPLATE, COMPATIBILITY_LEVEL_URL_TEMPLATE

    base_url = config.get("schemaRegistryUrl", SCHEMA_REGISTRY_URL)
    SUBJECTS_URL = f"{base_url}/subjects"
    VERSIONS_URL_TEMPLATE = lambda subject: f"{base_url}/subjects/{subject}/versions"
    VERSION_DETAILS_URL_TEMPLATE = lambda subject, version: f"{base_url}/subjects/{subject}/versions/{version}"
    COMPATIBILITY_LEVEL_URL_TEMPLATE = lambda subject: f"{base_url}/config/{subject}"

    compatibility_map = config.get("compatibility", COMPATIBILITY_MAP)

    subjects = get_subjects()
    logging.info(f"Total number of subjects: {len(subjects)}")

    for subject in subjects:
        logging.info(f"\nSubject: {subject}")
        versions = get_subject_versions(subject)
        if not versions:
            logging.warning(f"No version found for subject: {subject}")
            continue

        first_version = versions[0]
        schema = get_schema(subject, first_version)

        schema_type = schema.get('schemaType', 'AVRO')  # Default to AVRO if schemaType does not exist

        compatibility_level = compatibility_map.get(schema_type, {}).get('overrides', {}).get(subject)

        if not compatibility_level:
            compatibility_level = compatibility_map.get(schema_type, {}).get('default')

        if not compatibility_level:
            continue

        current_level = get_compatibility_level(subject)

        if current_level != compatibility_level:
            set_compatibility_level(subject, compatibility_level)

if __name__ == "__main__":
    main()
