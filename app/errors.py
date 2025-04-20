from flask import jsonify, render_template, Blueprint
from quart import has_request_context, request

errors_bp = Blueprint("errors", __name__)


def _is_json_request():
    if not has_request_context():
        return False
    return (
        request.path.startswith("/api/")
        or request.headers.get("Accept") == "application/json"
    )


def _fallback_html(title, message):
    return f"""
    <html>
        <head><title>{title}</title></head>
        <body>
            <h1>{title}</h1>
            <p>{message}</p>
            <p><a href="/">Return to homepage</a></p>
        </body>
    </html>
    """


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    if _is_json_request():
        return (
            jsonify(
                {
                    "error": "Not Found",
                    "message": "The requested resource was not found on this server.",
                    "status_code": 404,
                }
            ),
            404,
        )

    try:
        return render_template("errors/404.html"), 404
    except:
        return (
            _fallback_html(
                "404 Not Found", "The requested resource was not found on this server."
            ),
            404,
        )


@errors_bp.app_errorhandler(500)
def internal_error(error):
    if _is_json_request():
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred on the server.",
                    "status_code": 500,
                }
            ),
            500,
        )

    try:
        return render_template("errors/500.html"), 500
    except:
        return (
            _fallback_html(
                "500 Internal Server Error",
                "An unexpected error occurred on the server.",
            ),
            500,
        )


@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    if _is_json_request():
        return (
            jsonify(
                {
                    "error": "Forbidden",
                    "message": "You do not have permission to access this resource.",
                    "status_code": 403,
                }
            ),
            403,
        )

    try:
        return render_template("errors/403.html"), 403
    except:
        return (
            _fallback_html(
                "403 Forbidden", "You do not have permission to access this resource."
            ),
            403,
        )


@errors_bp.app_errorhandler(401)
def unauthorized_error(error):
    if _is_json_request():
        return (
            jsonify(
                {
                    "error": "Unauthorized",
                    "message": "Authentication is required to access this resource.",
                    "status_code": 401,
                }
            ),
            401,
        )

    try:
        return render_template("errors/401.html"), 401
    except:
        return (
            _fallback_html(
                "401 Unauthorized",
                "Authentication is required to access this resource.",
            ),
            401,
        )
