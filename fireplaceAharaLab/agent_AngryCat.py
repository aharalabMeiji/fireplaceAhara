#StandardStep2

import random
import copy
from fireplace.exceptions import GameOver
from hearthstone.enums import CardClass, CardType#
from utils import *
from fireplace.game import Game
from enum import IntEnum


class AngryCatAgent(Agent):
	def __init__(self, myName: str, myFunction, myOption = [], myClass: CardClass = CardClass.HUNTER, rating =1000 ):
		super().__init__(myName, myFunction, myOption, myClass, rating )
	
	def getHisWorth(thisGame: Game):
		Vec = []
		His = thisGame.current_player.opponent
		Vec.append(His.hero.health)
		hisCharA = 0
		hisCharH = 0
		hisTauntCharH = 0
		for char in His.characters:
			hisCharA += char.atk
			if char.type==CardType.MINION:
				hisCharH += char.health
				if char.taunt:
					hisTauntCharH += char.health
		Vec.append(hisCharA)
		Vec.append(hisCharH)
		Vec.append(hisTauntCharH)
		My=thisGame.current_player
		myCharA = hisCharA
		myCharH = hisCharH
		myTauntCharH = hisTauntCharH
		for char in My.characters:
			myCharA -= char.atk
			if char.type==CardType.MINION:
				myCharH -= char.health
				#GameTag.TAUNT
				if char.taunt:
					myTauntCharH -= char.health
		Vec.append(myCharA)
		Vec.append(myCharH)
		Vec.append(myTauntCharH)
		return Vec# of length 7

	def getDiffHisWorth(thisGame: Game, myChoice: Candidate):
		oldVec = AngryCatAgent.getHisWorth(thisGame)
		newGame = copy.deepcopy(thisGame)
		executeAction(newGame, myChoice, debugLog=False)
		#StandardRandom(newGame)	# simulating until turn-end
		newVec = AngryCatAgent.getHisWorth(newGame)
		answer=[]
		for i in range (len(oldVec)):
			answer.append(newVec[i]-oldVec[i])
		return answer

	def myDot(Vec1, Vec2):#これだけのためにnumpyを呼び出すのはナンなので
		myLen = (len(Vec1), len(Vec2))[len(Vec1)<len(Vec2)]
		answer = 0
		for n in range(myLen):
			answer -= (Vec1[n]*Vec2[n])
		return answer

	def AngryCatAI(thisGame: Game, option=[], gameLog=[], debugLog=True):
		while True:
			myCandidates = getCandidates(thisGame)
			if len(myCandidates)==0:
				return
			else:
				for myChoice in myCandidates:
					myChoice.score = AngryCatAgent.getDiffHisWorth(thisGame, myChoice)
				myChoice = AngryCatAgent.myChoiceAngryCat(thisGame, myCandidates)
				if myChoice==None:
					return
				else:
					executeAction(thisGame, myChoice, debugLog=debugLog)
					postAction(thisGame.current_player)

	def myChoiceAngryCat(thisGame, myCandidates, option=[2,1,1,1,1,1,1]):
		""" 
		リストの中から、スコアの高いものをピックアップして返す。
		"""
		# modify option by thisGame

		ret = None
		score = 0
		random.shuffle(myCandidates)
		for myChoice in myCandidates:
			thisScore =  AngryCatAgent.myDot(myChoice.score, option)
			if score < thisScore:
				score = thisScore
				ret = myChoice
		return ret



#CardClass.WARRIOR 8,6,3,7,8,3,8,1,5,4,5,10,5,5,7,9,5,1,8,10,1,5,2,8,6,3,3,10,10,2,8,8,3,5,
#win=20, 3,10,1,5,9,6,7,7,2,1,2,2,5,8,3,8,1,7,4,7,9,4,2,4,9,7,10,2,5,5,3,10,10,8,Start game
#win=17, 1,7,3,8,2,7,7,5,1,1,10,8,8,1,8,8,1,8,6,4,6,4,13,4,4,8,5,1,5,10,9,6,4,8,Start game
