#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamjobsbackend.settings")
    django_env = os.environ.get("DJANGO_ENV", "development")
    try:
        from django.core.management import (  # pylint: disable=import-outside-toplevel
            execute_from_command_line,
        )
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if (
        django_env in ("development", "staging", "production")
        and os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
        and os.environ.get("OTEL_EXPORTER_OTLP_HEADERS")
    ):
        provider = TracerProvider()
        processor = BatchSpanProcessor(OTLPSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        match django_env:
            case "development":
                SQLite3Instrumentor().instrument()
            case "production" | "staging":
                Psycopg2Instrumentor().instrument()
        DjangoInstrumentor().instrument(is_sql_commentor_enabled=True)
        RequestsInstrumentor().instrument()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
