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
        destination = random.choice(
            ['Europe', 'Russia', 'Asia', 'Africa', 'America', 'Middle East', 'Dubai', 'Australia'])

        def _process(self):
            self.msg = self._receive(True)
            if self.msg:
                request = json.loads(self.msg.content)
                if request['request_type'] == 'games':
                    self.games = request['data']
                if request['request_type'] == 'game_evaluation':
                    self.games = request['data']

        def set_preferences(self):
            print "Hmmm, I'd like to go to: %s" % self.destination
            travel = {'request_type': 'travel_request', 'destination': self.destination}
            self.send_message(json.dumps(travel))

        def send_message(self, content):

            agencies_addresses = ConfigurationReader.read_agency_addresses()
            for address in agencies_addresses:
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

        '''
        Agent feels like going somewhere (i.e Asia,Russia) and asks agencies to make an offer
        Ask for initial offer, then select based on current MOOD(price,distance)... and ask for discount, if right then accept offer and say tnx to other agencies
        '''

        # settings.send_message(json.dumps({'request_type': 'games'}))
        settings.set_preferences()


if __name__ == '__main__':
    p = TravelerAgent('traveler@127.0.0.1', 'traveler')
    p.start()
