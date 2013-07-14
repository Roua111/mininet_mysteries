#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node improt CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel


class LinearTopo(Topo):
    "Linear topology of k switches, with one host per switch."
    def __init__(self, k=2, **opts):
        """Init.
        k = number of switches(and hosts)
        hconf: host configuration options
        lconf: link configuration options"""
        
        super(LinearTopo, self).__init__(**opts)
        self.k = k
        
        lastSwitch = None
        for i in irange(1,k):
            host = self.addHost('h%s' % i, cpu=0.5/k)
            switch = self.addSwitch('s%s' %i)
            self.addLink(host, switch, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
            if lastSwitch:
                self.addLink(switch, lastSwitch, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
            lastSwitch = switch
            
def simpleTest():
    "Create and test a simple network"
    topo = LinearTopo(k=4)
    net = Mininet(topo)
    net.start()
    print "Dmping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivitiy"
    net.pingAll()
    print "Testing bandwidht between h1 and h4"
    h1, h4 = newt.get('h1', 'h4')
    net.iperf((h1,h4))
    net.stop()
    
if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()
