# Schema Registry Helm Chart
This chart bootstraps a deployment of a Confluent Schema Registry

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
* Optionally add a cronjob to take backup the schema registry topic and save it in [Google Cloud Storage](https://cloud.google.com/storage).


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