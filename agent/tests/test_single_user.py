import time
import pytest

daytime = 5

def test_single_user(DemandBid, accounts):
    #Setting phase
    assert accounts[0].balance() == "100 ether"
    assert accounts[1].balance() == "100 ether"
    assert len(accounts) == 10
    accounts[0].deploy(DemandBid, daytime)
    assert accounts[0].balance() < "100 ether"
    assert accounts[1].balance() == "100 ether"
    assert DemandBid[0].balance() == "0 ether"

    #Submit bet phase
    prediction = 4200
    password = "there"
    bet = bytes(DemandBid[0].returnKeccak256OfEncoded(prediction, password))
    DemandBid[0].submitBet.transact(bet, {'value':'5 ether','from': accounts[1]})
    assert DemandBid[0].balance() == "5 ether"
    assert accounts[1].balance() < "95 ether"
    #time.sleep(daytime*23/24)

    #Reveal bet phase
    DemandBid[0].revealBet(prediction, password, {'from': accounts[1]})
    assert DemandBid[0].getRevealedBet({'from': accounts[1]}) == True;
    assert DemandBid[0].getHash() == "0x4cb4505a52771700b35b3d7f151080a1222b4f6d3bb3a796c367c6380a71e2cd"
    #time.sleep(daytime + daytime/24)
    time.sleep(2*daytime)

    #Set settlement phase
    DemandBid[0].setSettlementValue(4200, {'from': accounts[0]})
    assert DemandBid[0].getSettlementValue(0, {'from': accounts[1]}) == "4200"

    #Calculate reward phase
    DemandBid[0].calculateReward({'from': accounts[1]})
    assert DemandBid[0].getRewardAmount(0,{'from': accounts[1]}) == "5 ether"
    assert DemandBid[0].balance() == "5 ether"
    assert accounts[1].balance() < "95 ether"
    time.sleep(daytime*4/24)

    #Withdraw phase
    DemandBid[0].withdraw({'from': accounts[1]})
    assert DemandBid[0].balance() == "0 ether"
    assert accounts[1].balance() > "99 ether"
