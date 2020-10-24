import random
import copy
from fireplace.exceptions import GameOver, InvalidAction
from fireplace.logging import log
from hearthstone.enums import  CardType, BlockType, Race#
from typing import List
from utils import *
from fireplace.card import Card
from fireplace.game import Game

class HunterCatLogLog:
	loglog=[]
	pass

class HunterCatAgent(Agent):

	def __init__(self, myName: str, myFunction, myOption = [], myClass: CardClass = CardClass.HUNTER, rating =1000 ):
		super().__init__(myName, myFunction, myOption, myClass, rating )
	def HunterCatLoadData():
		pass
	def ClearHunterCatLogLog(self):
		HunterCatLogLog.loglog=[]
		pass

	def HunterCatSaveLog(self, winlose):
		with open("hunterCatQ.csv", mode='a') as f:
			for line in HunterCatLogLog.loglog:
				if len(line)==4:
					f.write("%d,%d,%d,%d,%d,%d,%d,%s\n"%(line[0],line[1],line[2],line[3],-1,-1,winlose,"***"))
				else:
					f.write("%d,%d,%d,%d,%d,%d,%d,%s\n"%(line[0],line[1],line[2],line[3],line[4],line[5],winlose,line[6]))
		pass

	def HunterCatAI(self, game, option=[], gameLog=[], debugLog=False):
		if game.turn<2:
			HunterCatAgent.HunterCatLoadData()
		while True:
			scoreVector = HunterCatAgent.HunterCatScore(game)
			HunterCatLogLog.loglog.append([game.turn, scoreVector.myMinionPoint, scoreVector.myHeroPoint - scoreVector.hisHeroPoint, scoreVector.hisCharN])
			player = game.current_player
			myCandidates = getCandidates(game,_smartCombat=True,_includeTurnEnd=True)
			random.shuffle(myCandidates)
			#if debugLog:
			#	print( '--------------------------')
			for myChoice in myCandidates:
				cardID=myChoice.card
				myChoice.notes=HunterCat_CardStatus(cardID)
				tmpGame = copy.deepcopy(game)
		
				if myChoice.type==ExceptionPlay.TURNEND:
					pass
				else:
					result = executeAction(tmpGame, myChoice, debugLog=False)
					if result==ExceptionPlay.GAMEOVER and tmpGame.current_player.opponent.hero.health<=0:
						#終われるなら終わりにします。
						HunterCatLogLog.loglog[-1].append(player.hero.health)
						HunterCatLogLog.loglog[-1].append(player.opponent.hero.health)
						HunterCatLogLog.loglog[-1].append(str(myChoice))
						executeAction(game, myChoice, debugLog=debugLog)
						postAction(player)
						return
					#else:
						#ターンの最後までプレーする
						#ここをもっと賢くしてもよい
						#複数回行って平均を取ってもよい
				scoreVector = HunterCatAgent.HunterCatScore(tmpGame)
				myChoice.score=scoreVector.getScore()
			if len(myCandidates)>0:
				myChoice = HunterCatAgent.HunterCatChoice(myCandidates, player, debugLog=debugLog)
				HunterCatLogLog.loglog[-1].append(player.hero.health)
				HunterCatLogLog.loglog[-1].append(player.opponent.hero.health)
				HunterCatLogLog.loglog[-1].append(str(myChoice))
				if myChoice.card==None:
					#HunterCatAgent.HunterCatSaveLog()
					#if debugLog:
					#	print( '--------------------------')
					return
				executeAction(game, myChoice, debugLog=debugLog)
				postAction(player)
			else:
				self.loglog[-1].append(player.hero.health)
				self.loglog[-1].append(player.opponent.hero.health)
				self.loglog[-1].append("None")
				#HunterCatAgent.HunterCatSaveLog()
				#if debugLog:
				#	print( '--------------------------')
				return

	def HunterCatChoice(cds: List, player, debugLog=False):
		maxScore = -10000
		myChoices = []
		exists_attack=False
		for choice in cds:
			if choice.type==BlockType.ATTACK:
				exists_attack=True
		for choice in cds:
			#if debugLog:
			#	print("%s %s %s"%(choice.card,choice.type,choice.target),end='->')
			score = choice.score
			if choice.type==BlockType.PLAY:
				note=choice.notes
				cls = choice.card
				conditions=note.split(":")
				if choice.target!=None:
					if 'damage' in conditions[4] and choice.target.controller == player:
						score -= 5000
					if 'help' in conditions[4] and choice.target.controller != player:
						score -= 5000
				if eval(conditions[5]):
				  score+=1000
				if eval(conditions[6]):
				  score+=1000
				score+=(eval(conditions[7])*1000)
			#if debugLog:
			#	print(" %f"%score)
			if score>=5000 and choice.card!=None:#詰んでいるばあいは詰ましにいく
				return choice
			if exists_attack and choice.card==None:#ミニオンがあってパスを選択するのはナシ？
				pass
			else:
				if maxScore<score:
					myChoices=[choice]
					maxScore = score
				elif maxScore==score:
					myChoices.append(choice)

		return random.choice(myChoices)


	class HunterCatScore(object):
		paraA=1.0
		paraB=1.0
		paraC=1.0
		turn=None
		myHeroH=hisHeroH=0
		myCharA=myCharN=myCharH=0
		myTauntCharA=myTauntCharH=0
		hisCharA=hisCharN=hisCharH=0
		hisTauntCharA=hisTauntCharH=0
		def __init__(self, game):
			ahara=0
			self.turn=game.turn
			me = game.current_player
			he = game.current_player.opponent
			myHero = me.hero
			hisHero = he.hero
			self.myHeroH = myHero.health
			self.hisHeroH = hisHero.health
			for char in me.characters:
				charatk=char.atk
				if charatk>char.max_attacks:
					charatk=char.max_attacks
					pass
				self.myCharA += charatk
				self.myCharN += 1
				if char.taunt:
					self.myTauntCharA += charatk
				if char.type == CardType.MINION:
					self.myCharH += char.health
					if char.taunt:
						self.myTauntCharH += char.health
			for char in he.characters:
				charatk=char.atk
				if charatk>char.max_attacks:
					charatk=char.max_attacks
					pass
				self.hisCharA += charatk
				self.hisCharN += 1
				if char.taunt:
					self.hisTauntCharA += charatk
				if char.type == CardType.MINION:
					self.hisCharH += char.health
					if char.taunt:
						self.hisTauntCharH += char.health
			self.myMinionPoint = self.myCharA - self.hisCharA
			self.myHeroPoint = self.myHeroH - (self.hisCharA - self.myTauntCharH)
			self.hisHeroPoint = self.hisHeroH - (self.myCharA - self.hisTauntCharH)
			self.SpellCN=0
			self.PlayableSpellCN=0
			for card in me.hand:
				if card.type == CardType.SPELL:
					self.SpellCN += 1
					if card.is_playable():
						self.PlayableSpellCN += 1
		def getPhase(self):
			if self.turn<6:#まずはリードを確保する
				self.phase=5
			elif self.hisCharN>=3:#相手の枚数が増えてきたら
				self.phase=2
			elif self.hisCharN<=1:#相手のミニオンがないなら
				self.phase=3
			elif self.myHeroPoint-self.hisHeroPoint<=-5:#劣勢を取り返す
				self.phase=2
			else:
				self.phase=4
			pass
		def getScore(self):
			self.getPhase()
			if self.hisHeroH<=0:
				return 10000
			if self.hisHeroPoint<=0:
				return 5000
			self.paraA=0.3

			if self.phase==5:#ポイント重視
				self.paraA=0.0
				self.paraB=1.0
				self.paraC=0.0
			elif self.phase==4:#ポイント・枚数平等
				self.paraA=3.0
				self.paraB=1.0
				self.paraC=0.0
			elif self.phase==3:#枚数重視
				self.paraA=3.0
				self.paraB=0.0
				self.paraC=0.0
			elif self.phase==2:#ポイント重視＋相手の枚数重視
				self.paraA=0.0
				self.paraB=1.0
				self.paraC=3.0
			else:#相手の枚数重視
				self.paraA=0.0
				self.paraB=0.0
				self.paraC=3.0
			return self.paraA*self.myMinionPoint\
				+ self.paraB*(self.myHeroPoint - self.hisHeroPoint)\
				- self.paraC*self.hisCharN


