#!/usr/bin/python3
import time
from brownie import accounts, convert, DemandBid
from threading import Thread
import struct
import random

import requests

colour = "\033[1;30m"

class Agent(Thread):

    def __init__(self, num, password, daytime, rounds):
        Thread.__init__(self)
        self.num = num
        self.password = password
        self.daytime = daytime
        self.rounds = rounds
        self.prediction = None
        self.i = 0

    def get_prediction(self):
        if self.num == 1:
            headers = {
                'Content-Type': 'application/json',
            }
            data = '{"prediction_size": "10"}'
            response = requests.post('http://ec2-18-188-39-149.us-east-2.compute.amazonaws.com:80/predict', headers=headers, data=data)
            values = response.content.split()
            self.prediction = []
            for v in values:
                v = int(float(str(v, 'utf-8')) * 1000000)
                self.prediction.append(v)
        else:
            self.prediction = [2000000] * 10

    def submit_bet(self, n, amount):
        bet = bytes(DemandBid[0].returnKeccak256OfEncoded(self.prediction[n], self.password))
        eth_amount = '{0} ether'.format(amount)
        DemandBid[0].submitBet.transact(bet, {'value':eth_amount,'from':accounts[self.num]})

        print(colour,'Agent {0} submitted a bet of {1} for for prediction {2} on day {3}'.format(
            self.num, eth_amount, self.prediction[n], DemandBid[0].getCurrentDay()
        ))

    def reveal_bet(self, n):
        DemandBid[0].revealBet(self.prediction[n], self.password, {'from': accounts[self.num]})

        print(colour,'Agent {0} revealed their bet on day {1}'.format(self.num, DemandBid[0].getCurrentDay()))

    def calculate_reward(self):
        DemandBid[0].calculateReward({'from': accounts[self.num]})
        print(colour,'Agent {0} calculated reward on day {1}'.format(
            self.num, DemandBid[0].getCurrentDay()
        ))

    def receive_reward(self, day):
        reward = DemandBid[0].getRewardAmount(day, {'from': accounts[self.num]})
        DemandBid[0].withdraw({'from': accounts[self.num]})

        print(colour,'Agent {0} received their reward on day {1}'.format(
            self.num, DemandBid[0].getCurrentDay()
        ))
        # print('Agent {0} has balance {1}'.format(self.num, accounts[self.num].balance()))

    def run(self):
        day = 0
        self.get_prediction()
        # Day 0
        self.submit_bet(self.i, 5)

        time.sleep(self.daytime*12/24)
        self.reveal_bet(self.i)
        time.sleep(self.daytime*12/24)

        self.i += 1
        day += 1
        self.rounds -= 1

        # Day 1
        self.submit_bet(self.i, 5)
        time.sleep(self.daytime*12/24)
        self.reveal_bet(self.i)
        time.sleep(self.daytime*12/24)

        self.i += 1
        day += 1
        self.rounds -= 1

        while self.rounds:

            #Day 2
            time.sleep(self.daytime/24)
            self.calculate_reward()
            print()
            self.submit_bet(self.i, 5)
            time.sleep(self.daytime*8/24)
            self.receive_reward(day)
            time.sleep(self.daytime*3/24)
            self.reveal_bet(self.i)
            time.sleep(self.daytime*12/24)

            day += 1
            self.rounds -= 1
            self.i += 1


class Oracle(Agent):

    def __init__(self, num, password, daytime, rounds, settlements):
        assert num == 0
        Thread.__init__(self)
        self.num = num
        self.password = password
        self.daytime = daytime
        self.rounds = rounds
        self.i = 0
        self.settlements = settlements

    def set_settlement(self, settlement):
        DemandBid[0].setSettlementValue(settlement, {'from': accounts[0]})

        print(colour,'The oracle has set the settlement value at: {0}'.format(settlement))

    def run(self):
        time.sleep(self.daytime*2)
        while self.rounds and self.i < len(self.settlements):
            self.set_settlement(self.settlements[self.i])
            time.sleep(self.daytime)
            self.i += 1
            self.rounds -= 1
            time.sleep(self.daytime)
            DemandBid[0].updateTotalPotFor2DaysAgoRound({'from': accounts[0]})
