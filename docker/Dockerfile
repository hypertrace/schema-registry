FROM adoptopenjdk/openjdk11:jre-11.0.4_11@sha256:140ba182d696180600a2871a98f67ad0ee2d6a1e48a7c570d1c0e156860c2a9d

ENV SCHEMA_REGISTRY_VERSION=5.3.2-1

ADD docker-start.sh /usr/bin/docker-start.sh

RUN apt-get update && \
    apt-get install -y gnupg && \
    echo "deb [arch=amd64] https://packages.confluent.io/deb/5.3 stable main" | tee -a /etc/apt/sources.list.d/confluent.list && \
    curl https://packages.confluent.io/deb/5.3/archive.key | apt-key add - && \
    apt-get update && \
    apt-get install -y confluent-schema-registry=${SCHEMA_REGISTRY_VERSION} && \
    chmod 755 /usr/bin/docker-start.sh && \
    apt-get clean && \
    rm -rf /tmp/* /var/lib/apt/lists/*

COPY LICENSE /usr/share/doc/schema-registry/licenses/LICENSE

EXPOSE 8081

CMD ["/usr/bin/docker-start.sh"]
