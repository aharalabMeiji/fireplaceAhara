import random
from collections import OrderedDict

from hearthstone.enums import BlockType, CardClass, CardType, Mulligan, PlayState, Step, Zone

from fireplace.dsl import LazyNum, LazyValue, Selector
from fireplace.entity import Entity
from fireplace.exceptions import InvalidAction
from fireplace.logging import log
from fireplace.utils import random_class

#################### a h a r a l a b ##############################

from .utils import GameWithLog, Candidate
from fireplace.actions import TargetedAction, ActionArg

class CastAllSpells(TargetedAction):
	TARGET = ActionArg()# controller
	def do(self, source, target, enemies):
		spells = []
		turn = self.controller.game.turn
		logs = self.controller.game.__myLog__
		for log in logs:
			if (log.turn+turn)%2==0:
				if log.type == BlockType.PLAY and log.card.type == CardType.SPELL:
					spells.append(log.card)
		for spell in spells:
			if spell.requires_target():
				CastSpellTargetsEnemiesIfPossible(spell).trigger(source)
			else:
				CastSpell(spell).trigger(source)

