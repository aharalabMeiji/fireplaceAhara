from ..utils import *

####### hunter in savior of uldum #######

class ULD_155:#OK
	"""Unseal the Vault	Legendary
	&lt;b&gt;Quest:&lt;/b&gt; Summon 20_minions.
	&lt;b&gt;Reward:&lt;/b&gt; Pharaoh's Warmask."""
	tags={GameTag.SIDEQUEST:True}
	events = Summon(CONTROLLER, MINION).on(	SidequestCounter(SELF,2,[Summon(CONTROLLER,"ULD_155p"), Destroy(SELF)]))
	
ULD_155e = buff(2,0)

class ULD_155p:#OK
	""" Pharaoh's Warmask
	&lt;b&gt;Hero Power&lt;/b&gt;
	Give your minions +2_Attack."""
	activate = Buff(FRIENDLY_MINIONS, "ULD_155e")

class ULD_152:#OK
	"""Pressure Plate	Common
	&lt;b&gt;Secret:&lt;/b&gt; After your opponent casts a spell, destroy a random enemy_minion."""
	secret = Play(OPPONENT, SPELL).on(Reveal(SELF), Destroy(RANDOM_ENEMY_MINION))

class ULD_430:#OK
	"""Desert Spear	Common
	After your hero attacks, summon a 1/1 Locust with &lt;b&gt;Rush&lt;/b&gt;."""
	events = Attack(FRIENDLY_HERO, ENEMY_MINIONS | ENEMY_HERO).on(Summon(CONTROLLER, "ULD_430t"))

class ULD_429:#OK
	"""Hunter's Pack	Common
	Add a random Hunter Beast, &lt;b&gt;Secret&lt;/b&gt;, and weapon to your_hand."""
	play = Give(CONTROLLER,RandomBeast(card_class=CardClass.HUNTER)), Give(CONTROLLER, RandomSpell(secret=True)), Give(CONTROLLER, RandomWeapon())

class ULD_151:#OK
	"""Ramkahen Wildtamer	Rare
	&lt;b&gt;Battlecry:&lt;/b&gt; Copy a random Beast in your hand.	"""
	play = Give(CONTROLLER,Copy(RANDOM(FRIENDLY_HAND + BEAST)))

class ULD_154:#OK
	"""Hyena Alpha	Rare
	[x]&lt;b&gt;Battlecry:&lt;/b&gt; If you control
	a &lt;b&gt;Secret&lt;/b&gt;, summon two
	2/2 Hyenas."""
	play = Find(FRIENDLY_SECRETS) & Summon(CONTROLLER, "ULD_154t") * 2
class ULD_154t:
	""" Hyena
	Vanilla """

class ULD_410:#OK
	"""Scarlet Webweaver	Epic
	&lt;b&gt;Battlecry:&lt;/b&gt; Reduce the Cost of a random Beast in your_hand by (5)."""
	play = Buff(RANDOM(IN_HAND + BEAST), "ULD_410e")
ULD_410e = buff(cost=-5)

class ULD_713:#OK
	"""Swarm of Locusts	Rare
	Summon seven 1/1 Locusts with &lt;b&gt;Rush&lt;/b&gt;."""
	play = Summon(CONTROLLER, "ULD_430t") * 7

class ULD_212:#OK  Who attacks the target? 
	"""Wild Bloodstinger	Epic
	&lt;b&gt;Battlecry:&lt;/b&gt; Summon a minion from your opponent's hand. Attack it."""
	play = Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION)).then( RegularAttack(FRIENDLY_MINIONS, Summon.CARD))

class ULD_156:#OK
	"""Dinotamer Brann	Legendary
	&lt;b&gt;Battlecry:&lt;/b&gt; If your deck has no duplicates, summon King Krush"""
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & Summon(CONTROLLER,"ULD_156t3")
class ULD_156t3:
	pass

