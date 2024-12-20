import logging
import traceback
from collections.abc import Mapping
from http import HTTPStatus
from typing import Any

import werkzeug.exceptions

from .error import ErrorGroup

LOG = logging.getLogger(__name__)


def _handle_unexpected(err: Exception) -> tuple[Mapping[str, Any], int]:
    trace = {"traceback": traceback.format_exception(err)}
    payload_error = {
        "errors": [{"code": "INTERNAL_ERROR", "message": "Unexpected error detected"}]
    }

    LOG.error(payload_error | trace)
    return payload_error, HTTPStatus.INTERNAL_SERVER_ERROR


def _handle_group(ec: ErrorGroup) -> tuple[Mapping[str, Any], int]:
    if int(ec.message) >= int(HTTPStatus.INTERNAL_SERVER_ERROR):
        return _handle_unexpected(ec)

    response_payload = {"errors": [vars(e) for e in ec.exceptions]}
    LOG.warning(response_payload)
    return response_payload, int(ec.message)


def _handle_werkzeug(
    err: werkzeug.exceptions.HTTPException,
) -> tuple[Mapping[str, Any], int]:
    if err.code and err.code < HTTPStatus.INTERNAL_SERVER_ERROR:
        response_payload = {
            "errors": [{"code": "GENERAL_CLIENT_ERROR", "message": err.description}]
        }
        LOG.warning(response_payload)
        return response_payload, err.code
    return _handle_unexpected(err)


def handle_error(err: Exception) -> tuple[Mapping[str, Any], int]:
    if isinstance(err, ErrorGroup):
        return _handle_group(err)
    if isinstance(err, werkzeug.exceptions.HTTPException):
        return _handle_werkzeug(err)
    return _handle_unexpected(err)
