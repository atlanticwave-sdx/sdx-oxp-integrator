# SDX-OXP-Integrator

The `sdx-oxp-integrator` is designed to simplify interactions with various OXPO (Open eXchange Point Operator) APIs by providing a streamlined programming interface. This integrator abstracts the complexities of direct API calls and offers a consistent method to interact with different OXPO services, enhancing code readability and maintainability.

## Key Features

### Unified API Calls
Standardize the way applications communicate with different OXPOs, regardless of their underlying API differences.

### Error Handling
Robust error handling mechanisms are built-in to manage API response variability and ensure reliable application behavior.

### Authentication Management
Handles all aspects of authentication automatically, from token generation to renewal, ensuring seamless access to OXPO services.

### Response Parsing
Automatically parses responses into user-friendly formats, reducing the need for repetitive parsing logic in the main application code.

### Extensibility
Easily extendible to accommodate new endpoints or changes in existing OXPO API specifications.

### Logging and Monitoring
Integrated logging for debugging and monitoring API interactions, facilitating easier troubleshooting and performance tracking.

## Getting Started

### Configuration
Copy the provided `.env` file and adjust it according to your environment.

### Building the Container Images
We have several container images. To build all container images, run the shell script files `1_build_kytos.sh` and `2_build_oxpos.sh`. From the project root directory, execute:

```sh
$ ./1_build_kytos.sh
$ ./2_build_oxpos.sh
```  

## Running with Docker Compose (Recommended)
A `docker-compose.yml` is provided for bringing up Ampath, SAX, Tenet, ampath-topology-conversion, sax-topology-conversion, tenet-topology-conversion, MongoDB, Mininet, and an Nginx instance. To start/stop the `sdx-oxp-integrator`, from the project root directory, run:

```sh
$ docker compose up
$ docker compose down
```  

### Navigate to http://localhost for testing the API.

## Running Unit Tests for Topology Conversion

# With Tox

You will need Docker installed and running. You will also need Tox and Tox-Docker. To activate a virtual environment, install the requirements, Tox, and Tox-Docker, run the script `piptst.sh`:

```sh
$ ./piptst.sh
```  

# With Pytest

If you prefer to avoid Tox and run Pytest directly, ensure Docker Compose is up. Set the required environment variables by running:

```sh
$ . export.sh
```  

To activate a virtual environment and install the requirements, run the script `piptst.sh`:

```sh
$ ./piptst.sh
```  

Then, run Pytest:

```sh
$ pytest
```  

## Integration Tests

### OXP Layer Test
Using hand-crafted inputs (OXP Test Input) to the OXP topology/provisioning system interface (REST API) to validate end-to-end services in the data plane.

#### FIU Input
The VLAN ranges on the two ports on an inter-domain link should be the same (pre-agreed upon by the admin). Validation checks are needed when adding topologies, and VLAN translation happens within a domain, simplifying VLAN assignment after the path is obtained.

### Middleware Layer Test
Using the AW-SDX Service data model (Service Test Input in JSON format) to the SDX-Controller service endpoint to validate if the middleware can satisfy the service request and generate the necessary breakdowns for the mock OXP systems.

### UI Layer Test
Using the Meican GUI to validate if it can generate the service data model as the input to the mock SD-Controller.

### Cross-layer Integration Tests
These tests play a crucial role in validating the functionality and interoperability of the AtlanticWave-SDX 2.0 system, focusing on interaction between the middleware and OXP systems.

#### Integration Test 1 - Middleware-OXP Cross-layer Test
The supported OXP system needs to publish the converted OXP topology to SDX-LC and update the topology via the `sdx-oxp-integrator` APIs. 
SDX-LC publishes this information into the SDX Message Queue, where it is received by the SDX Controller.

##### Precondition
A Docker Compose environment instantiates three Kytos OXPO servers: Ampath, SAX, and Tenet, and three SDX-LC servers: Ampath-LC, Sax-LC, and Tenet-LC. An SDX topology validator server and a MongoDB cluster are configured for communication.

##### Test Steps
Test commands and curl scripts for this integration test can be found at http://67.17.206.221/ as shown below:

