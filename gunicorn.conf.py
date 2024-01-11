import os
from gevent import monkey

monkey.patch_all()

from psycogreen import gevent

gevent.patch_psycopg()


access_log_format = (
    '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s ' '"%(f)s" "%(a)s"'
)

django_env = os.environ.get("DJANGO_ENV", "development")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamjobsbackend.settings")


def post_fork(server, worker):
    # If we do this before now, ssl in requests goes unpatched and causes
    # recursion errors.
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    server.log.info("Worker spawned (pid: %s)", worker.pid)
    if (
        django_env in ("development", "staging", "production")
        and os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
        and os.environ.get("OTEL_EXPORTER_OTLP_HEADERS")
    ):
        provider = TracerProvider()
        processor = BatchSpanProcessor(OTLPSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        tracer = trace.get_tracer(__name__)
        DjangoInstrumentor().instrument()
        SQLite3Instrumentor().instrument()
        Psycopg2Instrumentor().instrument()
        RequestsInstrumentor().instrument()
