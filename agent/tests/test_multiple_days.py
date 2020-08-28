import time
import pytest

daytime = 15

def test_multiples_users(DemandBid, accounts):
    accounts[0].deploy(DemandBid, daytime)

    #Day 0
    prediction1 = 4200
    password1 = "there"
    prediction2 = 4100
    password2 = "there"
    prediction3 = 4200
    password3 = "there"
    bet1 = bytes(DemandBid[0].returnKeccak256OfEncoded(prediction1, password1))
    bet2 = bytes(DemandBid[0].returnKeccak256OfEncoded(prediction2, password2))
    bet3 = bytes(DemandBid[0].returnKeccak256OfEncoded(prediction3, password3))
    DemandBid[0].submitBet.transact(bet1, {'value':'5 ether','from': accounts[1]})
    DemandBid[0].submitBet.transact(bet2, {'value':'5 ether','from': accounts[2]})
    DemandBid[0].submitBet.transact(bet3, {'value':'5 ether','from': accounts[3]})

    #time.sleep(daytime*23/24)
    DemandBid[0].revealBet(prediction1, password1, {'from': accounts[1]})
    DemandBid[0].revealBet(prediction2, password2, {'from': accounts[2]})
    DemandBid[0].revealBet(prediction3, password3, {'from': accounts[3]})
    assert DemandBid[0].getTotalPot(0) == "15 ether"
    #time.sleep(daytime + daytime/24)
    time.sleep(daytime)

    #Day 1
    prediction4 = 3000
    password4 = "there"
    prediction5 = 3100
    password5 = "there"
    bet4 = bytes(DemandBid[0].returnKeccak256OfEncoded(prediction4, password4))
    bet5 = bytes(DemandBid[0].returnKeccak256OfEncoded(prediction5, password5))
    DemandBid[0].submitBet.transact(bet4, {'value':'5 ether','from': accounts[4]})
    DemandBid[0].submitBet.transact(bet5, {'value':'5 ether','from': accounts[5]})
    DemandBid[0].revealBet(prediction4, password4, {'from': accounts[4]})
    DemandBid[0].revealBet(prediction5, password5, {'from': accounts[5]})
    assert DemandBid[0].getTotalPot(0) == "15 ether"
    assert DemandBid[0].getTotalPot(1) == "10 ether"
    assert DemandBid[0].balance() == "25 ether"
    time.sleep(daytime)


    #Day 2
    DemandBid[0].setSettlementValue(4300, {'from': accounts[0]})
    DemandBid[0].calculateReward({'from': accounts[1]})
    DemandBid[0].calculateReward({'from': accounts[2]})
    DemandBid[0].calculateReward({'from': accounts[3]})
    time.sleep(daytime*4/24)
    DemandBid[0].withdraw({'from': accounts[1]})
    DemandBid[0].withdraw({'from': accounts[2]})
    assert DemandBid[0].getTotalPot(0) == "6 ether"
    assert DemandBid[0].getTotalPot(1) == "10 ether"
    time.sleep(daytime*20/24)


    #Day 3
    DemandBid[0].updateTotalPotFor2DaysAgoRound({'from': accounts[0]})
    assert DemandBid[0].getTotalPot(0) == "0 ether"
    assert DemandBid[0].getTotalPot(1) == "16 ether"
    assert DemandBid[0].balance() == "16 ether"
    DemandBid[0].setSettlementValue(3080, {'from': accounts[0]})
    DemandBid[0].calculateReward({'from': accounts[4]})
    DemandBid[0].calculateReward({'from': accounts[5]})
    time.sleep(daytime*4/24)
    DemandBid[0].withdraw({'from': accounts[4]})
    DemandBid[0].withdraw({'from': accounts[5]})
    assert accounts[1].balance() > "100 ether"
    assert accounts[1].balance() < "101 ether"
    assert accounts[2].balance() > "97 ether"
    assert accounts[2].balance() < "98 ether"
    assert accounts[3].balance() < "95 ether"
    assert accounts[4].balance() > "98 ether"
    assert accounts[4].balance() < "99 ether"
    assert accounts[5].balance() > "107 ether"
    assert DemandBid[0].getTotalPot(1) == "0 ether"
    assert DemandBid[0].balance() == "0 ether"
