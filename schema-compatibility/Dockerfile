FROM python:3.12.4-slim

# update packages
RUN apt update && apt upgrade -y && apt install -y curl && rm -rf /var/lib/apt/lists/*

# setup virtual environment
RUN python -m venv /opt/venv

# create directory and copy schema-compatibility directory
RUN mkdir -p /opt/schema-compatibility

COPY schema-compatibility /opt/schema-compatibility

# installed required dependent library
RUN /opt/venv/bin/pip install -r /opt/schema-compatibility/requirements.txt

# run the application
WORKDIR "/opt/schema-compatibility"
CMD ["/opt/venv/bin/python"]
