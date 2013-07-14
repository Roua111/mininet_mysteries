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
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1=0, linkopts2=0, linkopts3=0, fanout=3, depth=3, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        
        self.hosts = []
        self.hostCount = 27
        self.core = 1
        self.edgeCount = 9
        self.edges = []
        self.aggrCount = 3
        self.aggrs = []
        self.depth = depth
        self.createNetwork()
        
        
   
        
    def createHosts(self):
        for i in range (self.hostCount):
            self.hosts.append(self.addHost('h%s' % str(i+1)))
    
    def createEdges(self):
        for i in range (self.edgeCount):
            self.edges.append(self.addSwitch('e%s' % str(i+1)))
            
    def createAggrs(self):
        for i in range (self.aggrCount):
            self.aggrs.append(self.addSwitch('a%s' % str(i+1)))
            
    
    
    def linkHosts(self):
        for anEdge in self.edges:
            hostCount = 0
            for aHost in self.hosts:
                if hostCount < 3:
                    self.addLink(aHost, anEdge)
                else:
                    break
                hostCount += 1
                
    def linkAggregators(self):
        core = self.addSwitch('c1')
        for anAggr in self.aggrs:
            self.addLink(core, anAggr)
            edgeCount = 0
            for anEdge in self.edges:
                if edgeCount < 3:
                    self.addLink(anAggr, anEdge)
                else:
                    break
                edgeCount += 1
        return core
        

    def createNetwork(self):
        self.createHosts()    
        self.createEdges()
        self.createAggrs()
        self.linkHosts()
        return self.linkAggregators()
        
        
    def addTree( self, depth, fanout):
        isSwitch = depth > 0
        
       
        if isSwitch:
            print "Depth: " + str(depth)
            node = self.addSwitch('s%s' % self.edgeNum)
            self.edgeNum += 1
            for _ in range (fanout): 
                child = self.addTree(depth-1, fanout)
                self.addLink(node, child)
        else:
            node = self.addHost('h%s' % self.hostNum)
            self.hostNum += 1
        return node
            
if __name__ == '__main__':
    setLogLevel('info')
    topo = CustomTopo()
    print str(type(topo))
    network = Mininet(topo)
    network.start()
    network.stop()
