# Using the same image as we use in CircleCI to avoid transfer costs
FROM cimg/openjdk:11.0 AS schema-registry

# Use latest stable release here
ENV CONFLUENT_VERSION 5.5.1
ENV SCALA_VERSION 2.12

USER root
WORKDIR /opt/schema-registry
COPY install /opt/schema-registry/
COPY docker-start /opt/schema-registry/
RUN ./install && rm install


# Share the same base image to reduce layers
FROM hypertrace/java:11

MAINTAINER Hypertrace "https://www.hypertrace.org/"

WORKDIR /opt/schema-registry

ARG USER=schema-registry

RUN adduser -g '' -h /opt/schema-registry -D ${USER}

# use hard-coded username as a workaround to CircleCI build failure.
# see https://github.com/moby/moby/issues/35018 for more details.
# TODO: switch back when CircleCI config is using newer remote Docker
COPY --from=schema-registry --chown=schema-registry /opt/schema-registry /opt/schema-registry
# TODO COPY docker-healthcheck /usr/local/bin/

USER ${USER}

EXPOSE 8081

# We use start period of 10s to avoid marking Service Registry unhealthy on slow or contended CI hosts
HEALTHCHECK --interval=2s --start-period=10s --timeout=1s CMD wget -qO- http://127.0.0.1:8081 &> /dev/null || exit 1

ENTRYPOINT /opt/schema-registry/docker-start
