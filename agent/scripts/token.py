#!/usr/bin/python3
import time
from brownie import accounts, convert, DemandBid

import requests

headers = {
    'Content-Type': 'application/json'
}

data = {"dataset_size": "100"}


daytime = 5


def getPrediction(text):
    begin = 0
    end = len(text)


    for i in range(len(text)):

        if(text[i] == 91):
            begin = i+1
            break
    for j in range(begin,len(text)):
        if(text[j] == 32):
            end = j
            break



    return float(str(text[begin:end], 'utf-8'))

def main():
    accounts[0].deploy(DemandBid, daytime)
    response = requests.post('http://ec2-18-191-230-57.us-east-2.compute.amazonaws.com:80/predict')
    values = response.content
    prediction, actual, std_dev = values.split()
    print(prediction, std_dev)


    prediction = float(prediction) * 1000
    settlement = float(actual) * 1000
    print(prediction)
    password = "there"
    print("CurrentDay")
    print(DemandBid[0].getCurrentDay())
    bet = bytes(DemandBid[0].returnKeccak256OfEncoded(prediction, password))
    DemandBid[0].submitBet.transact(bet, {'value':'5 ether','from': accounts[1]})
    print('hash at submit')
    print(DemandBid[0].getHash())


    print("CurrentDay")
    print(DemandBid[0].getCurrentDay())
    DemandBid[0].revealBet(prediction, password, {'from': accounts[1]})

    print('revealDone')
    print(DemandBid[0].getRevealedBet())
    print('hash at reveal')
    print(DemandBid[0].getHash())




    #time.sleep(daytime/24)

    time.sleep(2*daytime)



    print("CurrentDay")
    print(DemandBid[0].getCurrentDay())

    DemandBid[0].setSettlementValue(settlement, {'from': accounts[0]})
    print('settlement')
    print(DemandBid[0].getSettlementValue(0))
    print('senderpredict')
    print(DemandBid[0].getSenderPrediction({'from': accounts[1]}))
    print("CurrentDay")
    print(DemandBid[0].getCurrentDay())

    DemandBid[0].calculateReward({'from': accounts[1]})
    print('result')
    print(DemandBid[0].getResult())


    time.sleep(daytime*3/24)

    DemandBid[0].withdraw({'from': accounts[1]})

    value = DemandBid[0].getRewardAmount(0, {'from': accounts[1]})
    print('After withdraw')
    print(value)

    print(DemandBid[0].balance())
    print(accounts[0].balance())
    print(accounts[1].balance())
