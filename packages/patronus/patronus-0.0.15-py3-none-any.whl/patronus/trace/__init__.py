import json
import random
import traceback
import typing
import functools
import time

import opentelemetry
from opentelemetry import trace
from opentelemetry._logs import SeverityNumber
from opentelemetry.sdk import _logs
from opentelemetry.trace import TraceFlags
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)

logger = opentelemetry._logs.get_logger("patronus")
tracer = trace.get_tracer("patronus")

def jsonify(v: typing.Any):
    try:
        return json.loads(json.dumps(v))
    except TypeError:
        return str(v)


def clean_dict(d: dict):
    if isinstance(d, dict):
        keys_to_delete = []
        for k, v in d.items():
            if v is None:
                keys_to_delete.append(k)
            else:
                clean_dict(v)
        for k in keys_to_delete:
            del d[k]
    if isinstance(d, list):
        for item in d:
            clean_dict(item)


def traced(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with tracer.start_as_current_span(func.__name__) as span:

            # TODO remove
            time.sleep(random.random()/10)

            span: trace.Span
            span.set_attribute("function_name", func.__name__)
            span_ctx = span.get_span_context()
            ret = None
            exc = None
            exc_info = None
            try:
                ret = func(*args, **kwargs)
            except Exception as e:
                exc = e
                exc_info = traceback.format_exc()

            sev = SeverityNumber.ERROR if exc else SeverityNumber.INFO
            body = {
                "input": {
                    **{f"{i}": jsonify(arg) for i, arg in enumerate(args)},
                    **{k: jsonify(v) for k, v in kwargs.items()},
                },
                "output": jsonify(ret) or {},
            }
            if exc is not None:
                body["exception"] = str(exc)
                body["stack_trace"] = exc_info

            log = _logs.LogRecord(
                timestamp=time.time_ns(),
                trace_flags=TraceFlags.SAMPLED,
                trace_id=span_ctx.trace_id,
                span_id=span_ctx.span_id,
                severity_text=sev.name,
                severity_number=sev,
                body=body,
                attributes={"pat.log_type": "function_call", "pat.function_name": func.__name__},
            )
            print(log.to_json())
            logger.emit(log)

            if exc:
                raise exc
            return ret

    return wrapper