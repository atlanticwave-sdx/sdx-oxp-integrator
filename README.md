# sdx-oxp-integrator

Designed to simplify interactions with various OXPO (Open eXchange Point Operator) APIs by providing a unified and simplified programming interface. The wrapper abstracts the complexities of direct API calls and offers a consistent method to interact with different OXPO services, enhancing code readability and maintainability.

## Key Features

## Unified API Calls
Standardize the way applications communicate with different OXPOs, regardless of their underlying API differences.

## Error Handling
Robust error handling mechanisms are built in to manage API response variability and ensure reliable application behavior.

## Authentication Management
Handles all aspects of authentication automatically, from token generation to renewal, ensuring seamless access to OXPO services.

## Response Parsing
Automatically parses responses into user-friendly formats, reducing the need for repetitive parsing logic in the main application code.

## Extensibility
Easily extendible to accommodate new endpoints or changes in existing OXPO API specifications.

## Logging and Monitoring
Integrated logging for debugging and monitoring API interactions, facilitating easier troubleshooting and performance tracking.  


## Running oxpo-api-wrapper  
### Configuration  
Copy the provided `.env` file, and adjust it according to your environment.  
### Building the container images  
We have several container images. Need to run the shell script files `1_build_kytos.sh` and `2_build_oxpos.sh` to build all container images. For running the scripts, from the project root directory, do:  

```console
$ ./1_build_kytos.sh
$ ./2_build_oxpos.sh
```  

### Running with Docker Compose (recommended)  
A `docker-compose.yml` is provided for bringing up amlight, sax, tenet, ampath-topology-conversion, sax-topology-conversion, tenet-topology-conversion, MongoDB, mininet and nginx instance.  
To start/stop oxpo-api-wrapper, from the project root directory, do:  

```console
$ docker compose up 
$ docker compose down
```  

Navigate to http://localhost for testing the API.  

## Running the unit tests for topology-conversion  
Before runnning the tests, make sure you are in the `topology-conversion` directory.  

### With tox  

You will need Docker installed and running. You will also need [tox]
and [tox-docker].  

For activating a virtual environment, installing the requirements, tox and tox-docker, run the script `piptst.sh`: 

```
$ ./piptst.sh
```  

Once you have `tox` and `tox-docker` installed, you can run tests:

```console
$ tox
```  

### With pytest  
If you want to avoid tox and run [pytest] directly, that is possible too. You will need to have docker compose up.  

Some environment variables are expected to be set for the tests to work as expected, for setting the required environment variables do:  
```
$ . export.sh
```  

For activating a virtual environment and installing the requirements, run the script `piptst.sh`:  
```
$ ./piptst.sh
```  

For runnning `pytest`:  
```
$ pytest
```  

<!-- References -->  

[tox]: https://tox.wiki/en/latest/
[tox-docker]: https://tox-docker.readthedocs.io/
[pytest]: https://docs.pytest.org/
