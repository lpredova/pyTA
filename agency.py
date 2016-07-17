# coding=utf-8
# !/usr/bin/env python
import json
import sys
import time
from threading import Thread

import spade
from spade.ACLMessage import ACLMessage
from spade.Agent import Agent
from spade.Behaviour import Behaviour

from configuration_reader import ConfigurationReader


class AgencyAgent(Agent):
    class MakingOffer(Behaviour):
        msg = None

        def _process(self):
            self.msg = self._receive(True)

            if self.msg:
                request = json.loads(self.msg.content)
                if request['request_type'] == 'travel_request':
                    print "IMAM PONUDU OD"
                    print self.msg.content

                    # self.send_message(json.dumps({'request_type': 'games', 'data': None}))

                else:
                    pass

        def stop_agent(self):
            print "Agent is dying..."
            self.kill()
            sys.exit()

        def send_message(self, message):

            client = "traveler@127.0.0.1"
            address = "xmpp://" + client
            receiver = spade.AID.aid(name=client, addresses=[address])

            self.msg = ACLMessage()
            self.msg.setPerformative("inform")
            self.msg.setOntology("travel")
            self.msg.setLanguage("eng")
            self.msg.addReceiver(receiver)
            self.msg.setContent(message)

            self.myAgent.send(self.msg)
            print "\nMessage sent to: %s !" % client

    def _setup(self):
        print "\nTravel agency\t%s\tis up" % self.getAID().getAddresses()

        # template = ACLTemplate()
        # template.setOntology('booking')

        # behaviour = spade.Behaviour.MessageTemplate(template)
        # self.addBehaviour(self.MakingOffer(), behaviour)


def start_agency(agency_address):
    print "Starting agent"
    try:
        print "start"
        AgencyAgent(agency_address, 'travel').start()
        print "end"
        return None
    except Exception, e:
        print e


if __name__ == "__main__":

    # read config file and start agents in separate threads
    agencies_addresses = ConfigurationReader.read_agency_addresses()

    for agency_address in agencies_addresses:
        print agencies_addresses
        try:
            thread = Thread(target=start_agency(agency_address), args=agency_address)
            thread.daemon = True
            thread.start()
            time.sleep(2)
        except Exception, e:
            print "\nError while starting agencies!"
            print e.message
