from ..utils import *

####  paladin @ scholomance, 14 cards  ####

class SCH_247:#OK
	"""First Day of School		0	-	-	Spell	Common	-	-
	Add 2 random 1-Cost minions to your hand."""
	play = Give(CONTROLLER, RandomMinion(cost=1)) * 2
class SCH_524:#OK
	"""Shield of Honor		1	-	-	Spell	Common	-	Divine Shield	
	Give a damaged minion +3 Attack and &lt;b&gt;Divine Shield&lt;/b&gt;."""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY:0, PlayReq.REQ_DAMAGED_TARGET:0, PlayReq.REQ_MINION_TARGET:0 }
	play = Buff(TARGET, "SCH_524e"),SetTag(TARGET, (GameTag.DIVINE_SHIELD,))
SCH_524e = buff(3,0)
class SCH_250:#OK
	"""Wave of Apathy		1	-	-	Spell	Common	-	-	
	Set the Attack of all enemy minions to 1 until your next turn."""
	play = Buff(ENEMY_MINIONS, "SCH_250e")
class SCH_250e:
	""" Apathetic """
	atk = SET(1)
	events = OWN_TURN_BEGIN.on(Destroy(SELF))
class SCH_149:#OK
	"""Argent Braggart		2	1	1	Minion	Epic	-	Battlecry	
	&lt;b&gt;Battlecry:&lt;/b&gt; Gain Attack and Health to match the highest in the battlefield."""
	play = ArgentBraggart(SELF)
class SCH_149e:# error: 'OpAttr' object is not callable
	""" Best of the Best """
	#atk = OpAttr(ALL_MINIONS, GameTag.ATK, max)
	#max_health = OpAttr(ALL_MINIONS, GameTag.HEALTH, max)
class SCH_523:#OK
	"""Ceremonial Maul		3	2	-	Weapon	Epic	-	Spellburst	
	&lt;b&gt;Spellburst&lt;/b&gt;: Summon a Student with &lt;b&gt;Taunt&lt;/b&gt; and stats equal to the spell's Cost."""
	#play = OWN_SPELL_PLAY.on(Summon(CONTROLLER, Buff(ID("SCH_523t"), {GameTag.ATK: SET(Attr(SELF, GameTag.COST)), GameTag.HEALTH: SET(Attr(SELF, GameTag.COST))})))
	play = Play(CONTROLLER, SPELL).on(CeremonialMaul(CONTROLLER, Play.CARD, "SCH_523t"))#
class SCH_523t:
	""" Honor Student """
	pass
class SCH_302:#OK
	"""Gift of Luminance		3	-	-	Spell	Rare	-	Divine Shield	
	Give a minion &lt;b&gt;Divine Shield&lt;/b&gt;, then summon a_1/1 copy of it."""
	requirements = { PlayReq.REQ_MINION_TARGET:0, PlayReq.REQ_TARGET_TO_PLAY:0 }
	#play = SetTag(TARGET, (GameTag.DIVINE_SHIELD, )).then(Summon(CONTROLLER, Buff(Copy(TARGET),"SCH_302e")))
	play = SetTag(TARGET, (GameTag.DIVINE_SHIELD, )).then(Summon(CONTROLLER,  ExactCopy(TARGET)).then(Buff(Summon.CARD, "SCH_302e")))
class SCH_302e:#OK
	""" Student of the Light """
	atk=SET(1)
	max_health=SET(1)
class SCH_532:#OK
	"""Goody Two-Shields		3	4	2	Minion	Rare	-	Divine Shield	
	&lt;b&gt;Divine Shield&lt;/b&gt;
	&lt;b&gt;Spellburst:&lt;/b&gt; Gain &lt;b&gt;Divine Shield&lt;/b&gt;."""
	events = OWN_SPELL_PLAY.on(SetTag(SELF,(GameTag.DIVINE_SHIELD,)))
class SCH_526:#OK
	"""Lord Barov		3	3	2	Minion	Legendary	-	Battlecry	
	[x]&lt;b&gt;Battlecry:&lt;/b&gt; Set the Health
	of all other minions to 1.
	&lt;b&gt;Deathrattle:&lt;/b&gt; Deal 1 damage
	to all minions."""
	play = Buff(ALL_MINIONS - SELF, "SCH_526e")
	deathrattle = Hit(ALL_MINIONS - SELF, 1)
class SCH_526e:
	max_health=SET(1)
class SCH_141:#OK
	"""High Abbess Alura		4	3	6	Minion	Legendary	-	Spellburst	
	&lt;b&gt;Spellburst:&lt;/b&gt; Cast a spell from your deck &lt;i&gt;(targets this if possible)&lt;/i&gt;."""
	play = OWN_SPELL_PLAY.on(CastSpellMe(RANDOM(FRIENDLY_DECK),SELF))
	## if we modify the definition of class CastSpell, we can!
class SCH_138:######################################################## cannot 'It_can't attack heroes' 
	"""Blessing of Authority		5	-	-	Spell	Rare	-	-	
	Give a minion +8/+8. It_can't attack heroes this turn."""
	requirements = { PlayReq.REQ_TARGET_TO_PLAY:0, PlayReq.REQ_MINION_TARGET:0, }
	play = Buff(TARGET, "SCH_138e"), Buff(TARGET, "SCH_138e2")
SCH_138e = buff(8,8)
class SCH_138e2:
	play = SetTag(OWNER, (GameTag.CANNOT_ATTACK_HEROES, ))
	events = OWN_TURN_END.on()
class SCH_139:############################################# NO WAY
	"""Devout Pupil		6	4	5	Minion	Epic	-	Divine Shield	
	[x]&lt;b&gt;Divine Shield, Taunt&lt;/b&gt;
	Costs (1) less for each spell
	you've cast on friendly
	characters this game."""
	#cost_mod = -Count(????)
class SCH_712:#OK
	"""Judicious Junior		6	4	9	Minion	Common	-	Lifesteal	
	&lt;b&gt;Lifesteal&lt;/b&gt;"""
	pass
class SCH_533:#OK
	"""Commencement		7	-	-	Spell	Rare	-	Divine Shield	
	Summon a minion from your deck. Give it &lt;b&gt;Taunt&lt;/b&gt; and &lt;b&gt;Divine Shield&lt;/b&gt;."""
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)).then(SetTag(Summon.CARD, (GameTag.TAUNT, GameTag.DIVINE_SHIELD)))
class SCH_135:#OK
	"""Turalyon, the Tenured		8	3	12	Minion	Legendary	-	Rush	
	[x]&lt;b&gt;Rush&lt;/b&gt;. Whenever this attacks
	a minion, set the defender's
	Attack and Health to 3."""
	events = Attack(SELF, ENEMY_MINIONS).on(Buff(Attack.DEFENDER, "SCH_135e"))
class SCH_135e:
	""" Schooled """
	atk = SET(3)
	max_health = SET(3)

