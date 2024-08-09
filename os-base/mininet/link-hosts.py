#!/usr/bin/python
"""

Changing to use two controller for the SDX environment

SAX will be one switch and it will have its own controller
TENET will be one switch and it will have its own controller
AmLight will have multiple switches and it will have its own controller

Custom topology for AmLight/AMPATH
@author: Italo Valcy <italo@amlight.net>
@author: Renata Frez <renata.frez@rnp.br>

"""
import sys

import mininet.clean as Cleanup
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController


def custom_topo(amlight_ctlr, sax_ctlr, tenet_ctlr):
    """Create AmLight network for tests"""
    # net = Mininet(topo=None, build=False)
    net = Mininet(topo=None, build=False, controller=RemoteController, switch=OVSSwitch)

    # ********************************************** TENET OXP - Start ************************************************
    TenetController = net.addController(
        "tenet_ctrl", controller=RemoteController, ip=tenet_ctlr, port=6653
    )
    TenetController.start()

    tenet_sw1 = net.addSwitch("Novi06", listenPort=6701, dpid="dd00000000000006")
    tenet_sw2 = net.addSwitch("Novi07", listenPort=6702, dpid="dd00000000000007")
    tenet_sw3 = net.addSwitch("Novi08", listenPort=6703, dpid="dd00000000000008")

    net.addLink(tenet_sw1, tenet_sw2, port1=8, port2=8)
    net.addLink(tenet_sw2, tenet_sw3, port1=9, port2=9)

    h3 = net.addHost("INT03", mac="00:00:00:00:00:33")
    h4 = net.addHost("INT04", mac="00:00:00:00:00:44")

    net.addLink(h3, tenet_sw2, port1=33, port2=33)
    net.addLink(h4, tenet_sw3, port1=44, port2=44)

    # ************************************************ TENET OXP - End ************************************************

    # ************************************************ SAX OXP - Start ************************************************
    SaxController = net.addController(
        "sax_ctrl", controller=RemoteController, ip=sax_ctlr, port=6653
    )
    SaxController.start()

    sax_sw1 = net.addSwitch("Novi04", listenPort=6801, dpid="cc00000000000004")
    sax_sw2 = net.addSwitch("Novi05", listenPort=6802, dpid="cc00000000000005")

    net.addLink(sax_sw1, sax_sw2, port1=6, port2=6)

    # ************************************************ SAX OXP - End ************************************************

    # ******************************************** AmLight OXP - Start **********************************************
    AmLightController = net.addController(
        "amlight_ctrl", controller=RemoteController, ip=amlight_ctlr, port=6653
    )
    AmLightController.start()

    ampath_sw1 = net.addSwitch("Novi01", listenPort=6601, dpid="aa00000000000001")
    ampath_sw2 = net.addSwitch("Novi02", listenPort=6602, dpid="aa00000000000002")
    ampath_sw3 = net.addSwitch("Novi03", listenPort=6603, dpid="aa00000000000003")

    net.addLink(ampath_sw1, ampath_sw2, port1=2, port2=2)
    net.addLink(ampath_sw1, ampath_sw3, port1=3, port2=3)
    net.addLink(ampath_sw2, ampath_sw3, port1=5, port2=5)

    h1 = net.addHost("INT01", mac="00:00:00:00:00:11")
    h2 = net.addHost("INT02", mac="00:00:00:00:00:22")

    net.addLink(h1, ampath_sw1, port1=11, port2=11)
    net.addLink(h2, ampath_sw1, port1=22, port2=22)

    # ********************************************* AmLight OXP - End ************************************************

    # ********************************************** Inter-OXP links ***********************************************

    net.addLink(ampath_sw1, tenet_sw1, port1=1, port2=1)
    net.addLink(ampath_sw2, tenet_sw1, port1=3, port2=3)
    net.addLink(ampath_sw2, sax_sw1, port1=4, port2=4)
    net.addLink(ampath_sw3, tenet_sw2, port1=1, port2=1)
    net.addLink(sax_sw2, tenet_sw1, port1=7, port2=7)

    # Connect Ampath switches to AmLight controller
    ampath_sw1.start([AmLightController])
    ampath_sw2.start([AmLightController])
    ampath_sw3.start([AmLightController])

    # Connect Sax switches to Sax controller
    sax_sw1.start([SaxController])
    sax_sw2.start([SaxController])

    # Connect Tenet switches to Tenet controller
    tenet_sw1.start([TenetController])
    tenet_sw2.start([TenetController])
    tenet_sw3.start([TenetController])

    net.build()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")  # for CLI output
    # amlight_ctlr = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    amlight_ctlr = sys.argv[1] if len(sys.argv) > 1 else "192.168.0.2"
    # sax_ctlr = sys.argv[2] if len(sys.argv) > 2 else '0.0.0.0'
    sax_ctlr = sys.argv[2] if len(sys.argv) > 2 else "192.168.0.3"
    # tenet_ctlr = sys.argv[3] if len(sys.argv) > 3 else '0.0.0.0'
    tenet_ctlr = sys.argv[3] if len(sys.argv) > 3 else "192.168.0.4"
    custom_topo(amlight_ctlr, sax_ctlr, tenet_ctlr)
    Cleanup.cleanup()
#!/usr/bin/python
"""

Changing to use two controller for the SDX environment

SAX will be one switch and it will have its own controller
TENET will be one switch and it will have its own controller
AmLight will have multiple switches and it will have its own controller

Custom topology for AmLight/AMPATH
@author: Italo Valcy <italo@amlight.net>
@author: Renata Frez <renata.frez@rnp.br>

"""
