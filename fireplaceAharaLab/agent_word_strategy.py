#agent_word_strategy

from enum import IntEnum, CardType
from utils import ExceptionPlay,Candidate
import random

class WS(IntEnum):
	""" プレーを言葉で説明　"""
	ランダムにプレー=0
	呪文を使えるなら呪文=1
	ミニョンで敵ヒーローの体力を削る=2
	自ヒーローの体力を回復する=3
	最初の2巡は小物を出す=4
	大物が出ているならば挑発を出す=5
	コストの小さいミニョンを出す=6
	pass

def agent_word_strategy(game, option=[WS.ランダムにプレー], debugLog=True):
	Loop=True
	while Loop:
		Loop=False
		for i in range(len(option)):
			ws = option[i]
			act,exc =  execute_word_strategy(game, ws, debugLog)
			if exc == ExceptionPlay.GAMEOVER:
			   return ExceptionPlay.GAMEOVER
			if act:#継続
				Loop=True
	return ExceptionPlay.VALID

def execute_word_strategy(game, ws, debugLog):
	if ws==WS.ランダムにプレー:
		myCandidate = []
		for card in player.hand:
			if card.is_playable():
				target = None
				if card.must_choose_one:
					card = random.choice(card.choose_cards)
				if card.requires_target():
					for target in card.targets:
						myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=target))
				else:
					myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=None))
		for character in player.characters:
			if character.can_attack():
				for target in character.targets:
					if character.can_attack(target):
						myH=character.health
						hisA=target.atk
						if myH >= hisA:
							myCandidate.append(Candidate(character, _type=BlockType.ATTACK, _target=None))
		if len(myCandidate) > 0:
			myChoice = random.choice(myCandidate)
			exc = executePlay(game, myChoice)
			postAction(player)
			if exc==ExceptionPlay.GAMEOVER:
				return False,ExceptionPlay.GAMEOVER
			else:
				return True,ExceptionPlay.VALID
		return False,ExceptionPlay.VALID
	elif ws==WS.呪文を使えるなら呪文:
		player=game.current_player
		myCandidate = []
		for card in player.hand:
			if card.type==CardType.SPELL and card.is_playable():
				if card.requires_target():
					for target in card.targets:
						if '沈黙' in card.name and is_vanilla(target):#現状ではつかえてしまうため
							pass
						else:
							myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=target))
				else:
					myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=None))
		if len(myCandidate)>0:
			exc = executeAction(game, random.choice(muCandidate))
			postAction(player)
			if exc==ExceptionPlay.GAMEOVER:
				return False,ExceptionPlay.GAMEOVER
			else:
				return True,ExceptionPlay.VALID
		return False,ExceptionPlay.VALID
	elif ws==WS.ミニョンで敵ヒーローの体力を削る:
		player=game.current_player
		myCandidate = []
		max_atk=-1
		for character in player.characters:
			if character.can_attack(player.opponent.hero):
				if character.atk>max_atk:
					myCandidate=[Candidate(character, _type=BlockType.ATTACK, _target=player.opponent.hero)]
					max_atk = character.atk
				elif character.atk==max_atk:
					myCandidate.append(Candidate(character, _type=BlockType.ATTACK, _target=player.opponent.hero))
		if len(myCandidate)>0:
			exc = executeAction(game, random.choice(muCandidate))
			postAction(player)
			if exc==ExceptionPlay.GAMEOVER:
				return False,ExceptionPlay.GAMEOVER
			else:
				return True,ExceptionPlay.VALID
		return False,ExceptionPlay.VALID
	elif ws==WS.自ヒーローの体力を回復する:
		player=game.current_player
		pre_candidate=[]
		currentHeroHealth=player.hero.health
		for card in player.hand:
			if card.is_playable():
				if card.requires_target():
					for target in card.targets:
						pre_candidate.append(Candidate(card, _type=BlockType.PLAY, _target=target))
				else:
					myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=None))
		myCandidate=[]
		if len(pre_candidate)>0:
			for myChoice in pre_candidate:
				tmpgame = deepcopy(game)
				executeAction(tmpgame,myChoice)
				if tmpgame.current_player.hero.health > currentHeroHealth:
					myCandidate.append(myChoice)
		if len(myCandidate)>0:
			exc = executeAction(game, random.choice(muCandidate))
			postAction(player)
			if exc==ExceptionPlay.GAMEOVER:
				return False,ExceptionPlay.GAMEOVER
			else:
				return True,ExceptionPlay.VALID
		return False,ExceptionPlay.VALID
	elif ws==WS.最初の2巡は小物を出す:
		if game.turn<5:#最初の2巡
			player=game.current_player
			myCandidate = []
			for card in player.hand:
				if card.type==CardType.MINION and card.is_playable():
					if card.requires_target():
						for target in card.targets:
							myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=target))
					else:
						myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=None))
			if len(myCandidate)>0:
				exc = executeAction(game, random.choice(muCandidate))
				postAction(player)
				if exc==ExceptionPlay.GAMEOVER:
					return False,ExceptionPlay.GAMEOVER
				else:
					return True,ExceptionPlay.VALID
			return False,ExceptionPlay.VALID
		else:
			return False,ExceptionPlay.VALID
		pass
	elif ws==WS.大物が出ているならば挑発を出す:
		player=game.current_player
		totalHealth=0
		totalAttack=0
		for card in player.characters:
			totalHealth += card.health
			totalAttack += card.atk
		if totalHealth<2 or totalAttack<2:
			return False,ExceptionPlay.VALID
		myCandidate = []
		for card in player.hand:
			if card.taunt and card.is_playable():
				if card.requires_target():
					for target in card.targets:
						myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=target))
				else:
					myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=None))
		if len(myCandidate)>0:
			exc = executeAction(game, random.choice(muCandidate))
			postAction(player)
			if exc==ExceptionPlay.GAMEOVER:
				return False,ExceptionPlay.GAMEOVER
			else:
				return True,ExceptionPlay.VALID
		return False,ExceptionPlay.VALID
		
	elif ws==WS.コストの小さいミニョンを出す:
		player=game.current_player
		myCandidate = []
		for card in player.hand:
			if card.type==CardType.MINION and card.is_playable() and card.cost<3:
				if card.requires_target():
					for target in card.targets:
						myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=target))
				else:
					myCandidate.append(Candidate(card, _type=BlockType.PLAY, _target=None))
		if len(myCandidate)>0:
			exc = executeAction(game, random.choice(muCandidate))
			postAction(player)
			if exc==ExceptionPlay.GAMEOVER:
				return False,ExceptionPlay.GAMEOVER
			else:
				return True,ExceptionPlay.VALID
		return False,ExceptionPlay.VALID

		
def is_vanilla(cls):
	return len(cls.data.description)<3

def postAction(player):
	if player.choice:
		choice = random.choice(player.choice.cards)
		#print("Choosing card %r" % (choice))
		myChoiceStr = str(choice)
		if 'RandomCardPicker' in str(choice):
			myCardID =  random.choice(choice.find_cards())
			myCard = Card(myCardID)
			myCard.controller = player#?
			myCard.draw()
			player.choice = None
		else :
			player.choice.choose(choice)
