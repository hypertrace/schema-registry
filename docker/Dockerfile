# Using the same image as we use in CircleCI to avoid transfer costs
FROM cimg/openjdk:14.0.2 AS install

# Use latest stable release here
ENV CONFLUENT_VERSION=5.5.1 SCALA_VERSION=2.12

USER root
WORKDIR /install
ADD install /tmp/install
RUN /tmp/install && rm /tmp/install

# Share the same base image to reduce layers
FROM hypertrace/java:11

MAINTAINER Hypertrace "https://www.hypertrace.org/"

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

ENV JAVA_OPTS="-Xms128M -Xmx200M -XX:+ExitOnOutOfMemoryError"

EXPOSE 8081

# We use start period of 30s to avoid marking the container unhealthy on slow or contended CI hosts
HEALTHCHECK --interval=1s --start-period=30s --timeout=5s CMD ["docker-healthcheck"]

ENTRYPOINT ["start-schema-registry"]
