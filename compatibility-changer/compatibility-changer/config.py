# Schema Registry Service
SCHEMA_REGISTRY_URL = 'http://localhost:8081'

# Helm Configurations
COMPATIBILITY_MAP = {
    "PROTOBUF": {
        "default": "NONE",
        "overrides": {
            "subject-1": "level",
        }
    },
    "AVRO": {
        "overrides": {
            "subject-2": "level",
        }
    }
}

# Query Strings
SUBJECTS_URL = f"{SCHEMA_REGISTRY_URL}/subjects"
VERSIONS_URL_TEMPLATE = lambda subject: f"{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions"
VERSION_DETAILS_URL_TEMPLATE = lambda subject, version: f"{SCHEMA_REGISTRY_URL}/subjects/{subject}/versions/{version}"
COMPATIBILITY_LEVEL_URL_TEMPLATE = lambda subject: f"{SCHEMA_REGISTRY_URL}/config/{subject}"

# Logging Configuration
LOGGING_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
