import datetime
from db import tdb
from village import tvillage
from objects import *
from configuration import *
# ----------------------------------------------------------------------------------------------------------------------
# This is the world class, which contains Village list in form of World= [users:{userid:int,villge:tvillage}]
 #Only one instance is created in the program.
# ----------------------------------------------------------------------------------------------------------------------
class tworld:
    users = []  # list of users
    db = 0      # db class to connect to mysqlserver
    world_map = [[]]        # not used
    _config={}              # database configs
    # ------------------------------------------------------------------------------------------------------------------
    # In this function we connect to the game database and initialize db class.
    def __init__(self, config):
        self._config=config
        self.db = tdb(config)
        self.fetch_busy_villages()  #This function loads villages which has an operation to do.
    # ------------------------------------------------------------------------------------------------------------------
    def is_exist(self,userid):
        sql = "select count(*) as N from village where userid = %d" % (userid)
        self.db.execute(sql)
        c=self.db.fetchall()[0]['N']
        if c==0:
            return False
        else:
            True

    # ------------------------------------------------------------------------------------------------------------------
    # This function fetch all properties of a village from the database.
    def fetch_one(self,userid=None,vid = None):
        if vid != None:
            sql = "select * from village where vid = %d"%(vid)
        elif userid != None:
            sql = "select * from village where userid = %d"%(userid)
        c = self.db.execute(sql)
        if c:
            village = self.db.fetchone()
            village.update({'fa':0})
            self.db.execute("select * from weapons where vid = %d" % village['vid'])
            weapons = self.db.fetchall()
            w = []
            for weapon in weapons:
                w.append({'wid': weapon['wid'], 'count': weapon['wcount']})
            village['weapons'] = w
            user = {'userid': village['userid'],
                    'village': tvillage(self._config, village)}  # in this line we create village for each user
            self.users.append(user)
            self.db.close()
            return user['village']
        else:
            self.db.close()
            raise LookupError
    # ---------------------------------------------------------------------------------------------------------------------
    # This function Fetches all of village from database and stores in a list in world class
    # def fetch_all(self):
    #     self.db.execute("select * from village")
    #     villages = self.db.fetchall()
    #     for village in villages:
    #         village['fa'] = 0
    #         self.db.execute("select * from weapons where vid = %i" % village['vid'])
    #         weapons = self.db.fetchall()
    #         w = []
    #         for weapon in weapons:
    #             w.append({'wid': weapon['wid'], 'count': weapon['wcount']})
    #         village['weapons'] = w
    #         user = {'userid': village['userid'], 'village': tvillage(self._config,village)}  # in this line we create village for each user
    #     self.users.append(user)
    #     self.db.close()

    # ------------------------------------------------------------------------------------------------------------------
    # Sometimes server stops while some villages are doing something.(e.g creating a worker). So This function load Those villages that have an operation to do.
    def fetch_busy_villages(self):
        self.db.execute("select * from village where operation <> '' ")
        villages = self.db.fetchall()
        for village in villages:
            print("I am loading: %s"%(village['name']))
            village['fa'] = 0
            self.db.execute("select * from weapons where vid = %i" % village['vid'])
            weapons = self.db.fetchall()
            w = []
            for weapon in weapons:
                w.append({'wid': weapon['wid'], 'count': weapon['wcount']})
            village['weapons'] = w
            user = {'userid': village['userid'],
                    'village': tvillage(self._config, village)}  # in this line we create village for each user
            self.users.append(user)

        self.db.close()

    # ------------------------------------------------------------------------------------------------------------------
    # this function writes user's messages in database
    def log_message(self,from_id,to_id,message,msg_admin=0):
        sql = "insert into messages (msg_from,msg_to,msg_message,msg_admin) values (%s,%s,'%s',%s)"%(from_id,to_id,message,msg_admin)
        self.db.execute(sql)
        self.db.close()

    # ------------------------------------------------------------------------------------------------------------------
    # This function writes weapons of a village in database
    def update_weapons(self,village):
        if not village.weapon_modified:
            return
        if not village.weapons:
            return  # it means thers is no weapon to insert
        weaponlist = ""
        for w in village.weapons:
            weaponlist += "(%i,%i,%i)," % (village.vid, w['wid'], w['count'])
        weaponlist = weaponlist[:-1]  # to remove last camma (,)
        sql = "INSERT INTO weapons (vid,wid,wcount) values \n %s ON DUPLICATE KEY UPDATE wcount= VALUES(wcount) ;" % (
            weaponlist)
        self.db.execute(sql)
        self.db.close()
        village.weapon_modified = False
        return True

    # ------------------------------------------------------------------------------------------------------------------
    # This function writes a village properties into database.
    def update(self,village):
        if not village.dirty:  #if nothing has changed ,  do not save to database
            return
        self.update_weapons(village)
        sql = "update village set name='%s', score= %i , food = %i, gold = %i, wood = %i, farm_capacity = %i, farm_unit = %i,worker= %i ,worker_randeman = %f," \
              " soldier_skill = %f, food_price = %f, wood_price = %f, era= %i , race = '%s',operation= '%s' ,operation_time = %i , shield = %i ,fast = %i , tired = %i ," \
              "power_attack = %i ,power_defence = %i  ,username= '%s' , first_name= '%s' , last_name = '%s' , last_visit='%s' , home= %i, home_capacity= %i  where vid= %i;" % (
                  village.name,
                  village.score,
                  village.food,
                  village.gold,
                  village.wood,
                  village.farm_capacity,
                  village.farm_unit,
                  village.worker,
                  village.worker_randeman,
                  village.soldier_skill,
                  village.food_price,
                  village.wood_price,
                  village.era,
                  village.race,
                  village.operation,
                  village.operation_time,
                  village.shield,
                  village.fast,
                  village.tired,
                  village.power_attack,
                  village.power_defence,
                  village.username,
                  village.first_name,
                  village.last_name,
                  str(datetime.datetime.now()),
                  village.home,
                  village.home_capacity,
                  village.vid
              )
        try:
            self.db.execute(sql)
            village.dirty = False
            self.db.close()
        except Exception as e :
            print( "TYPE: ",type(e))
            print("ARGS: ",e.args)


    # ------------------------------------------------------------------------------------------------------------------
    # This function write all changes of villages into database.
    def update_all(self):
        for user in self.users:
            try:
                self.update(user['village'])
            except Exception as e :
                 print("TYPE: ",type(e))
                 print("ARGS: ",e.args)
                 print("vid : %d  rollbacked!"%(user['village'].vid))
                 self.db.rollback()
    # ------------------------------------------------------------------------------------------------------------------
    # this function create a village, assignes default values to properties and write to database
    def create_village(self, userid,username='',first_name='',last_name='', inviter=0):
        village = {}
        village['userid'] = userid
        village['username'] = username
        village['first_name'] = first_name
        village['last_name'] = last_name
        if first_name!="":
            village['name'] =  first_name
        elif username!="None":
            village['name'] =  username
        else:
            village['name'] = last_name
        village['score'] = 0
        village['food'] = DEFAULTS['food']
        village['gold'] = DEFAULTS['gold']
        village['wood'] = DEFAULTS['wood']
        village['farm_capacity'] = 0
        village['worker'] = 0
        village['farm_unit'] = DEFAULTS['farm_unit']
        village['worker_randeman'] = 1
        village['soldier_skill'] = 1
        village['food_price'] = DEFAULTS['food_price']
        village['wood_price'] = DEFAULTS['wood_price']
        village['weapons'] = []
        village['power_attack'] = 0
        village['power_defence'] = 0
        village['home']= 0
        village['home_capacity'] = HOME_CAPACITY
        village['era'] = 0
        village['race'] = ''
        village['operation'] = ''
        village['operation_time'] = 0
        village['last_visit'] = datetime.datetime.now()
        village['shield'] = SHIELD_TIME
        village['fast'] = 0
        village['tired'] = 0
        village['fa'] = 1
        v = (village['userid'],
             village['username'],
             village['first_name'],
             village['last_name'],
             village['score'],
             village['food'],
             village['gold'],
             village['wood'],
             village['farm_capacity'],
             village['worker'],
             village['farm_unit'],
             village['worker_randeman'],
             village['soldier_skill'],
             village['food_price'],
             village['wood_price'],
             village['home'],
             village['home_capacity'],
             village['era'],
             village['power_attack'],
             village['power_defence'],
             village['operation'],
             village['operation_time'],
             village['shield'],
             village['fast'],
             village['tired'],
             str(village['last_visit'])
             )
        sql = """insert IGNORE into village
            (userid,
            username,
            first_name,
            last_name,
            score,
            food,
            gold,
            wood,
            farm_capacity,
            worker,
            farm_unit,
            worker_randeman,
            soldier_skill,
            food_price,
            wood_price,
            home,
            home_capacity,
            era,
            power_attack,
            power_defence,
            operation,
            operation_time,
            shield,
            `fast`,
            tired,
            last_visit
            ) values( % s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s' , %s, %s ,%s,%s,'%s');""" % v


        self.db.execute(sql)
        is_inserted = self.db.cursor.rowcount
        if is_inserted:
            village['vid'] = self.db.cursor.lastrowid
            self.db.commit()
            if inviter!=0:
                self.bonus(inviter)
                invite_sql = "insert into invite (inviter_id,invited_id,accept_date) VALUES (%d,%d,NOW())" % ( inviter, userid)
                self.db.execute(invite_sql)
            user = {'userid': village['userid'], 'village': tvillage(self.db,village)}
            self.users.append(user)
            self.db.close()
            return True
        else:
            return False
    # ------------------------------------------------------------------------------------------------------------------
    # This function first searches in world by Telegram userid.users list. if village not found. lookit yp from database and append to world.users.

    def find_village(self, userid):
        user = list(filter(lambda x: x['userid'] == userid, self.users))
        if user:
            v = user[0]['village']
            v.calc_farming_eating_wooding()
            self.update(v)
            return v
        else:
            try:
                v = self.fetch_one(userid = userid)
                v.calc_farming_eating_wooding()
                self.update(v)
                return v
            except LookupError as e:
                raise LookupError

    # ------------------------------------------------------------------------------------------------------------------
    # This function first searches in world by village id.users list. if village not found. lookit yp from database and append to world.users.
    def find_by_vid(self,vid):
        user = filter(lambda x: x['vid'] == vid, self.users)
        if user:
            v = user[0]['village']
            v.calc_farming_eating_wooding()
            self.update(v)
            return v
        else:
            v = self.fetch_one(vid = vid)
            v.calc_farming_eating_wooding()
            self.update(v)
            return v

   # -------------------------------------------------------------------------------------------------------------------
   #  This function display top villages depends on scores
    def top10(self,user_id):
        self.db.execute("select vid,name,score from village order by score DESC limit 10")
        list = self.db.fetchall()
        self.db.close()
        # list= sorted(self.users, key = lambda x: x['village'].score , reverse=True)
        v=self.find_village(user_id)
        i=0
        for l in list:
            i+=1
            if l['vid'] == v.vid:
                break

        list=list[:10]
        result=""
        for l in list:
            result+= "%s : %d \n"%(l['name'], l['score'])
        result+= u"--------------------\n"
        result+= YOUR_RANK+": %s"%i
        return result

    # ------------------------------------------------------------------------------------------------------------------
    #  weapon number 6(Catapults) is bonus. This function give Catapults to who invite somebody to this game, give him/her score and change the era
    def bonus(self, inviter):
        v = self.find_village(inviter)
        if v != False:
            v.weapon_making(6,1)    # 6 means Catapults.
            v.gold +=  SCORE_BONUS
            if v.era == 0:
                v.era = 1
        return

    # ------------------------------------------------------------------------------------------------------------------
    #  This function uses for admin panel. By this function admin can add , subtract or update village properties such as (gold, food, wood ,...)
    def load_or_increament(self,village_value, value):
        try:
            if value[0] == '+':
                return village_value + int(value[1:])
            elif value[0] == '-':
                return village_value - int(value[1:])
            else:
                return int(value)
        except:
            return 0

