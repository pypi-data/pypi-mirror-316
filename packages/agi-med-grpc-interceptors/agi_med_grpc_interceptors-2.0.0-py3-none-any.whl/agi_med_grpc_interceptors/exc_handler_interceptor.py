from typing import Callable, Iterator, Never, override

from grpc import StatusCode, HandlerCallDetails, ServicerContext
from loguru import logger
from prometheus_client import Counter

from .base_interceptor import ReqType, RespType
from . import BaseInterceptor, BaseGrpcError


class ExcHandlerInterceptor(BaseInterceptor):

    def __init__(self) -> None:
        self._error_counter: Counter = Counter(
            "error_counter", "Count errors per path", ["path", "status_code", "error"]
        )

    @override
    def handle_method(  # type: ignore[override]
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> RespType | Iterator[RespType]:
        try:
            return super().handle_method(method, request, context, handler_call_details, method_type)
        except Exception as exc:
            self.exception_handler(exc, request, context, handler_call_details, method_type)

    @override
    def handle_stream_response(
        self,
        method: Callable,
        request: ReqType | Iterator[ReqType],
        context: ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> Iterator[RespType]:
        try:
            yield from super().handle_stream_response(method, request, context, handler_call_details, method_type)
        except Exception as exc:
            self.exception_handler(exc, request, context, handler_call_details, method_type)

    def exception_handler(
        self,
        exc: Exception,
        request: ReqType | Iterator[ReqType],
        context: ServicerContext,
        handler_call_details: HandlerCallDetails,
        method_type: str,
    ) -> Never:
        status_code: StatusCode
        if isinstance(exc, BaseGrpcError):
            status_code = exc.status_code
            logger.error(f"Error {exc} in {method_type} gRPC call: {handler_call_details.method}. Pack to .abort()")
            logger.debug(f"Error request: {request}")
            exc.abort(context)
        else:
            status_code = StatusCode.INTERNAL
        error: str = exc.__class__.__name__
        self._error_counter.labels(path=handler_call_details.method, status_code=status_code, error=error).inc()
        raise
