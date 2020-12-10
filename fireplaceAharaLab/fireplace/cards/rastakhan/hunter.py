from ..utils import *
from fireplaceAharaLab.myactions import *

### hunter @ rastakhan's rumble

class TRL_348:
	"""Springpaw	Common
	[x]&lt;b&gt;Rush&lt;/b&gt;
	&lt;b&gt;Battlecry:&lt;/b&gt; Add a 1/1 Lynx
	with &lt;b&gt;Rush&lt;/b&gt; to your hand."""
	play = Give(CONTROLLER, "TRL_348t")
class TRL_348t:
	""" Lynx"""
	pass

class TRL_119:
	"""The Beast Within	Epic
	Give a friendly Beast +1/+1, then it attacks a random enemy minion."""
	play = Buff(FRIENDLY_MINIONS + BEAST, "TRL_119e").then(Attack(Buff.TARGET, RANDOM(ENEMY_MINIONS)))
TRL_119e = buff(1,1)
"""The Beast Within"""

class TRL_111:
	"""Headhunter's Hatchet	Common
	[x]&lt;b&gt;Battlecry:&lt;/b&gt; If you
	control a Beast, gain
	+1 Durability."""
	play = Find(FRIENDLY_MINIONS + BEAST) & Buff(SELF, "TRL_111e1")
TRL_111e1 = buff(0,1)
"""Headhunter's Hatchet"""

class TRL_566:
	"""Revenge of the Wild	Rare
	Summon your Beasts that died this turn."""
	play = Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED_THIS_TURN + BEAST))

class TRL_349:
	"""Bloodscalp Strategist	Rare
	&lt;b&gt;Battlecry:&lt;/b&gt; If you have a weapon equipped, &lt;b&gt;Discover&lt;/b&gt; a spell."""
	powered_up = Find(FRIENDLY_WEAPON)
	play = powered_up & Discover(CONTROLLER, SPELL)

class TRL_339:##################################
	"""Master's Call	Epic
	&lt;b&gt;Discover&lt;/b&gt; a minion in your deck.
	If all 3 are Beasts,
	draw them all."""
	play = Discover(CONTROLLER, FRIENDLY_DECK)

class TRL_901:
	"""Spirit of the Lynx	Rare
	[x]&lt;b&gt;Stealth&lt;/b&gt; for 1 turn.
	Whenever you summon a 
	Beast, give it +1/+1."""
	play = OWN_TURN_END.on(Unstealth(SELF))
	events = Summon(CONTROLLER, BEAST).on(Buff(SELF, "TRL_901e"))

TRL_901e = buff(1, 1)
"""Blessing of Halazzi"""

class TRL_347:
	"""Baited Arrow	Common
	Deal $3 damage. &lt;b&gt;Overkill:&lt;/b&gt; Summon a 5/5 Devilsaur."""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 3), Summon(CONTROLLER, "TRL_347t")
class TRL_347t:
	"""Devilsaur"""
	pass

class TRL_900:
	"""Halazzi, the Lynx	Legendary
	&lt;b&gt;Battlecry:&lt;/b&gt; Fill your hand with 1/1 Lynxes that have_&lt;b&gt;Rush&lt;/b&gt;."""
	play = Give(CONTROLLER, "TRL_348t") * 10

class TRL_065:
	"""Zul'jin	Legendary
	[x]&lt;b&gt;Battlecry:&lt;/b&gt; Cast all spells
	you've played this game
	&lt;i&gt;(targets chosen randomly)&lt;/i&gt;."""
	play = CastAllSpells(CONTROLLER)
