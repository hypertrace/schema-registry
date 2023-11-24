# Schema Registry Helm Chart
Confluent Schema Registry provides a serving layer for your metadata. It provides a RESTful interface for storing and retrieving Apache Avro schemas. It stores a versioned history of all schemas based on a specified subject name strategy, provides multiple compatibility settings and allows evolution of schemas according to the configured compatibility settings and expanded Avro support.

This chart bootstraps a deployment of a Confluent Schema Registry

## How do we use schema-registry?
Hypertrace uses Confluent schema-registry as a serialization mechanism for the avro messages published to Kafka and these Schemas are defined in the code along with their respective owner modules. All the avro messages schema are registered with the schema registry and kafka producer/consumers uses it while serializing/de-searlizing avro messages.

| ![space-1.jpg]( https://hypertrace-docs.s3.amazonaws.com/ingestion-pipeline.png) | 
|:--:| 
| *Hypertrace Ingestion Pipeline* |

## Prerequisites
* Kubernetes 1.10.0+
* Helm 3.0.0+
* A healthy and accessible Kafka Cluster

## Docker Image Source
* [DockerHub -> ConfluentInc](https://hub.docker.com/r/confluentinc/cp-schema-registry)

## Helm Chart Components
This chart will do the following:

* Create a schema registry cluster using a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
* Create a Service configured to connect to the available schema registry instance on the configured port.
* Optionally apply a [Pod Anti-Affinity](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#inter-pod-affinity-and-anti-affinity-beta-feature) to spread the schema registry instances across nodes.
* Optionally add an [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) resource.
* Optionally start a JMX Exporter container inside schema registry pods.
* Optionally create a Prometheus ServiceMonitor for each enabled jmx exporter container.
* Optionally add a cronjob to take backup the schema registry topic and save it in [Google Cloud Storage](https://cloud.google.com/storage) or [AWS S3](https://aws.amazon.com/pm/serv-s3/)


## Installing the Chart
```console
helm upgrade schema-registry ./helm --install --namespace hypertrace
```

## Configuration
You can specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```console
$ helm upgrade my-release ./helm --install --namespace hypertrace -f values.yaml
```

## Default Values
- You can find all user-configurable settings, their defaults in [values.yaml](helm/values.yaml).
