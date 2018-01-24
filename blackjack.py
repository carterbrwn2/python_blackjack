#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:29:41 2018

@author: carterbrown
"""

from random import shuffle

class Bank(object):
    
    def __init__(self, balance=0):
        self.balance = balance
        
    def subtract(self, amount):
        self.balance -= amount
        
    def add(self, amount):
        self.balance += amount
        
    def getBal(self):
        return self.balance

class Deck(object):
    suits = ['hearts', 'spades', 'clubs', 'diamonds']
    values = ['ACE', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'JACK', 'QUEEN', 'KING']
    
    def __init__(self, deck=[]):
        self.deck = deck
        
    def numOfCards(self):
        return len(self.deck)
    
    def createDeck(self):
        for suit in Deck.suits:
            for value in Deck.values:
                self.deck.append(value+' of '+suit)
                
    def printDeck(self):
        for card in self.deck:
            print(card)
            
    def clearDeck(self):
        self.deck = []
    
    def shuffle(self):
        shuffle(self.deck)
        
    def recreate(self):
        print('\nNot enough cards left to deal, re-creating deck and shuffling...\n')
        self.clearDeck()
        self.createDeck()
        self.shuffle()
        
    def canDraw(self):
        return len(self.deck) > 0
        
    def draw(self):
        if len(self.deck) > 0:
            card = self.deck.pop()
            value = 0
            if card[0] == 'A':
                value=11
            elif card[0] == '2':
                value=2
            elif card[0] == '3':
                value=3
            elif card[0] == '4':
                value=4
            elif card[0] == '5':
                value=5
            elif card[0] == '6':
                value=6
            elif card[0] == '7':
                value=7
            elif card[0] == '8':
                value=8
            elif card[0] == '9':
                value=9
            elif card[0] == '1':
                value=10
            elif card[0] == 'J' or card[0] == 'Q' or card[0] == 'K':
                value=10
            return (card, value)
        else:
            return ('EMPTY DECK', -1)
            
class Hand(object):
    def __init__(self, hand=[], handValue=0):
        self.hand=hand
        self.handValue=handValue

    def recCard(self, card):
        self.hand.append(card)
    
    def calcHand(self):
        self.handValue = 0
        if len(self.hand) > 0:
            aceCount=0
            value=0
            for card in self.hand:
                if card[0][0] == 'A':
                    aceCount+=1
                value+=card[1]
            if aceCount == 0:
                self.handValue = value
            else:
                if aceCount == 1:
                    if value>21:
                        value-=10
                if aceCount == 2:
                    if value>21:
                        value-=10
                        if value>21:
                            value-=10
                if aceCount == 3:
                    if value>21:
                        value-=10
                        if value>21:
                            value-=10
                            if value>21:
                                value-=10
                if aceCount == 4:
                    if value>21:
                        value-=10
                        if value>21:
                            value-=10
                            if value>21:
                                value-=10
                                if value>21:
                                    value-=10
                self.handValue = value
                
            return self.handValue
        else:
            return -1
    
    def clearHand(self):
        self.hand=[]
        self.handValue=0
        
    def returnCard(self, cardNumber=0):
        return self.hand[cardNumber][0]
        
def getMove():
    while(True):
        move = input('Would you like to stand or hit? (type s or h, then press enter) ')
        if move == 's' or move == 'h':
            return move
        print('\nPlease enter valid input')
    
def keepPlaying():
    while(True):
        i = input('Would you like to keep playing? (type y or n, then press enter) ')
        if i == 'y':
            return True
        elif i == 'n':
            return False
        print('\nPlease enter valid input')
        
d = Deck()
d.createDeck()
d.shuffle()

playerHand = Hand()
dealerHand = Hand()

playerBank = Bank()

while (True):
    print('\nYour +/- is', playerBank.getBal())
    
    s = input('How much would you like to bet? ')
    bet = int(s)
    
    pBust = False
    dBust = False
    playerHand.clearHand()
    dealerHand.clearHand()
    
    playerHand.recCard(d.draw())
    dealerHand.recCard(d.draw())
    playerHand.recCard(d.draw())
    dealerHand.recCard(d.draw())

    print('\nThe dealer shows', dealerHand.returnCard(),'\n')
    print('You have', playerHand.returnCard(), 'and', playerHand.returnCard(1))
    dHandVal = dealerHand.calcHand()
    pHandVal = playerHand.calcHand()

    
    if pHandVal == 21 and dHandVal == 21:
        print("Both you and the dealer have blackjack, it's a standoff")
        keepPlay = keepPlaying()
        if keepPlay:
            continue
        else:
            break
    elif pHandVal == 21:
        print('Blackjack!')
        playerBank.add(bet*1.5)
        keepPlay = keepPlaying()
        if keepPlay:
            continue
        else:
            break
    elif dHandVal == 21:
        print("\nThe dealer's second card was", dealerHand.returnCard(1))
        print('The dealer has blackjack, he collects your bet')
        playerBank.subtract(bet)
        keepPlay = keepPlaying()
        if keepPlay:
            continue
        else:
            break
    else:
        print('Your hand value is', pHandVal)
        move = getMove()     
        if move == 's':
            print("\nThe dealer's second card was", dealerHand.returnCard(1))
            print('Dealer hand value:', dHandVal)
            while(dHandVal<17):
                if not d.canDraw():
                    d.recreate()
                dealerHand.recCard(d.draw())
                dHandVal = dealerHand.calcHand()
                print('\nThe dealer drew', dealerHand.returnCard(-1))
                print('Dealer hand value is now', dHandVal)
                if dHandVal > 21:
                    print('\nBust!')
                    dBust = True
                    break
                    
        else:
            while(True):
                if not d.canDraw():
                    d.recreate()
                playerHand.recCard(d.draw())
                pHandVal = playerHand.calcHand()
                print('\nYou drew', playerHand.returnCard(-1))
                print('Your hand value is now', pHandVal)
                if pHandVal > 21:
                    print('\nBust!')
                    pBust = True
                    break
                move = getMove()
                if move == 's':
                    break
                
            if pBust:
                playerBank.subtract(bet)
                keepPlay = keepPlaying()
        
                if keepPlay:
                    continue
                else:
                    break
            
            print("\nThe dealer's second card was", dealerHand.returnCard(1))
            print('Dealer hand value:', dHandVal)
            while(dHandVal<17):
                if not d.canDraw():
                    d.recreate()
                dealerHand.recCard(d.draw())
                dHandVal = dealerHand.calcHand()
                print('\nThe dealer drew', dealerHand.returnCard(-1))
                print('Dealer hand value is now', dHandVal)
                if dHandVal > 21:
                    print('\nBust! Congrats!')
                    dBust = True
                    break
            
        if dBust:
            playerBank.add(bet)
            keepPlay = keepPlaying()
        
            if keepPlay:
                continue
            else:
                break
        
        if pHandVal == dHandVal:
            print("\nYour hand value matches the dealer's. It's a standoff")
        elif pHandVal > dHandVal:
            print("\nYour hand value was greater than the dealer's! Nice!")
            playerBank.add(bet)
        else:
            print("\nThe dealer's hand value was greater than yours. Maybe next time!")
            playerBank.subtract(bet)
        
        keepPlay = keepPlaying()
        
        if not keepPlay:
            break
     
    if d.numOfCards() < 4:
        d.recreate()
        
print('\nYour final +/- is', playerBank.getBal())