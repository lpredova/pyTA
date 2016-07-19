# coding=utf-8
# !/usr/bin/env python
import json

import spade
from spade.ACLMessage import ACLMessage
from spade.Agent import Agent, random, os
from spade.Behaviour import ACLTemplate, MessageTemplate, Behaviour

from configuration_reader import ConfigurationReader


class TravelerAgent(Agent):
    class Travel(Behaviour):

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        config_file = BASE_DIR + 'agency_config.json'

        msg = None
        agencies_counter = ConfigurationReader.number_of_agencies()
        offer_responses = 0
        offers = []

        destination = random.choice(['Europe', 'Australia', 'Asia', 'America'])

        def _process(self):
            self.msg = self._receive(True)
            if self.msg:
                request = json.loads(self.msg.content)
                if request['request_type'] == 'offer_response':

                    self.offer_responses += 1
                    self.offers.append(request)

                    if self.offer_responses >= self.agencies_counter:
                        # TODO check num of persons and which is in budget then send it request for discount
                        for offer in self.offers:
                            for o in offer["data"]:
                                print o["name"]

                                travel = {'request_type': 'discount_request', 'travel_id': o["name"]}
                                self.send_message(json.dumps(travel), offer["origin"])

                if request['request_type'] == 'discount_response':
                    print "OK NEMA POPUSTA"

        def set_preferences(self):
            print "Hmmm, I'd like to go to: %s" % self.destination
            travel = {'request_type': 'travel_request', 'destination': self.destination}
            self.send_message_all(json.dumps(travel))

        def send_message_all(self, content):

            agencies_ids = ConfigurationReader.read_agency_id()
            for agency_id in agencies_ids:
                address = "agency%i@127.0.0.1" % agency_id
                agent = spade.AID.aid(name=address, addresses=["xmpp://%s" % address])

                self.msg = ACLMessage()
                self.msg.setPerformative("inform")
                self.msg.setOntology("travel")
                self.msg.setLanguage("eng")
                self.msg.addReceiver(agent)
                self.msg.setContent(content)
                self.myAgent.send(self.msg)
                print 'Message %s sent to %s' % (content, address)

        def send_message(self, content, address):

            agent = spade.AID.aid(name=address, addresses=["xmpp://%s" % address])
            self.msg = ACLMessage()
            self.msg.setPerformative("inform")
            self.msg.setOntology("travel")
            self.msg.setLanguage("eng")
            self.msg.addReceiver(agent)
            self.msg.setContent(content)
            self.myAgent.send(self.msg)
            print 'Message %s sent to %s' % (content, address)

    def _setup(self):
        print "\n Agent\t" + self.getAID().getName() + " is up"

        feedback_template = ACLTemplate()
        feedback_template.setOntology('travel')

        mt = MessageTemplate(feedback_template)
        settings = self.Travel()
        self.addBehaviour(settings, mt)
        settings.set_preferences()


if __name__ == '__main__':
    '''
        Agent feels like going somewhere (i.e Asia,Russia) and asks agencies to make an offer
        Ask for initial offer, then select based on current MOOD(price,distance)... and ask for discount, if right then accept offer and say tnx to other agencies
        '''
    TravelerAgent('traveler@127.0.0.1', 'traveler').start()
