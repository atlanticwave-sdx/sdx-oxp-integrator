from unittest.mock import patch, mock_open
import yaml
from sdx_topology_validator.topology_validator import load_openapi_schema, resolve_references, get_validator_schema, validate

# Sample OpenAPI schema for testing
sample_openapi_spec = {
    'paths': {
        '/validator': {
            'post': {
                'requestBody': {
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'property1': {'type': 'string'},
                                    'property2': {'type': 'integer'}
                                },
                                'required': ['property1']
                            }
                        }
                    }
                }
            }
        }
    }
}

# Mock data for validation
valid_data = {'property1': 'value', 'property2': 30}
invalid_data = {'property2': 30}

def test_load_openapi_schema():
    """
    Test if `load_openapi_schema` correctly loads the YAML file content.

    This test mocks the reading of the YAML file and verifies that the function
    returns the correct OpenAPI schema as a Python dictionary.
    """
    with patch('sdx_topology_validator.topology_validator.pkg_resources.open_text',\
               mock_open(read_data=yaml.dump(sample_openapi_spec))):
        schema = load_openapi_schema()
        assert schema == sample_openapi_spec

def test_resolve_references():
    """
    Test if `resolve_references` correctly resolves JSON references.

    This test verifies that the function handles an OpenAPI schema without any
    actual references and returns the schema unchanged.
    """
    resolved = resolve_references(sample_openapi_spec)
    assert resolved == sample_openapi_spec

def test_get_validator_schema():
    """
    Test if `get_validator_schema` correctly extracts the validator schema.

    This test ensures that the function extracts the JSON schema used for
    validating the request body of the `/validator` endpoint.
    """
    resolved_spec = sample_openapi_spec
    schema = get_validator_schema(resolved_spec)
    expected_schema = \
        sample_openapi_spec['paths']['/validator']['post']['requestBody']['content']['application/json']['schema']
    assert schema == expected_schema

def test_validate_success():
    """
    Test if `validate` function returns success for valid data.

    This test mocks the functions used in `validate` and verifies that it
    correctly validates valid data against the schema and returns a success result.
    """
    with patch('sdx_topology_validator.topology_validator.load_openapi_schema', return_value=sample_openapi_spec):
        with patch('sdx_topology_validator.topology_validator.resolve_references', return_value=sample_openapi_spec):
            with patch('sdx_topology_validator.topology_validator.get_validator_schema', \
                       return_value=sample_openapi_spec['paths']['/validator']['post']['requestBody']['content']['application/json']['schema']):
                result = validate(valid_data)
                assert result == {"result": "Validated Successfully", "status_code": 200}

def test_validate_failure():
    """
    Test if `validate` function returns failure for invalid data.

    This test mocks the functions used in `validate` and verifies that it
    correctly identifies invalid data, returning an appropriate error message and status code.
    """
    with patch('sdx_topology_validator.topology_validator.load_openapi_schema', return_value=sample_openapi_spec):
        with patch('sdx_topology_validator.topology_validator.resolve_references', return_value=sample_openapi_spec):
            with patch('sdx_topology_validator.topology_validator.get_validator_schema', \
                       return_value=sample_openapi_spec['paths']['/validator']['post']['requestBody']['content']['application/json']['schema']):
                result = validate(invalid_data)
                assert result == {"result": "Validation Error: 'property1' is a required property", "status_code": 400}
