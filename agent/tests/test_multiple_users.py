import time
import pytest

daytime = 5

def test_multiples_users(DemandBid, accounts):
    #Setting phase
    accounts[0].deploy(DemandBid, daytime)

    #Submit bet phase
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
    assert DemandBid[0].balance() == "15 ether"
    #time.sleep(daytime*23/24)

    #Reveal bet phase
    DemandBid[0].revealBet(prediction1, password1, {'from': accounts[1]})
    assert DemandBid[0].getRevealedBet({'from': accounts[1]}) == True;
    DemandBid[0].revealBet(prediction2, password2, {'from': accounts[2]})
    assert DemandBid[0].getRevealedBet({'from': accounts[2]}) == True;
    DemandBid[0].revealBet(prediction3, "three", {'from': accounts[3]})
    assert DemandBid[0].getRevealedBet({'from': accounts[3]}) == False;
    #time.sleep(daytime + daytime/24)
    time.sleep(2*daytime)

    #Set settlement phase
    DemandBid[0].setSettlementValue(4400, {'from': accounts[0]})


    #Calculate reward phase
    DemandBid[0].calculateReward({'from': accounts[1]})
    DemandBid[0].calculateReward({'from': accounts[2]})
    DemandBid[0].calculateReward({'from': accounts[3]})
    time.sleep(daytime*4/24)

    #Withdraw phase
    assert DemandBid[0].balance() == "15 ether"
    DemandBid[0].withdraw({'from': accounts[1]})
    assert DemandBid[0].balance() == "0 ether"
    DemandBid[0].withdraw({'from': accounts[2]})
    DemandBid[0].withdraw({'from': accounts[3]})
    assert DemandBid[0].getRewardAmount(0,{'from': accounts[1]}) == "15 ether"
    assert DemandBid[0].getRewardAmount(0,{'from': accounts[2]}) == "0 ether"
    assert DemandBid[0].getRewardAmount(0,{'from': accounts[3]}) == "0 ether"
    assert accounts[1].balance() > "109 ether"
    assert accounts[1].balance() < "110 ether"
    assert accounts[2].balance() < "95 ether"
    assert accounts[3].balance() < "95 ether"
