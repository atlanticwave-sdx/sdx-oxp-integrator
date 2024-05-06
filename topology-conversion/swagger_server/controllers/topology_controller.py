import requests
import logging
import connexion
from flask import render_template
from topology-conversion.controllers.convert_topology import ParseConvertTopology

logger = logging.getLogger(__name__)

def get_kytos_topology():
    kytos_topology_url = "http://67.17.206.221:8181/api/kytos/topology/v3/"
    response = requests.get(kytos_topology_url)
    if response.status_code == 200:
        kytos_topology = response.json()
        result = kytos_topology["topology"]
        return result
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

def convert_topology():
    try:
        topology_converted = ParseConvertTopology(
            topology=get_kytos_topology(),
            version= 1,
            timestamp='2024-05-01T11:13:05Z',
            model_version='2.0.0',
            oxp_name='Ampath-OXP',
            oxp_url='ampath.net',
            ).parse_convert_topology()
        return {"result": topology_converted, "status_code": 200}
    except Exception as err:
        logger.info("validation Error, status code 401:", err)
        return {"result": "Validation Error", "status_code": 401}

'''
def validate_sdx_topology():
    try:
        sdx_topology_validator = "http://localhost:8000/validator/v1/validate"
        response = requests.post(
                sdx_topology_validator,
                json={},
                timeout=10)
    except ValueError as exception:
        logger.info("validate topology result %s %s", exception, 401)
        raise HTTPException(
                401,
                detail=f"Path is not valid: {exception}"
            ) from exception
    result = response.json()
    return {"result": result, "status_code": response.status_code}
'''
