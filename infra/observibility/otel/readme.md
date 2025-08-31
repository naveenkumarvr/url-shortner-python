Otel Docker command

```bash
docker run --rm -p 4317:4317 -p 4318:4318   -v /mnt/d/code/url-shortner-python/app/otel-collector-config.yaml:/otel-collector-config.yaml   otel/opentelemetry-collector:latest   --config /otel-collector-config.yaml
```