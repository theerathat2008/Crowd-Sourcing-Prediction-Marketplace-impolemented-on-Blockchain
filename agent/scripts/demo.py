from brownie import accounts, DemandBid
from .agent import Agent, Oracle

def main():
    daytime = 20
    oracle = None
    agents = []
    rounds = 10
    settlements = [101643, 99419, 100924, 92123, 98228, 96530, 97947, 96135, 94158, 97995]

    for i in range(6):
        if i == 0:
            oracle = Oracle(0, "oracle", daytime, rounds, settlements)
        else:
            agents.append(Agent(i, "agent{0}".format(i), daytime, rounds))

    accounts[0].deploy(DemandBid, daytime)
    oracle.start()
    for agent in agents:
        agent.start()
