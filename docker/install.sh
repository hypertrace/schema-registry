#!/bin/sh

set -eux

echo "*** Downloading Schema Registry"
# download confluent binaries
curl -sSL http://packages.confluent.io/archive/5.5/confluent-community-$CONFLUENT_VERSION-$SCALA_VERSION.tar.gz | tar xz \
confluent-$CONFLUENT_VERSION/bin/schema-registry-run-class \
confluent-$CONFLUENT_VERSION/etc/schema-registry \
confluent-$CONFLUENT_VERSION/share/java/confluent-common \
confluent-$CONFLUENT_VERSION/share/java/rest-utils \
confluent-$CONFLUENT_VERSION/share/java/schema-registry

mv confluent-$CONFLUENT_VERSION/* .

# Remove bash as our images doesn't have it, and it isn't required
sed -i 's~#!/bin/bash~#!/bin/sh~g' bin/*
# Remove bash syntax relating to irrelevant CYGWIN (prevents console errors)
sed -i -e 's/$(uname -a) =~ "CYGWIN"/0/g' -e  's/.*\(\( CYGWIN \)\).*//g' bin/*

# hush logs including HEALTHCHECK
sed -i 's~INFO~WARN~g' etc/schema-registry/log4j.properties
# Stop JUL spam about io.confluent.kafka.schemaregistry.rest.resources.ServerMetadataResource
echo 'org.glassfish.jersey.internal.inject.Providers = SEVERE' > etc/schema-registry/logging.properties

# default to listen on 8081 and connect to "kafka" hostname on default port
cat > etc/schema-registry/schema-registry.properties <<-'EOF'
avro.compatibility.level=full_transitive
kafkastore.group.id=hypertrace-schema-registry
listeners=http://0.0.0.0:8081
host.name=schema-registry
kafkastore.bootstrap.servers=PLAINTEXT://kafka:9092
master.eligibility=true
EOF

echo "*** Cleaning Up"
rm -rf confluent-$CONFLUENT_VERSION

echo "*** Image build complete"
