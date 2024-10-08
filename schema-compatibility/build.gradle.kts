plugins {
  id("base")
  id("org.hypertrace.docker-plugin")
  id("org.hypertrace.docker-publish-plugin")
}

hypertraceDocker {
  defaultImage {
    imageName.set("schema-compatibility")
    dockerFile.set(file("Dockerfile"))
  }
}