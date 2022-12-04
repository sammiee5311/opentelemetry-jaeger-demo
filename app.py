from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

SERVICE_NAME = "opentelemetry-jaeger-demo"
OPENTELEMETRY_ENDPOINT = "http://localhost:4317"

resource = Resource(attributes={SERVICE_NAME: SERVICE_NAME})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=OPENTELEMETRY_ENDPOINT))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)


@app.route("/")
def main():
    with trace.get_tracer(__name__).start_as_current_span("foo"):
        with trace.get_tracer(__name__).start_as_current_span("bar"):
            return {"response": "Hello World"}


if __name__ == "__main__":
    app.run()