![alt text](https://github.com/atlanticwave-sdx/sdx-oxp-integrator/blob/main/scripts/readme_images/all_commands.png)

On the swagger server, hit the blue **GET** button to execute a command. A box will appear as shown below:

![alt text](https://github.com/atlanticwave-sdx/sdx-oxp-integrator/blob/main/scripts/readme_images/template.png)

Hit the **TRY IT OUT** bottom and fill in the two required parameters **url** and **command**.
When the command is executed, a curl script command is provided to execute it from anywhere in a command prompt, as well as the server response.

###### Specific Tests Include:

# Get OXP Topology

## Get Ampath OXP Topology

- **URL:** `ampath.net`
- **Command:** `/topology`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Ftopology' -H 'accept: application/json'
```  

## Get SAX OXP Topology

- **URL:** `sax.net`
- **Command:** `/topology`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Ftopology' -H 'accept: application/json'
```  

## Get TENET OXP Topology

- **URL:** `tenet.ac.za`
- **Command:** `/topology`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Ftopology' -H 'accept: application/json'
```  
**Expected Outcome**
A `200 OK` API status is expected from all three OXPO servers. Any other status indicates that the environment is not pre-initialized to work with Kytos and further troubleshooting is needed before continuing.

# Get all switches of an OXPO 

## Get all Ampath OXPO Switches

- **URL:** `ampath.net`
- **Command:** `/switches`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Fswitches' -H 'accept: application/json'
```  

## Get all SAX OXPO Switches

- **URL:** `sax.net`
- **Command:** `/switches`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Fswitches' -H 'accept: application/json'
```  

## Get all TENET OXPO Switches

- **URL:** `tenet.ac.za`
- **Command:** `/switches`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Fswitches' -H 'accept: application/json'
```  

# Get all Interfaces of an OXPO 

## Get all Ampath OXPO Interfaces

- **URL:** `ampath.net`
- **Command:** `/interfaces`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Finterfaces' -H 'accept: application/json'
```  

## Get all SAX OXPO Interfaces

- **URL:** `sax.net`
- **Command:** `/interfaces`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Finterfaces' -H 'accept: application/json'
```  

## Get all TENET OXPO Interfaces

- **URL:** `tenet.ac.za`
- **Command:** `/interfaces`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Finterfaces' -H 'accept: application/json'
```  

# Get all Links of an OXPO  

## Get all Ampath OXPO Links

- **URL:** `ampath.net`
- **Command:** `/links`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Flinks' -H 'accept: application/json'
```  

## Get all SAX OXPO Links

- **URL:** `sax.net`
- **Command:** `/links`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Flinks' -H 'accept: application/json'
```  

## Get all TENET OXPO Links

- **URL:** `tenet.ac.za`
- **Command:** `/links`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Flinks' -H 'accept: application/json'
```  

# Get all EVCs of an OXPO  

## Get all Ampath OXPO EVCs

- **URL:** `ampath.net`
- **Command:** `/evcs`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Fevcs' -H 'accept: application/json'
```  

## Get all SAX OXPO EVCs

- **URL:** `sax.net`
- **Command:** `/evcs`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Fevcs' -H 'accept: application/json'
```  

## Get all TENET OXPO EVCs

- **URL:** `tenet.ac.za`
- **Command:** `/evcs`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Fevcs' -H 'accept: application/json'
```  

# Get OXPO Converted SDX Topology

## Get Ampath OXPO Converted SDX Topology

- Ensure Kytos is operational in the Ampath OXPO server and a topology has been created.
- **URL:** `ampath.net`
- **Command:** `/sdx/topology`
- **curl script command provided:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Fsdx%2Ftopology' -H 'accept: application/json'
```
The following image shows the result for this case:

![alt text](https://github.com/atlanticwave-sdx/sdx-oxp-integrator/blob/36-update-readme/scripts/readme_images/example_sdx_topology.png)

## Get SAX OXPO Converted SDX Topology

- Validate functionality in the SAX OXP.
- **URL:** `sax.net`
- **Command:** `/sdx/topology`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Fsdx%2Ftopology' -H 'accept: application/json'
```  

## Get TENET OXPO Converted SDX Topology

- Verify the presence of a well-established topology in the Tenet OXP.
- **URL:** `tenet.ac.za`
- **Command:** `/sdx/topology`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Fsdx%2Ftopology' -H 'accept: application/json'
```  

# Enable all Switches, Interfaces and Links 

## Enable all Switches, Interfaces and Links on Ampath OXPO

- **URL:** `ampath.net`
- **Command:** `/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Fenable%2Fall' -H 'accept: application/json'
```  

## Enable all Switches, Interfaces and Links on SAX OXPO

- **URL:** `sax.net`
- **Command:** `/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Fenable%2Fall' -H 'accept: application/json'
```  

## Enable all Switches, Interfaces and Links on TENET OXPO

- **URL:** `tenet.ac.za`
- **Command:** `/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Fenable%2Fall' -H 'accept: application/json'
```  

# Enable all switches 

## Enable all switches on Ampath OXPO

- **URL:** `ampath.net`
- **Command:** `/switch/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Fswitch%2Fenable%2Fall' -H 'accept: application/json'
```  

## Enable all switches on SAX OXPO

- **URL:** `sax.net`
- **Command:** `/switch/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Fswitch%2Fenable%2Fall' -H 'accept: application/json'
```  

## Enable all switches on TENET OXPO

- **URL:** `tenet.ac.za`
- **Command:** `/switch/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Fswitch%2Fenable%2Fall' -H 'accept: application/json'
```  

# Enable all Interfaces 

## Enable all Interfaces on Ampath OXPO

- **URL:** `ampath.net`
- **Command:** `/interface/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Finterface%2Fenable%2Fall' -H 'accept: application/json'
```  

## Enable all Interfaces on SAX OXPO

- **URL:** `sax.net`
- **Command:** `/interface/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Finterface%2Fenable%2Fall' -H 'accept: application/json'
```  

## Enable all Interfaces on TENET OXPO

- **URL:** `tenet.ac.za`
- **Command:** `/interface/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Finterface%2Fenable%2Fall' -H 'accept: application/json'
```  

# Enable all Links 

## Enable all Links on Ampath OXPO

- **URL:** `ampath.net`
- **Command:** `/link/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Flink%2Fenable%2Fall' -H 'accept: application/json'
```  

## Enable all Links on SAX OXPO

- **URL:** `sax.net`
- **Command:** `/link/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Flink%2Fenable%2Fall' -H 'accept: application/json'
```  

## Enable all Links on TENET OXPO

- **URL:** `tenet.ac.za`
- **Command:** `/link/enable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Flink%2Fenable%2Fall' -H 'accept: application/json'
```  

# Enable all EVCs 

## Enable all EVCs on Ampath OXPO

- **URL:** `ampath.net`
- **Command:** `/evc/enable`
- **curl script command:**
```sh
curl -X 'POST' 'http://67.17.206.221/ampath.net%2Fevc%2Fenable' -H 'accept: application/json'
```  

## Enable all EVCs on SAX OXPO

- **URL:** `sax.net`
- **Command:** `/evc/enable`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Fevc%2Fenable' -H 'accept: application/json'
```  

## Enable all EVcs on TENET OXPO

- **URL:** `tenet.ac.za`
- **Command:** `/evc/enable`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Fevc%2Fenable' -H 'accept: application/json'
```  

# Enable all EVC VLANs 

## Enable all EVC VLANs on Ampath OXPO

- **URL:** `ampath.net`
- **Command:** `/evc/vlan/enable`
- **curl script command:**
```sh
curl -X 'POST' 'http://67.17.206.221/ampath.net%2Fevc%2Fvlan%2Fenable' -H 'accept: application/json'
```  

## Enable all EVC VLANs on SAX OXPO

- **URL:** `sax.net`
- **Command:** `/evc/enable`
- **curl script command:**
```sh
curl -X 'POST' 'http://67.17.206.221/sax.net%2Fevc%2Fvlan%2Fenable' -H 'accept: application/json'
```  

## Enable all EVC VLANs on TENET OXPO

- **URL:** `tenet.ac.za`
- **Command:** `/evc/vlan/enable`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Fevc%2Fvlan%2Fenable' -H 'accept: application/json'
```  

# Disable all Switches, Interfaces and Links 

## Disable all Switches, Interfaces and Links on Ampath OXPO

- **URL:** `ampath.net`
- **Command:** `/disable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/ampath.net%2Fdisable%2Fall' -H 'accept: application/json'
```  

## Disable all Switches, Interfaces and Links on SAX OXPO

- **URL:** `sax.net`
- **Command:** `/disable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/sax.net%2Fdisable%2Fall' -H 'accept: application/json'
```  

## Disable all Switches, Interfaces and Links on TENET OXPO

- **URL:** `tenet.ac.za`
- **Command:** `/disable/all`
- **curl script command:**
```sh
curl -X 'GET' 'http://67.17.206.221/tenet.ac.za%2Fdisable%2Fall' -H 'accept: application/json'
```  

![alt text](https://github.com/atlanticwave-sdx/sdx-oxp-integrator/blob/main/scripts/readme_images/oxp_topology.png?raw=true)
