""" SDX Topology Validator """
import os
from flask import Flask, request, jsonify, current_app
from openapi_core import create_spec
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.contrib.flask import FlaskOpenAPIRequest
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename
from werkzeug.exceptions import (BadRequest)


app = Flask(__name__)


@app.route('/validator/v1/validate', methods=['POST'])
def validate():
    """ validate the sdx topology """
    yml_file = os.path.join(current_app.root_path, 'validator.yml')
    spec_dict, spec_url = read_from_filename(yml_file)
    try:
        spec_error = validate_spec(spec_dict)
    except ValueError as err:
        raise BadRequest(err) from err
    else:
        if spec_error:
            print("spec_url %s", spec_url)
            raise BadRequest(spec_error) from spec_error
    spec = create_spec(spec_dict)
    try:
        data = request.json
    except BadRequest:
        result = "The request body is not a well-formed JSON."
        raise BadRequest(result) from BadRequest
    validator = RequestValidator(spec)
    openapi_request = FlaskOpenAPIRequest(request)
    result = validator.validate(openapi_request)
    if result.errors:
        errors = result.errors[0]
        if hasattr(errors, "schema_errors"):
            schema_errors = errors.schema_errors[0]
            error_response = {
                "error_message": schema_errors.message,
                "error_validator": schema_errors.validator,
                "error_validator_value": schema_errors.validator_value,
                "error_path": list(schema_errors.path),
                "error_schema": schema_errors.schema,
                "error_schema_path": list(schema_errors.schema_path),
            }
        else:
            error_response = {
                    "Error_response": errors
                }
        print('############ error_response ####################')
        print(error_response)
        return jsonify(error_response), 400
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
