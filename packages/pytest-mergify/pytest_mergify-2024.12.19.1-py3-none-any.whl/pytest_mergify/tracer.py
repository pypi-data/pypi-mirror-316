import dataclasses
import logging
import os

import opentelemetry.sdk.resources
from opentelemetry.sdk.trace import export
from opentelemetry import context
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor, Span
from opentelemetry.exporter.otlp.proto.http import Compression
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)

from pytest_mergify import utils

import pytest_opentelemetry.instrumentation
import pytest_mergify.resources.ci as resources_ci
import pytest_mergify.resources.github_actions as resources_gha


class InterceptingSpanProcessor(SpanProcessor):
    trace_id: None | int

    def __init__(self) -> None:
        self.trace_id = None

    def on_start(
        self, span: Span, parent_context: context.Context | None = None
    ) -> None:
        if span.attributes is not None and any(
            "pytest" in attr for attr in span.attributes
        ):
            self.trace_id = span.context.trace_id


class ListLogHandler(logging.Handler):
    """Custom logging handler to capture log messages into a list."""

    def __init__(self) -> None:
        super().__init__()
        self.log_list: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.log_list.append(self.format(record))


@dataclasses.dataclass
class MergifyTracer:
    token: str | None = dataclasses.field(
        default_factory=lambda: os.environ.get("MERGIFY_TOKEN")
    )
    repo_name: str | None = dataclasses.field(default_factory=utils.get_repository_name)
    interceptor: InterceptingSpanProcessor | None = None
    api_url: str = dataclasses.field(
        default_factory=lambda: os.environ.get(
            "MERGIFY_API_URL", "https://api.mergify.com"
        )
    )
    exporter: export.SpanExporter | None = dataclasses.field(init=False, default=None)
    tracer: opentelemetry.trace.Tracer | None = dataclasses.field(
        init=False, default=None
    )
    tracer_provider: opentelemetry.sdk.trace.TracerProvider | None = dataclasses.field(
        init=False, default=None
    )
    log_handler: ListLogHandler = dataclasses.field(
        init=False, default_factory=ListLogHandler
    )

    def __post_init__(self) -> None:
        span_processor: SpanProcessor

        # Set up the logger
        self.log_handler.setLevel(logging.ERROR)  # Capture ERROR logs by default
        self.log_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )

        logger = logging.getLogger("opentelemetry")
        # FIXME: we should remove the handler when this tracer is not used
        # (e.g., reconfigure() is called) Since reconfigure() is unlikely to be
        # called outside our testing things, it's not a big deal to leak it.
        logger.addHandler(self.log_handler)

        if os.environ.get("PYTEST_MERGIFY_DEBUG"):
            self.exporter = export.ConsoleSpanExporter()
            span_processor = export.SimpleSpanProcessor(self.exporter)
        elif utils.strtobool(os.environ.get("_PYTEST_MERGIFY_TEST", "false")):
            from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
                InMemorySpanExporter,
            )

            self.exporter = InMemorySpanExporter()
            span_processor = export.SimpleSpanProcessor(self.exporter)
        elif self.token:
            if self.repo_name is None:
                return

            self.exporter = OTLPSpanExporter(
                endpoint=f"{self.api_url}/v1/repos/{self.repo_name}/ci/traces",
                headers={"Authorization": f"Bearer {self.token}"},
                compression=Compression.Gzip,
            )
            span_processor = export.BatchSpanProcessor(self.exporter)
        else:
            return

        resources_gha.GitHubActionsResourceDetector().detect()
        resource = opentelemetry.sdk.resources.get_aggregated_resources(
            [
                resources_ci.CIResourceDetector(),
                resources_gha.GitHubActionsResourceDetector(),
            ]
        )

        self.tracer_provider = TracerProvider(resource=resource)

        self.tracer_provider.add_span_processor(span_processor)

        if self.ci_supports_trace_interception():
            self.interceptor = InterceptingSpanProcessor()
            self.tracer_provider.add_span_processor(self.interceptor)

        self.tracer = self.tracer_provider.get_tracer("pytest-mergify")

        # Replace tracer of pytest-opentelemetry
        pytest_opentelemetry.instrumentation.tracer = self.tracer

    def ci_supports_trace_interception(self) -> bool:
        return utils.get_ci_provider() == "github_actions"
