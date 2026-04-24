from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSBridge
import time

# --------------------------------
# Topology still has 3 hosts
# --------------------------------

class HostDiscoveryTopo(Topo):

    def build(self):

        s1 = self.addSwitch('s1')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)


host_db = {}


# Initial discovery only h1 and h2
def initial_discovery(net):

    print("\nDetecting Initial Hosts...\n")

    for host in net.hosts:
        if host.name != 'h3':
            host_db[host.name] = host.IP()


def display_hosts():

    print("Host Database:\n")

    for h in host_db:
        print(h,"->",host_db[h])


# Dynamic update adds h3 later
def dynamic_update(net):

    print("\nHost Join Event Detected: h3")

    time.sleep(3)

    print("\nUpdating dynamically...\n")

    h3 = net.get('h3')

    host_db[h3.name] = h3.IP()


def main():

    topo = HostDiscoveryTopo()

    net = Mininet(
        topo=topo,
        switch=OVSBridge,
        controller=None
    )

    net.start()

    # Initial DB
    initial_discovery(net)

    display_hosts()

    # Dynamic update
    dynamic_update(net)

    print("\nUpdated Host Information:\n")

    display_hosts()

    print("\nTesting Connectivity")

    net.pingAll()

    net.stop()


if __name__=="__main__":
    main()
