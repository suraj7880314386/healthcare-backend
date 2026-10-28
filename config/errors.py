from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def handler(exc, ctx):
    res = exception_handler(exc, ctx)

    if res is None:
        # drf didn't handle it, check for db errors, else let django send a 500
        if isinstance(exc, IntegrityError):
            return Response(
                {"success": False, "errors": {"detail": "Database integrity error"}},
                status=400,
            )
        return None

    res.data = {"success": False, "errors": res.data}
    return res