#### True or False ####

def onMinion(player):
	for card in player.field:
		if card.type==CardType.MINION:
			return True
	return False

def onBeast(player):
	for card in player.field:
		if card.race == Race.BEAST:
			return True
	return False

def haveSecret(player):
	for card in player.hand:
		if '秘策:' in card.data.description:
			return True
	return False

def haveNoMinion(player):
	for card in player.field:
		if card.type==CardType.MINION:
			return False
	return True

def haveSpell(player):
	for card in player.hand:
		if card.type==CardType.SPELL:
			return True
	return False

def haveOvercostCard(player,cost):
	myCost = cost
	for card in player.hand:
		#if card.is_playable() and card.cost==myCost:
		#	return False
		if card.cost==myCost+1:
			return True
	return False

def hasHeroPowerMerrit(player):
	for card in player.field:
		if '自分がヒーローパワーを使用した後' in card.data.description.replace('\n',''):
			return True
	return False

def heHasMinion(player):
	opponent=player.opponent
	for card in player.field:
		if card.type==CardType.MINION:
			return True
	return False

def haveCard(player, a, b):
	NoC=len(player.hand)
	if NoC>=a and NoC<=b:
		return True
	return False



### 0 or 1 or 2 ###

def handCardNumber(player):
	return len(player.hand)


