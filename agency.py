# coding=utf-8
# !/usr/bin/env python
import json
import sys
import threading
import time

import spade
from spade.ACLMessage import ACLMessage
from spade.Agent import Agent
from spade.Behaviour import Behaviour, ACLTemplate

from configuration_reader import ConfigurationReader


class AgencyAgent(Agent):
    class MakingOffer(Behaviour):
        msg = None

        def _process(self):
            self.msg = self._receive(True)

            if self.msg:
                request = json.loads(self.msg.content)
                if request['request_type'] == 'travel_request':
                    results = ConfigurationReader.destination_finder(request['destination'], self.getName())
                    print results
                    print self.getName()
                    print "Agency %s has %i travels to offer" % (self.getName(), len(results))
                    if len(results) > 0:
                        for result in results:
                            print "%s - %i$ : %i persons, %i days" % (
                                result["name"], result["price"], result["persons"], result["days"])
                    else:
                        print "There are no destinations to desired location"

                    self.send_message(json.dumps(
                        {'request_type': 'offer_response', 'data': results, 'origin': self.getName().split(" ")[0]}))

                if request['request_type'] == 'discount_request':
                    self.send_message(json.dumps({'request_type': 'discount_response', 'data': "NO DISCOUNT",
                                                  'origin': self.getName().split(" ")[0]}))

                else:
                    pass

        def stop_agent(self):
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

        template = ACLTemplate()
        template.setOntology('travel')

        behaviour = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.MakingOffer(), behaviour)


def start_agency(agency_id):
    try:
        ip = "agency%i@127.0.0.1" % agency_id
        agency_name = "agency0%i" % agency_id

        agent = AgencyAgent(ip, agency_name)
        agent.start()

    except Exception, e:
        print e


if __name__ == "__main__":
    agencies_ids = ConfigurationReader.read_agency_id()
    for agency_id in agencies_ids:
        try:
            threading.Thread(target=start_agency(agency_id), args=None).start()
            time.sleep(1)
        except Exception, e:
            print "\nError while starting agencies!"
            print e.message
