import random
from utils import *
     
class takasho002(Agent):    
     def __init__(self, myName: str, myFunction, myOption = [], myClass: CardClass = CardClass.HUNTER, rating =1000 ):
          super().__init__(myName, myFunction, myOption, myClass, rating )
     def agent_takasho002(self, game: Game, option=[], gameLog=[], debugLog=False):
         player = game.current_player
         while True:
              myCandidate = getCandidates(game)#���s�ł��邱�Ƃ�������X�g�Ŏ擾
              if len(myCandidate)>0:
                   myChoice = random.choice(myCandidate)#�����_���Ɉ�I��
                   if myChoice.type ==ExceptionPlay.TURNEND:#�������Ȃ���I�������Ƃ�
                       return
                   executeAction(game, myChoice, debugLog=debugLog)#�I���������̂����s
                   postAction(player)#�㏈��
              else:
                   return