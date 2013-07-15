#!/usr/bin/python

'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1=0, linkopts2=0, linkopts3=0, fanout=3, depth=3, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        
        self.hostCount = 27
        self.core = 1
        self.edgeCount = 9
        self.aggrCount = 3
        self.depth = depth
        self.createNetwork()
        
        
   

                
    def createNetwork(self):
        core = self.addSwitch('c1')
        edgeIndex = 0
        hostIndex = 0
        for aggrIndex in  range(self.aggrCount):
            anAggr = self.addSwitch('a%s' % str(aggrIndex+1))
            self.addLink(core, anAggr)
            while edgeIndex < self.edgeCount:
               
                anEdge = self.addSwitch('e%s' % str(edgeIndex+1))
                self.addLink(anEdge, anAggr)
                while hostIndex < self.hostCount:
                    aHost = self.addHost('h%s' % str(hostIndex+1))
                    self.addLink(aHost, anEdge)
                    hostIndex += 1
                    if hostIndex % 3 == 0:
                        break

                edgeIndex += 1
                if edgeIndex % 3 == 0:
                    break
        return core
        

            
if __name__ == '__main__':
    setLogLevel('info')
    topo = CustomTopo()
    print str(type(topo))
    network = Mininet(topo)
    network.start()
    network.stop()
