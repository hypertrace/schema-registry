# Using the same image as we use in CircleCI to avoid transfer costs
FROM cimg/openjdk:14.0.2 AS install

# Use latest stable release here
ENV CONFLUENT_VERSION=7.3.1

USER root
WORKDIR /install
COPY install.sh /tmp/
RUN /tmp/install.sh && rm /tmp/install.sh

# Share the same base image to reduce layers
FROM hypertrace/java:11
LABEL MAINTAINER Hypertrace "https://www.hypertrace.org/"

# Add HEALTHCHECK and ENTRYPOINT scripts into the default search path
COPY docker-bin/* /usr/local/bin/

# All content including binaries and logs write under WORKDIR
WORKDIR /opt/schema-registry
ARG USER=schema-registry

# Ensure the process doesn't run as root
RUN adduser -g '' -h ${PWD} -D ${USER}
USER ${USER}

# Copy binaries and config we installed earlier
COPY --from=install --chown=${USER} /install .

# Use Schema Registry specific variable to reduce heap default
ENV SCHEMA_REGISTRY_HEAP_OPTS="-Xms128M -Xmx200M"

# Stop JUL spam about io.confluent.kafka.schemaregistry.rest.resources.ServerMetadataResource
ENV SCHEMA_REGISTRY_LOG4J_OPTS="-Dlog4j.configuration=file:./etc/schema-registry/log4j.properties -Djava.util.logging.config.file=./etc/schema-registry/logging.properties"

RUN mkdir -p /opt/schema-registry/logs && \
    chmod a+w /opt/schema-registry/etc/schema-registry/schema-registry.properties /opt/schema-registry/logs

EXPOSE 8081

# We use start period of 30s to avoid marking the container unhealthy on slow or contended CI hosts
HEALTHCHECK --interval=1s --start-period=30s --timeout=5s CMD ["docker-healthcheck"]

ENTRYPOINT ["start-schema-registry"]
