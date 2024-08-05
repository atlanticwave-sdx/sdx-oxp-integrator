"""
Main class of kytos/sdx_topology Kytos Network Application.

SDX API
"""

from controllers.operational_controller import get_oxp_links

class ParseConvertTopology:
    """Parse Topology  class of kytos/sdx_topology NApp."""

    def __init__(self, **args):
        self.kytos_topology = args["topology"]
        self.version = args["version"]
        self.timestamp = args["timestamp"]
        self.model_version = args["model_version"]
        self.oxp_name = args["oxp_name"]
        self.oxp_url = args["oxp_url"]
        self.topology_id = args["topology_id"]
        # mapping from Kytos to SDX and vice-versa
        self.kytos2sdx = {}
        self.sdx2kytos = {}

    def get_kytos_nodes(self) -> dict:
        """return parse_args["topology"]["switches"] values"""
        return self.kytos_topology["switches"].values()

    def get_port_status(self, port_status: str) -> str:
        """
        Convert port status to a consistent lower case format.

        Args:
            port_status (str): The status string to be converted.

        Returns:
            str: The converted status or "error" if not recognized.
        """
        status_map = {
            "UP": "up",
            "up": "up",
            "DOWN": "down",
            "down": "down",
        }
        return status_map.get(port_status, "error")

    def get_link_port_speed(self, speed: str) -> int:
        """
        Get the link port speed based on the speed string.

        Args:
            speed (str): The speed string to be converted to an integer value.

        Returns:
            int: The corresponding speed in Gbps or 0 if not found.
        """
        type_to_speed = {
            "400GE": 400,
            "100GE": 100,
            "50GE": 50,
            "40GE": 40,
            "25GE": 25,
            "10GE": 10,
            "50000000000": 400,
            "50000000000.0": 400,
            "12500000000": 100,
            "12500000000.0": 100,
            "6250000000": 50,
            "6250000000.0": 50,
            "5000000000": 40,
            "5000000000.0": 40,
            "3125000000": 25,
            "3125000000.0": 25,
            "1250000000": 10,
            "1250000000.0": 10,
        }
        return type_to_speed.get(speed, 0)

    @staticmethod
    def get_type_port_speed(speed: str) -> str:
        """Function to obtain the speed of a specific port type."""
        speed_to_type = {
            "400GE": "400GE",
            "50000000000": "400GE",
            "50000000000.0": "400GE",
            "100GE": "100GE",
            "12500000000": "100GE",
            "12500000000.0": "100GE",
            "50GE": "50GE",
            "6250000000": "50GE",
            "6250000000.0": "50GE",
            "40GE": "40GE",
            "5000000000": "40GE",
            "5000000000.0": "40GE",
            "25GE": "25GE",
            "3125000000": "25GE",
            "3125000000.0": "25GE",
            "10GE": "10GE",
            "1250000000": "10GE",
            "1250000000.0": "10GE",
        }

        return speed_to_type.get(speed, "Other")

    @staticmethod
    def get_status(status: bool) -> str:
        """Function to obtain the status."""
        return "up" if status else "down"

    @staticmethod
    def get_state(state: bool) -> str:
        """Function to obtain the state."""
        return "enabled" if state else "disabled"

    def get_port_urn(self, switch: str, interface) -> str:
        """function to generate the full urn address for a node"""

        if not isinstance(interface, str) and not isinstance(interface, int):
            raise ValueError("Interface is not the proper type")
        if interface == "" or switch == "":
            raise ValueError("Interface and switch CANNOT be empty")
        if isinstance(interface, int) and interface <= 0:
            raise ValueError("Interface cannot be negative")

        try:
            switch_name = self.get_kytos_nodes_names()[switch]
        except KeyError:
            switch_name = switch

        return f"urn:sdx:port:{self.oxp_url}:{switch_name}:{interface}"

    def get_port(self, sdx_node_name: str, interface: dict) -> dict:
        """
        Retrieve a network device's port (or interface) details.
        
        Args:
            sdx_node_name (str): The name of the SDX node.
            interface (dict): The interface data.
            
        Returns:
            dict: The processed SDX port with relevant attributes.
        """
        sdx_port = {
                "id": self.get_port_urn(sdx_node_name, interface["port_number"]),
                "name": interface["metadata"].get("port_name", "")[:30],
                "node": f"urn:sdx:node:{self.oxp_url}:{sdx_node_name}",
                "type": self.get_type_port_speed(str(interface["speed"])),
                "status": self.get_status(interface["active"]),
                "state": self.get_state(interface["enabled"]),
                "mtu": interface["metadata"].get("mtu", 1500),
                "nni": f"urn:sdx:link:{interface['metadata']['sdx_nni']}" \
                if "sdx_nni" in interface["metadata"] else ""
            }

        if not sdx_port["name"]:
            sdx_port["name"] = interface["name"][:30]

        vlan_range = interface["metadata"].get("sdx_vlan_range")
        if not vlan_range:
            vlan_range = interface.get("tag_ranges", [[1, 4095]])

        sdx_port["services"] = {
            "l2vpn-ptp": {"vlan_range": vlan_range}
        }

        return sdx_port

    def get_ports(self, sdx_node_name: str, interfaces: dict) -> list:
        """Function that calls the main individual get_port function,
        to get a full list of ports from a node/ interface"""
        ports = []
        for interface in interfaces.values():
            port_no = interface["port_number"]
            if port_no != 4294967294:
                ports.append(self.get_port(sdx_node_name, interface))
                self.kytos2sdx[interface["id"]] = ports[-1]["id"]
                self.sdx2kytos[ports[-1]["id"]] = interface["id"]

        return ports

    def get_kytos_nodes_names(self) -> dict:
        """retrieve the data_path attribute for every Kytos topology switch"""
        nodes_mappings = {}

        for node in self.get_kytos_nodes():
            if "node_name" in node["metadata"]:
                nodes_mappings[node["id"]] = node["metadata"]["node_name"]
            else:
                nodes_mappings[node["id"]] = node["data_path"]

        return nodes_mappings

    def get_sdx_node(self, kytos_node: dict) -> dict:
        """function that builds every Node dictionary object with all the
        necessary attributes that make a Node object; the name, id, location
        and list of ports."""
        sdx_node = {}

        if "node_name" in kytos_node["metadata"]:
            sdx_node["name"] = kytos_node["metadata"]["node_name"]
        else:
            sdx_node["name"] = kytos_node["data_path"]

        sdx_node["id"] = f"urn:sdx:node:{self.oxp_url}:{sdx_node['name']}"

        sdx_node["location"] = {
            "address": kytos_node["metadata"].get("address", ""),
            "latitude": float(kytos_node["metadata"].get("lat", 0)),
            "longitude": float(kytos_node["metadata"].get("lng", 0)),
            "iso3166_2_lvl4": kytos_node["metadata"].get("iso3166_2_lvl4", ""),
            "private": [],
        }

        sdx_node["ports"] = self.get_ports(sdx_node["name"], kytos_node["interfaces"])

        sdx_node["status"] = self.get_status(kytos_node["active"])
        sdx_node["state"] = self.get_state(kytos_node["enabled"])

        return sdx_node

    def get_sdx_nodes(self) -> list:
        """returns SDX Nodes list with every enabled Kytos node in topology"""
        sdx_nodes = []
        for kytos_node in self.get_kytos_nodes():
            if kytos_node["enabled"]:
                sdx_nodes.append(self.get_sdx_node(kytos_node))
        return sdx_nodes

    def get_sdx_link(self, kytos_link):
        """
        Generate a dictionary object for each link in the network, 
        containing all relevant attributes.

        Args:
            kytos_link (dict): The link data from the Kytos topology.

        Returns:
            dict: The processed SDX link with relevant attributes.
        """
        sdx_link = {}
        if 'endpoint_a' in kytos_link and 'endpoint_b' in kytos_link:
            endpoint_a_name = kytos_link['endpoint_a'].get('name', 'Unknown')
            endpoint_a_speed = kytos_link['endpoint_a'].get('speed', 0)
            endpoint_a_switch = kytos_link['endpoint_a'].get('name', '')
            endpoint_b_name = kytos_link['endpoint_b'].get('name', 'Unknown')
            endpoint_b_speed = kytos_link['endpoint_b'].get('speed', 0)
            endpoint_b_switch = kytos_link['endpoint_b'].get('name', '')

            port_prefix = f"urn:sdx:port:{self.oxp_url}:"
            endpoint_a_port = f"{port_prefix}{endpoint_a_switch.split('-')[0]}:{endpoint_a_switch}"
            endpoint_b_port = f"{port_prefix}{endpoint_b_switch.split('-')[0]}:{endpoint_b_switch}"

            sdx_link["name"] = f"{endpoint_a_name}_{endpoint_b_name}"
            sdx_link["id"] = f"urn:sdx:link:{self.oxp_url}:{endpoint_a_name}_{endpoint_b_name}"
            sdx_link["type"] = "intra"
            sdx_link["ports"] = [endpoint_a_port, endpoint_b_port]
            sdx_link["bandwidth"] = self.get_link_port_speed(str(min(endpoint_a_speed, endpoint_b_speed)))
            sdx_link["residual_bandwidth"] = 100
            sdx_link["packet_loss"] = 0
            sdx_link["latency"] = 2
            sdx_link["status"] = self.get_port_status(kytos_link["status"])
            sdx_link["state"] = "enabled" if kytos_link["enabled"] else "disabled"

        return sdx_link

    def get_sdx_links(self):
        """
        Get a list of SDX link objects based on the intra connections.

        Returns:
            list: A list of SDX link dictionaries.
        """
        sdx_links = []
        if "links" in self.kytos_topology:
            for kytos_link in self.kytos_topology["links"].values():
                sdx_link = self.get_sdx_link(kytos_link)
                sdx_links.append(sdx_link)
        return sdx_links

    def parse_convert_topology(self):
        """function get_sdx_topology"""
        topology = {}
        topology["name"] = self.oxp_name
        topology["id"] = self.topology_id
        topology["version"] = self.version
        topology["timestamp"] = self.timestamp
        topology["model_version"] = self.model_version
        topology["nodes"] = self.get_sdx_nodes()
        topology["links"] = self.get_sdx_links()
        topology["services"] = ["l2vpn-ptp"]
        return topology
