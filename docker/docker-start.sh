#!/bin/bash

printenv | grep ^SCHEMA_REGISTRY_ | while read line; do
  name=`echo $line | awk -F'=' '{print $1}' | sed 's/^SCHEMA_REGISTRY_//g' | tr '[:upper:]' '[:lower:]' | sed 's/_/./g'`
  value=`echo $line | awk -F'=' '{print $2}'`
  echo "$name=$value"
done > /etc/schema-registry/schema-registry.properties

exec /usr/bin/schema-registry-start /etc/schema-registry/schema-registry.properties
