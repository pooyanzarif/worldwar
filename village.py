# coding: utf-8

from random import *
import datetime
from objects import *
from configuration import *
from db import tdb

"""
Format:
World= [users:{userid:int,villge:tvillage}]
weapons={'wid':int,count:int}
"""

# ----------------------------------------------------------------------------------------------------------------------
#     This function find a weapon based on id in weapon list on objects.py
def find_weapon(id):
    result = {}
    for w in WEAPONS:
        if w['wid'] == id:
            result = w
            break
    return result

#-----------------------------------------------------------------------------------------------------------------------
#This class is village. For each user we create an instance and we store them in a list in world instance.
#-----------------------------------------------------------------------------------------------------------------------
class tvillage:
    db = 0      # db object to write to databse
    vid = 0     # unique Village id
    userid = 0   # Telegram userid
    name = 'Unknown'  # Name of village
    username = ''   # Telegram username
    first_name= ''  # first name
    last_name = ''  # Last name
    score = 0       # score
    food = 0        # amount of food
    gold = 0        # amount of gold
    wood = 0        # amount of wood
    farm_capacity = 0   # capacity of farms. Each farm has a capacity to farm after some time it you can not farm in the farm land and have to create some new.
    worker = 0      # Number of Workers
    colony = []     # Is used in future.
    colonial = 0    # Is used in future.
    farm_unit = 0   #  number of farm
    worker_randeman = 0 # worker randeman. the more the more food and wood you get
    solduer_skill = 0   # Skills of solduers. the more skills, the more power in wars
    weapons = []        # list of weapons
    power_attack=0      # how much power in attack. calculated by solduer skills nad weapons
    power_defence=0     # how much power in attack. calculated by solduer skills nad weapons
    food_price = 0      # Price of food if you want to sell
    wood_price = 0      # Price of wood if you want to sell
    home = 0            # number of houses
    home_capacity = 0   # capacity of each house
    era = 0             # era of village
    race = ''           # race: 'Human','Orc','Elf', 'Undead'
    fa = 0              # Finite Automata  Not used
    food_empty = False      # True if food ==0
    farm_empty = False      # True if farm ==0
    operation = ''          # each operation a user does.  first it is inserts in this property and after operation_time is executed.
    operation_time = 0      # how much operation should be wait to be executed.
    weapon_modified = False # True if number of weapons changes.
    tired = 0               # after attack this property set by TIRED_TIME. and you can not attack again until this become zero again
    shield = 0              # if not zero, you have a shield and nobody can attack you. Until this becomes zero again.
    fast = 0                # if not zero, operations is executed immediately and user does not have to wait. after executing of each operation fast decrease one unit  and if this become zero user has to wait again.
    last_visit = 0          # date and time of last activity
    dirty = False           # if True Update function write properties to database if False, it means there is no need to update.

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,config, village): # we need cursor to write village activity in log table
        self.db=tdb(config)
        self.load(village)

    # ------------------------------------------------------------------------------------------------------------------
    # This function load village properties  by given object.
    def load(self, village):
        self.vid = village['vid']
        self.userid = int(village['userid'])
        self.username= village['username']
        self.first_name =  village['first_name']
        self.last_name =  village['last_name']
        if (village['name']=='') or (village['name']== 'None'):
            self.name = self.first_name
        else:
            self.name = village['name']
        self.score = village['score']
        self.food = village['food']
        self.gold = village['gold']
        self.wood = village['wood']
        self.farm_capacity = village['farm_capacity']
        self.worker = village['worker']
        self.farm_unit = village['farm_unit']
        self.worker_randeman = village['worker_randeman']
        self.soldier_skill = village['soldier_skill']
        self.food_price = village['food_price']
        self.wood_price = village['wood_price']
        self.home = village['home']
        self.home_capacity = village['home_capacity']
        self.weapons = village['weapons']
        self.power_attack =  village['power_attack']
        self.power_defence = village['power_defence']
        self.era = village['era']
        self.race = village['race']
        self.fa = 0
        self.dirty = False
        self.food_empty = True
        self.farm_empty = True
        self.operation = village['operation']
        self.operation_time = village['operation_time']
        self.shield = village['shield']
        self.fast = village['fast']
        self.tired = village['tired']
        self.last_visit = village['last_visit']
        self.weapon_modified = False

    # ------------------------------------------------------------------------------------------------------------------
    # This function writes village data on database
    def update(self):
        return
        if not self.dirty:  #if nothing has changed ,  do not save to database
            return
        self.update_weapons()
        sql = "update village set name='%s', score= %i , food = %i, gold = %i, wood = %i, farm_capacity = %i, farm_unit = %i,worker= %i ,worker_randeman = %f," \
              " soldier_skill = %f, food_price = %f, wood_price = %f, era= %i , race = '%s',operation= '%s' ,operation_time = %i , shield = %i ,fast = %i , tired = %i ," \
              "power_attack = %i ,power_defence = %i  ,username= '%s' , first_name= '%s' , last_name = '%s' , last_visit='%s' , home= %i, home_capacity= %i  where vid= %i;" % (
                  self.name,
                  self.score,
                  self.food,
                  self.gold,
                  self.wood,
                  self.farm_capacity,
                  self.farm_unit,
                  self.worker,
                  self.worker_randeman,
                  self.soldier_skill,
                  self.food_price,
                  self.wood_price,
                  self.era,
                  self.race,
                  self.operation,
                  self.operation_time,
                  self.shield,
                  self.fast,
                  self.tired,
                  self.power_attack,
                  self.power_defence,
                  self.username,
                  self.first_name,
                  self.last_name,
                  str(self.last_visit),
                  self.home,
                  self.home_capacity,
                  self.vid
              )
        self.db.execute(sql)
        self.db.close()
        self.dirty = False
        return
    # ------------------------------------------------------------------------------------------------------------------
    # This function suggest opponent  for attack. It chooses villages which their defense powers is near to your attack power.
    def suggest_opponent(self):
        sql = "select vid,userid,name,race, ABS(power_defence-%d) as nearest from village where shield = 0 and vid<>%d  and disabled=FALSE order by nearest limit %d" % (
        self.power_attack, self.vid,OPPONENT_COUNT)
        self.db.execute(sql)
        villages = self.db.fetchall()
        self.db.close()
        result = ""
        for v in villages:
            uid = (v['userid'])
            uid = KEY - uid  # We subtrace Telegram user id form KEY to encode user_id
            name = v['name']
            race = v['race']
            result += u"%s (%s) /profile%d\n" % (name, race, uid)
        return result

    # ------------------------------------------------------------------------------------------------------------------
    # When you choose an operation. first it is inserted into village operation property and operation_time is set. Then we count down operation timer, when it became zero operation starts.
    def insert_operation(self, operation, time):
        if self.operation != '':
            return BUSSY
        else:
            self.operation = operation
            self.operation_time = time
            self.last_visit = datetime.datetime.now()
            return PENDDING

    # ------------------------------------------------------------------------------------------------------------------
    # This function write weapons into database
    def update_weapons(self):
        return
        if not self.weapon_modified:
            return
        if not self.weapons:
            return  # it means there is no weapon to insert
        weaponlist = ""
        for w in self.weapons:
            weaponlist += "(%i,%i,%i)," % (self.vid, w['wid'], w['count'])
        weaponlist = weaponlist[:-1]  # to remove last camma (,)
        sql = "INSERT INTO weapons (vid,wid,wcount) values \n %s ON DUPLICATE KEY UPDATE wcount= VALUES(wcount) ;" % (
            weaponlist)
        self.db.execute(sql)
        self.db.close()
        self.weapon_modified = False
        return True

    # ------------------------------------------------------------------------------------------------------------------
    # This function calculate the sum of weapons
    def weapon_count(self):
        sum = 0
        for w in self.weapons:
            sum+=w['count']
        return sum
    # ------------------------------------------------------------------------------------------------------------------
    # When you want to do an operation, first you should pay some resources. This function subtract the operation resource which is needed from village resources.
    def get_resource_to_make(self,action,wid=0):
        if action== 'weapon':
            w = find_weapon(wid)
            self.gold -=w['cost'].get('gold',0)
            self.wood -=w['cost'].get('wood',0)
            self.food -=w['cost'].get('food',0)
        else:
            self.gold -= COSTS[action].get('gold', 0)
            self.wood -= COSTS[action].get('wood', 0)
            self.food -= COSTS[action].get('food', 0)
        return
    # ------------------------------------------------------------------------------------------------------------------
    # This function check whether your resource is enough for your operation or not.
    def check_resources(self,action, wid = 0):
        if (action=='home')and(self.home/self.home_capacity>=HOME_LIMIT):
            return NOHOMEALLOWED
        if (action=='worker') or (action== 'weapon'):
            if self.worker+self.weapon_count()> self.home:
                return NOHOME
            elif action == 'weapon':
                w=find_weapon(wid)
                if (self.gold < w['cost'].get('gold',0)):
                    return NOGOLD
                elif(self.wood<w['cost'].get('wood',0)):
                    return NOWOOD
                elif(self.food <w['cost'].get('food',0)):
                    return NOFOOD
                else:
                    return SUCCESSFULL

        if (self.gold< COSTS[action].get('gold',0)):
            return NOGOLD
        elif(self.wood<COSTS[action].get('wood',0)):
            return NOWOOD
        elif(self.food<COSTS[action].get('food',0)):
            return NOFOOD
        return SUCCESSFULL
    # ------------------------------------------------------------------------------------------------------------------
    # This function insert worker operation into operation property to be done after its time. if fast property is more than 0. this will happen immediately. and  fast property decreases
    def worker_preparation(self, execute=0):
        if execute == 0:
            result= self.check_resources('worker')
            if result==SUCCESSFULL:
                self.get_resource_to_make('worker')
                if self.fast:
                    self.fast -= 1
                    return self.worker_preparation(1)
                else:
                    return self.insert_operation('worker', COSTS['worker']['time'])
            else:
                return result

        else:  # execute ==1
            self.worker += 1
            self.score += SCORES['worker']
            self.log('worker',1)
            self.dirty = True
            self.update()
            return SUCCESSFULL

    # ------------------------------------------------------------------------------------------------------------------
        # This function insert farmer operation into operation property to be done after its time. if fast property is more than 0. this will happen immediately. and you loos one fast.
    def farm_preparation(self, execute=0):
        if execute == 0:
            result = self.check_resources('farm')
            if result == SUCCESSFULL:
                self.get_resource_to_make('farm')
                if self.fast:
                    self.fast -= 1
                    return self.farm_preparation(1)
                else:
                    return self.insert_operation('farm', COSTS['farm']['time'])
            else:
                return result
        else:  # execute ==1
            self.farm_capacity += self.farm_unit
            self.farm_empty = False
            self.score += SCORES['farm']
            self.log('farm',int(self.farm_unit))
            self.dirty = True
            self.update()
            return SUCCESSFULL
    # ------------------------------------------------------------------------------------------------------------------
    # When you load your village from database. you should calculate how much wood,food you have gotten and how much food you have eaten. This village has done during last activity.
    def calc_farming_eating_wooding(self):
        now = datetime.datetime.now()
        diff = now - self.last_visit
        seconds = (diff.days) * 86400 + diff.seconds
        steps = seconds / STEP_TIME
        self.farming(steps)
        self.wooding(steps)
        self.eating(steps)
        return
    # ------------------------------------------------------------------------------------------------------------------
    # This function add food to your village depends  on how many worker do you have. and give you some SCORE
    def farming(self,steps=1):
        if (datetime.datetime.now() - self.last_visit).days> 21:
            return False
        if self.farm_capacity:
            if self.farm_capacity > steps:
                self.food += steps*(self.worker * self.worker_randeman) * FARMING
                self.food_empty = False
                self.farm_capacity -= steps
                self.score += steps*SCORES['farming']
                self.dirty = True
                return True
            else:   # number of steps are more then farm_capacity. So we must add as much as farm capacity
                self.food += self.farm_capacity * (self.worker * self.worker_randeman) * FARMING
                self.food_empty = False
                self.score += self.farm_capacity * SCORES['farming']
                self.farm_capacity = 0
                self.dirty = True
                return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
        # This function decrease food to your village depends  on how many worker do you have.
    def eating(self,steps = 1):
        if (datetime.datetime.now() - self.last_visit).days> 21:
            return False
        if self.food:
            self.food -= (steps*self.worker*self.weapon_count() * FOOD_CONSUME)
            if self.food < 0:
                self.food = 0
            self.dirty = True
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    # This function add wood to your village depends on how many worker do you have. and give you some SCORE
    def wooding(self,steps = 1):
        if (datetime.datetime.now() - self.last_visit).days> 21:
            return False
        self.wood += round(steps*WOOD_COEFFICIENT*self.worker * self.worker_randeman)
        self.score += steps*SCORES['wooding']
        self.dirty = True
        return True

    # ------------------------------------------------------------------------------------------------------------------
    # This function add some weapons by admin.
    def weapon_add_byadmin(self,weapon_id,count):
        found = False
        for w in self.weapons:
            if w['wid'] == weapon_id:
                w['count'] += count
                found = True
                break
        if not found:
            self.weapons.append({'wid': weapon_id, 'count': count})
        self.power_attack = self.weapon_power('attack')
        self.power_defence = self.weapon_power('defence')
        self.dirty = True
        self.weapon_modified = True
    # ------------------------------------------------------------------------------------------------------------------
    # This function insert farmer operation into operation property to be done after its time. if fast property is more than 0. this will happen immidiately and  fast descearse
    def weapon_making(self, weapon_id, execute=0):
        new_weapon = find_weapon(weapon_id)
        if execute == 0:
            result = self.check_resources('weapon',weapon_id)
            if result == SUCCESSFULL:
                self.get_resource_to_make('weapon',weapon_id)
                if self.fast:
                    self.fast -= 1
                    return self.weapon_making(weapon_id,1)
                else:
                    return self.insert_operation('weapon:' + str(weapon_id), new_weapon['cost']['time'])
            else:
                return result

        else:  # execute ==1
            self.operation = ''
            self.operation_time = 0
            found = False
            for w in self.weapons:
                if w['wid'] == weapon_id:
                    w['count'] += 1
                    found = True
                    break
            if not found:
                self.weapons.append({'wid': weapon_id, 'count': 1})

            self.score += SCORES['weapon']
            self.weapon_modified = True
            self.power_attack = self.weapon_power('attack')
            self.power_defence = self.weapon_power('defence')
            self.log('weapon',int(weapon_id))
            self.dirty = True
            return SUCCESSFULL

    #-------------------------------------------------------------------------------------------------------------------
    # This function insert home operation into operation property to be done after its time. if fast property is more than 0. this will happen immediately and fast decrease
    def home_building(self,execute=0):
        if execute==0:
            result = self.check_resources('home')
            if result == SUCCESSFULL:
                self.get_resource_to_make('home')
                if self.fast:
                    self.fast-=1
                    return self.home_building(1)
                else:
                    return self.insert_operation('home',COSTS['home'].get('time'))
            else:
                return result
        else: #execute == 1
            self.home += self.home_capacity
            self.dirty = True
            self.log('home',1)
            self.update()
            return SUCCESSFULL

    #-------------------------------------------------------------------------------------------------------------------
    # if type is attack: This function calculate attack power of all weapons of the village
    # if type is defence: This function calculate defence power of all weapons of the village
    def weapon_power(self, type):  # type : attack or defence   # This function calculate the power of a village (attack power or defence power)
        self.check_skill()
        power = 0
        for weapon in self.weapons:
            w = find_weapon(weapon['wid'])
            power += (w['ranged'] * WAR_FACTOR[type]['ranged']
                      + w['mele'] * WAR_FACTOR[type]['mele']
                      + w['defance'] * WAR_FACTOR[type]['defence']) * weapon['count']
        return self.soldier_skill * power

    # ----------------------------------------------------------------------------------------------------------------------
    #  This function removes  weapons by the chance of 'chance'. This is used in attack. Beacuase in attacks we loose some weapons
    def remove_weapon(self, chance):
        self.weapon_modified = True
        broken_weapon_count=0
        exist_weapons= filter(lambda x:x['count']>0,self.weapons)
        for w in exist_weapons:
            # if random() < chance:
            if random() < 0.35:
                if w['count'] >= 0:
                    broken = min(int(w['count']*chance),w['count']) # if broken is bigger than wcount broken set to wcount
                    w['count'] -= broken
                    # w['count'] -= 1
                    broken_weapon_count+=broken
        self.power_attack = self.weapon_power('attack')
        self.power_defence = self.weapon_power('defence')
        self.home -=broken_weapon_count
        self.dirty = True
        return broken_weapon_count
    #-------------------------------------------------------------------------------------------------------------------
    # In this function, first we calculate distance between villages,(we assume that villages are organized in ad 10x N matix).
    # we calculate manhatan distance and atmost 30. Then we put sattack operation in opration property and distance in operation time.
    # On attack: we calculats the attack power of attacker and defense power of eney. and we multiply the powers by random number between (0.9 - 1.1) for attacker and (0.8 - 1.2) for enemy
    # we calculate ide time from last login  and subtract the power.
    # Two powers subtracts and winner  will identified. By the chance of GENETIC_MUTATION looser and winner swaps.
    #Finally some weapons are removed by chance of  power and some food,wood, gold is taken from looser and gives to the winner and winner get some SCORE

    def attack(self, enemy=None, execute=0):
        if execute == 0:
            result = self.check_resources('attack')
            if (self.weapons) and (result==SUCCESSFULL):
                self.get_resource_to_make('attack')
                x1 = self.vid//10
                y1 =self.vid %10
                x2= enemy.vid//10
                y2=enemy.vid%10
                distance = abs(x2-x1)+abs(y2-y1)
                distance = min(distance,30)
                result = self.insert_operation('attack:' + str(enemy.userid), distance)
                if result == PENDDING:
                    attacker_message = YOU_ATTACK % (enemy.name,distance)
                    idle_time = datetime.datetime.now() - enemy.last_visit
                    idle_hours = round((idle_time.days * 86400 + idle_time.seconds) / 3600)
                    if idle_hours:
                        enemy_message = DECLARE_WAR_IDLE % (self.name,idle_hours)
                    else:
                        enemy_message = DECLARE_WAR % (self.name)
                    return (attacker_message, enemy_message)
            else:
                return (MESSAGES[result],"")

        my_power = randint(90, 110) / 100.0 * self.power_attack
        if my_power==0:
            my_power=1  #power at least is 1 beacaues if it is zero expression "diff/mypower" raised an exception devision by zero
        # if not self.weapons:
        #     return (RESOURCE_IS_NOT_ENOUGH, "")
        self.tired = TIRED_TIME
        idle = enemy.idle_factor()
        enemy_power = randint(80, 120) / 100.0 * enemy.power_defence
        enemy_power -= idle * enemy_power   # reduce enemy power according to idle hour factor
        if enemy_power==0:
            enemy_power=1 #power at least is 1 beacaues if it is zero expression "diff/enemy_power" raised an exception devision by zero
        diff = my_power - enemy_power

        if randint(0, GENETIC_MUTATION) == 1:
            diff = -diff  # maybe the weak army won
            print("Wow! weaker won!")
        if diff > 0:  # if you as attacker win
            gold = int(enemy.gold * WAR_COMPENSATION)
            wood = int(enemy.wood * WAR_COMPENSATION)
            food = int(enemy.food * WAR_COMPENSATION)

            # We do not give compendsation to winner if looser has less than default
            if (enemy.food-food)<=DEFAULTS['food']: food=0
            if (enemy.wood-wood)<=DEFAULTS['wood']: wood=0
            if (enemy.gold-gold)<=DEFAULTS['gold']: gold=0

            self.gold += gold
            self.wood += wood
            self.food += food
            score = int((enemy_power/my_power)*SCORES['winning']+5)
            if score > SCORES['winning']:
                score = 200
            self.score += score

            soldier_skill = (0.05+int(enemy_power/my_power*100)/100*0.3)
            if  soldier_skill>0.4:
                soldier_skill = 0.4
            self.soldier_skill += soldier_skill
            self.soldier_skill = int(self.soldier_skill*100+0.05)/100.0
            result = (ATTACKER_WON % (score, gold, wood, food), YOU_DEFEATED%(self.name))
            enemy.gold -= gold
            enemy.wood -= wood
            enemy.food -= food
            enemy.worker -= int(enemy.worker * WAR_COMPENSATION)
            enemy.shield = SHIELD_TIME      # give the looser time to recover himself
            chance = diff / my_power

            enemy_broken_weapon_count = enemy.remove_weapon(chance)
            my_broken_weapon_count = self.remove_weapon(chance*WINNER_BROKEN_WEAPON)
            self.log('attackto',enemy.userid,'result','won','gold',gold,'wood',wood,'food',food,'mybrokenweapon',my_broken_weapon_count,'enemybrokenweapon',enemy_broken_weapon_count)

        elif diff < 0:  # if you loose the war!
            result = (YOU_DEFEATED%(enemy.name), ENEMY_WON%(self.name))
            chance = -diff / enemy_power
            my_broken_weapon_count=self.remove_weapon(chance)
            enemy_broken_weapon_count=self.remove_weapon(chance*WINNER_BROKEN_WEAPON)
            self.log('attackto', enemy.userid, 'result', 'defeated', 'gold', 0, 'wood', 0, 'food', 0,
                     'mybrokenweapon', my_broken_weapon_count, 'enemybrokenweapon', enemy_broken_weapon_count)
        else:  # two army are equal
            result = (YOU_DRAW, YOU_DRAW)
            self.log('attackto', enemy.userid, 'result', 'draw', 'gold', 0, 'wood', 0, 'food', 0,
                     'mybrokenweapon', 0, 'enemybrokenweapon', 0)
        self.dirty = True
        self.update()
        return result

    # ------------------------------------------------------------------------------------------------------------------
    # This function calculate how idle was a village from his/her last activity. It returns a number between (0-0.45)
    def idle_factor(self):
        IDLE_FACTORS = (0.03,0.02,0.005)
        idle_time = datetime.datetime.now() - self.last_visit
        idle_hours = round((idle_time.days * 86400 + idle_time.seconds) / 3600)
        if idle_hours<= 6:   # less than 6 hours
            factor= IDLE_FACTORS[0]*idle_hours
        elif idle_hours<=12:
            factor = IDLE_FACTORS[0]*6+IDLE_FACTORS[1]*(idle_hours-6)
        else:
            factor = (IDLE_FACTORS[0] + IDLE_FACTORS[1]) * 6 + IDLE_FACTORS[2]*(idle_hours-12)
        factor = min(factor,0.45)   # if factor is grater then 0.40 set it ot 0.40
        return factor


    # ------------------------------------------------------------------------------------------------------------------
    # This function decrease food or wood and increase gold
    def sell(self, type, amount):  # type : food or wood
        if type == 'food':
            if amount <= self.food:
                gold = int(self.food_price * amount)
                self.gold += gold
                self.food -= amount
                self.log('sell','food','food',amount,'gold', gold)
            else:
                return NOFOOD
        elif type == 'wood':
            if amount <= self.wood:
                gold = int(self.wood_price * amount)
                self.gold += gold
                self.wood -= amount
                self.log('sell', 'wood', 'wood', amount, 'gold', gold)
            else:
                return NOWOOD
        self.dirty = True
        return SOLD

    # ------------------------------------------------------------------------------------------------------------------
    # This function display the weapon list depends on era
    def menu_weapons(self):
        return filter(lambda x: x['era'] <= self.era, WEAPONS)

    # ------------------------------------------------------------------------------------------------------------------
    # This function shows village properties to user
    def status(self):
        wst = ""
        st = ''
        for w in self.weapons:
            weapon = find_weapon(w['wid'])
            wst += u"      %s:%i\n" % (weapon['title'], w['count'])

        st += STATUS % (
            self.name, self.era,self.home/self.home_capacity,self.home_capacity, self.food, self.wood, self.gold, self.worker, self.farm_capacity, wst,self.soldier_skill, self.score,self.operation)
        if self.name == self.first_name:
            st+="--------------------------------\n%s"%(NO_VIILAGE_NAME)
        self.log('status',1)
        return st

    # ------------------------------------------------------------------------------------------------------------------
    # This function set the race of village
    def set_race(self, race):
        self.race = race
        self.dirty = True

    # ------------------------------------------------------------------------------------------------------------------
    # This function get the name of village from the user and set
    def rename(self, name,username='',first_name='',last_name=''):
        self.name = name
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.dirty = True
        return
    # -----------------------------------------------------------------=============------------------------------------
    # This function write all activities into database
    def log(self,*action):
        sql = "insert into log (userid,action) VALUES(%d,JSON_OBJECT %s)"%(self.userid,action)
        try:
            self.db.execute(sql)
            self.db.close()
        except Exception as e:
            print(str(e))
            print(sql)
            print("Error in logging: %d , %s"%(self.userid,action))
            self.db.close()


    # -----------------------------------------------------------------------------=============------------------------
    #  This function calculate the skill property depends on last activity.
    def check_skill(self):
        now = datetime.datetime.now()
        diff = now-self.last_visit
        if (diff.days>1):
            self.soldier_skill-=diff.days*0.05
        if self.soldier_skill<1:
            self.soldier_skill = 1.0
        return

    # --------------------------------------------------------------------------------=============---------------------
    # This function reset default to village and write in database
    def reset(self):
        self.gold = DEFAULTS['gold']
        self.wood = DEFAULTS['wood']
        self.food = DEFAULTS['food']
        self.home = 10
        self.dirty = True
        self.update()