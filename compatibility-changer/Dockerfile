FROM python:3.12.4-slim

# update packages
RUN apt update && apt upgrade -y

RUN apt install -y curl && \
    apt install -y wget

# setup virtual environment
RUN python -m venv /opt/venv

# create directory and copy pinot-data-metrics directory
RUN mkdir -p /opt/compatibility-changer

COPY compatibility-changer /opt/compatibility-changer

# installed required dependent library
RUN /opt/venv/bin/pip install -r /opt/compatibility-changer/requirements.txt

# run the application
WORKDIR "/opt/compatibility-changer"
CMD ["/opt/venv/bin/python"]