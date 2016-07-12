# coding=utf-8
# !/usr/bin/env python
import json

import spade
from spade.ACLMessage import ACLMessage
from spade.Agent import Agent
from spade.Behaviour import ACLTemplate, MessageTemplate, Behaviour


class TravelerAgent(Agent):
    class BookingSettings(Behaviour):

        def _process(self):
            self.msg = self._receive(True)
            if self.msg:
                request = json.loads(self.msg.content)
                if request['request_type'] == 'games':
                    self.games = request['data']
                if request['request_type'] == 'game_evaluation':
                    self.games = request['data']

        def set_preferences(self):

            preferences = {'request_type': 'bet', 'number_of_teams': 3}
            self.send_message(json.dumps(preferences))

        def send_message(self, content):

            master_agent = spade.AID.aid(name="bookie@127.0.0.1", addresses=["xmpp://agency@127.0.0.1"])
            self.msg = ACLMessage()
            self.msg.setPerformative("inform")
            self.msg.setOntology("travel")
            self.msg.setLanguage("eng")
            self.msg.addReceiver(master_agent)
            self.msg.setContent(content)
            self.myAgent.send(self.msg)
            print 'Message %s sent to agency' % content

    def _setup(self):
        print "\n Agent\t" + self.getAID().getName() + " is up"

        feedback_template = ACLTemplate()
        feedback_template.setOntology('travel')

        mt = MessageTemplate(feedback_template)
        settings = self.BookingSettings()
        self.addBehaviour(settings, mt)

        '''
        Agent feels like going somewhere (i.e Asia,Russia) and asks agencies to make an offer
        Ask for initial offer, then select based on current MOOD(price,distance)... and ask for discount, if right then accept offer and say tnx to other agencies
        '''

        #settings.send_message(json.dumps({'request_type': 'games'}))
        settings.set_preferences()
        settings.make_inqury()


if __name__ == '__main__':
    p = TravelerAgent('traveler@127.0.0.1', 'traveler')
    p.start()
