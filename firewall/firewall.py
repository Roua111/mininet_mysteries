'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
import csv



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
        self.deny = []
        with open(policyFile, "r") as csvfile:
            dictReader = csv.DictReader(csvfile)
            for connectionPair in dictReader:
                self.deny.append((EthAddr(connectionPair['mac_0']),EthAddr(connectionPair['mac_1'])))
                self.deny.append((EthAddr(connectionPair['mac_1']),EthAddr(connectionPair['mac_0'])))

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        for (src, dst) in self.deny:
            match = of.ofp_match()
            match.dl_src = src
            match.dl_dst = dst
            msg = of.ofp_flow_mod()
            msg.match = match
            event.connection.send(msg)
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))
        
def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
    
    
from pyretic.lib.corelib import *
from pyretic.lib.std import *
 
from pyretic.modules.mac_learner import mac_learner as act_like_switch
 
import csv, os
policy_file = "%s/pyretic/pyretic/examples/firewall-policies.csv" % os.environ[ 'HOME' ]
 
def main():
    # start with a policy that doesn't match any packets
    not_allowed = none
    # and add traffic that isn't allowed
    with open(policy_file, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            not_allowed = not_allowed + match(srcmac=MAC(row['mac_0']), dstmac=MAC(row['mac_1'])) + match(srcmac=MAC(row['mac_1']), dstmac=MAC(row['mac_0']))
 
    # express allowed traffic in terms of not_allowed - hint use '~'
    allowed = ~not_allowed
#    allowed = if_(not_allowed, drop, passthrough)
 
    # and only send allowed traffic to the mac learning (act_like_switch) logic
    return allowed >> act_like_switch()
    
