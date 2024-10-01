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

# Logging Configuration
LOGGING_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
