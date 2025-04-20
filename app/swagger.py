from flask import Blueprint, jsonify, Response
import os
import json

swagger_bp = Blueprint("swagger", __name__)


@swagger_bp.route("/swagger.json")
def swagger_json():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    swagger_file_path = os.path.join(root_dir, "swagger.yaml")

    if not os.path.exists(swagger_file_path):
        return (
            jsonify(
                {
                    "error": "Swagger specification file not found",
                    "message": f"Make sure swagger.yaml exists in the project root directory.",
                }
            ),
            404,
        )

    try:
        import yaml

        with open(swagger_file_path, "r") as f:
            spec = yaml.safe_load(f.read())

        response = Response(json.dumps(spec), mimetype="application/json")
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    except ImportError:
        return (
            jsonify(
                {
                    "error": "PyYAML is not installed",
                    "message": "Run 'pip install pyyaml' to enable YAML to JSON conversion",
                }
            ),
            500,
        )
    except Exception as e:
        return (
            jsonify(
                {"error": "Error processing Swagger specification", "message": str(e)}
            ),
            500,
        )


@swagger_bp.route("/swagger")
def swagger_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>FlaskApp API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css">
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "/swagger.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    layout: "BaseLayout",
                    defaultModelsExpandDepth: -1
                });
                window.ui = ui;
            };
        </script>
    </body>
    </html>
    """