def needBeast(player,cost):
	for card in player.hand:
		if card.type==CardType.MINION and card.race==Race.BEAST:
			if card.cost<=player.mana-player.used_mana-cost:
				return 2
			return 1
	return 0

def needSpell(player, cost):
	for card in player.hand:
		if card.type==CardType.SPELL:
			if card.cost<=player.mana-player.used_mana-cost:
				return 2
			return 1
	return 0

def needSecret(player, cost):
	for card in player.hand:
		if '秘策:' in card.data.description:
			if card.cost<=player.mana-player.used_mana-cost:
				return 2
			return 1
	return 0

def needHeropower(player, cost):
	card = player.hero.power
	if card.cost<=player.mana-player.used_mana-cost:
		return 2
	return 0


def HunterCat_CardStatus(ID):
	if ID==None:
		return "0:0:0:0:None:0:0:0:"
	cls = Card(ID)
	ret = str(cls.cost)+":"
	if cls.type==CardType.MINION:
		ret += str(cls.atk)+":"
		ret += str(cls.health)+":"
		ret += "MINION:" 
	elif cls.type==CardType.SPELL:
		ret += "0:"
		ret += "0:"
		ret += "SPELL:" 
	elif cls.type==CardType.WEAPON:
		ret += str(cls.atk)+":"
		ret += "0:"
		ret += "WEAPON:" 
	elif cls.type==CardType.HERO_POWER:
		ret += "0:"
		ret += "0:"
		ret += "HERO_POWER:" 
	else:
		ret += "0:"
		ret += "0:"
		ret += "NONE:"
	if ID  == 'SCH_617':
		ret += 'help+summon+drawCard:'#type
		ret += 'onMinion(player):'#must condition
		ret += 'onMinion(player):'#condition for better
		ret += 'needBeast(player,'+str(cls.cost)+'):'#condition in turn
		#カワイイ侵入者 : ミニオン1体に+1/+1を付与する。1/1の仔を1体召喚する。仔1体を自分の手札に追加する。
	elif ID  == 'SCH_312':
		ret += 'help:'#type
		ret += 'False:'#must condition
		ret += 'player.mana-player.used_mana<2:'#condition for better
		ret += 'needHeropower(player,'+str(cls.cost)+'):'#condition in turn
		#ツアーガイド : 雄叫び:自分が次に使うヒーローパワーのコストは（0）。
	elif ID  == 'DRG_253':
		ret += 'help:'#type
		ret += 'False:'#must condition
		ret += 'heHasMinion(player):'#condition for better
		ret += '0:'#condition in turn
		#ドワーフの狙撃手 : 自分のヒーローパワーはミニオンを対象にできる。
	elif ID  == 'SCH_133':
		ret += 'summon:'#type
		ret += 'True:'#must condition
		ret += 'haveNoMinion(player) or 1<'+str(cls.atk)+':'#condition for better
		ret += 'needBeast(player,'+str(cls.cost)+'):'#condition in turn
		#ヴォルパーティンガー : 雄叫び:このミニオンの__コピーを1体召喚する。
	elif ID  == 'SCH_231':
		ret += 'help:'#type
		ret += 'False:'#must condition
		ret += 'haveSpell(player):'#condition for better
		ret += 'needSpell(player, '+str(cls.cost)+'):'#condition in turn
		#図太い徒弟 : 魔法活性:攻撃力+2を獲得する。
	elif ID  == 'SCH_600':
		ret += 'summon:'#type
		ret += 'True:'#must condition
		ret += 'True:'#condition for better
		ret += '0:'#condition in turn
		#悪魔の相棒 : ランダムな悪魔の相棒を1体召喚する。
	elif ID  == 'BT_213':
		ret += 'drawCard:'#type
		ret += 'False:'#must condition
		ret += 'False:'#condition for better
		ret += 'needBeast(player,'+str(cls.cost)+'):'#condition in turn
		#クズ拾いの工夫 : ___獣を1体引く。それに+2/+2を付与する。
	elif ID  == 'DRG_252':
		ret += 'secret:'#type
		ret += 'False:'#must condition
		ret += 'False:'#condition for better
		ret += 'needHeropower(player,'+str(cls.cost)+') or needBeast(player,'+str(cls.cost)+'):'#condition in turn
		#フェーズ・ストーカー : 自分がヒーローパワーを使用した後自分のデッキから秘策を1つ準備する。
	elif ID  == 'EX1_611':
		ret += 'secret+defence:'#type
		ret += 'False:'#must condition
		ret += 'heHasMinion(player):'#condition for better
		ret += '0:'#condition in turn
		#凍結の罠 : 秘策: 敵のミニオンが攻撃した時そのミニオンは持ち主の手札に戻る。そのミニオンのコストは（2）増える。
	elif ID  == 'ULD_152':
		ret += 'secret+damage:'#type
		ret += 'False:'#must condition
		ret += 'heHasMinion(player):'#condition for better
		ret += '0:'#condition in turn
		#感圧板 : 秘策:相手が呪文を使用した後ランダムな敵のミニオン1体を破壊する。
	elif ID  == 'EX1_610':
		ret += 'secret+damage:'#type
		ret += 'heHasMinion(player):'#must condition
		ret += 'heHasMinion(player):'#condition for better
		ret += '0:'#condition in turn
		#爆発の罠 : 秘策: 自分のヒーローが攻撃された時、全ての敵に$2ダメージを与える。
	elif ID  == 'BT_203':
		ret += 'secret+summon:'#type
		ret += 'True:'#must condition
		ret += 'haveNoMinion(player):'#condition for better
		ret += '0:'#condition in turn
		#群れの戦術 : 秘策:味方のミニオンが攻撃された時3/3のコピーを1体召喚する。
	elif ID  == 'SCH_142':
		ret += 'drawCard:'#type
		ret += 'False:'#must condition
		ret += 'haveCard(player,1,3):'#condition for better
		ret += '0:'#condition in turn
		#貪欲な読書家 : 自分のターンの終了時手札が3枚になるまでカードを引く。
	elif ID  == 'EX1_536':
		ret += 'help:'#type
		ret += 'False:'#must condition
		ret += 'haveSecret(player):'#condition for better
		ret += 'needSecret(player,'+str(cls.cost)+'):'#condition in turn
		#イーグルホーン・ボウ : 味方の秘策が発動する度耐久度+1を獲得する。
	elif ID  == 'EX1_539':
		ret += 'damage:'#type
		ret += 'False:'#must condition
		ret += 'onBeast(player):'#condition for better
		ret += '0:'#condition in turn
		#殺しの命令 : $3ダメージを与える。味方に獣がいる場合は代わりに$5ダメージを与える。
	elif ID  == 'NEW1_031':
		ret += 'summon:'#type
		ret += 'False:'#must condition
		ret += 'False:'#condition for better
		ret += 'needBeast(player,'+str(cls.cost)+'):'#condition in turn
		#獣の相棒 : ランダムな獣の相棒を1体召喚する。
	elif ID  == 'DRG_256':
		ret += 'damage:'#type
		ret += 'True:'#must condition
		ret += 'heHasMinion(player):'#condition for better
		ret += 'needHeropower(player,'+str(cls.cost)+'):'#condition in turn
		#ドラゴンベイン : 自分がヒーローパワーを使用した後ランダムな敵1体に___5ダメージを与える。
	elif ID  == 'SCH_428':
		ret += 'drawCard:'#type
		ret += 'False:'#must condition
		ret += 'False:'#condition for better
		ret += '0:'#condition in turn
		#伝承守護者ポルケルト : 雄叫び:自分のデッキのカードをコストが高い順に並べ替える。
	elif ID == 'GAME_005':
		ret += 'help:'#type
		ret += 'haveOvercostCard(player,'+str(cls.cost)+'):'#must condition
		ret += 'False:'#condition for better
		ret += '0:'#condition in turn
		#コイン
	elif ID == 'HERO_05bp':
		ret += 'help:'#type
		ret += 'hasHeroPowerMerrit(player):'#must condition
		ret += 'False:'#condition for better
		ret += '0:'#condition in turn
		# ヒーローパワー　敵のヒーローに\n$2ダメージを\n与える。
	else:
		ret += 'None:'#type
		ret += 'False:'#must condition
		ret += 'False:'#condition for better
		ret += '0:'#condition in turn
	return ret
