from mongoengine import *
import json
from dateutil.parser import *
from dateutil import *
from datetime import datetime, timedelta

f = open(".credential")
cred = json.loads(f.read())
f.close()

class DB():

    @staticmethod
    def enterCalories(userId, cal):
        db_client = connect("scb2018-miambot", host=cred['HOST'])
        user = User.objects(username=str(userId))
        now = parse(str(datetime.now()))
        today = str(now.date())
        if(len(user) != 1):
            todayCal = {today: cal}
            u = User(username=str(userId))
            print(todayCal)
            u.calories = todayCal
            u.save()
        else:
            u = user[0]
            exist = False
            try:
                if(u.calories[today]):
                    u.calories[today] += cal
            except (KeyError):
                u.calories[today] = cal
            u.save()

        db_client.close()

    @staticmethod
    def getCalories(userId):
        db_client = connect("scb2018-miambot", host=cred['HOST'])
        user = User.objects(username = str(userId))
        now = parse(str(datetime.now()))
        today = str(now.date())
        if(len(user) != 0):
            try:
                u = user[0]
                kcal = u.calories[today]
                db_client.close()
                return kcal
            except (KeyError):
                db_client.close()
                return 0
        else:
            return 0

    @staticmethod
    def getLast7Calories(userId):
        db_client = connect("scb2018-miambot", host=cred['HOST'])
        user = User.objects(username = userId)
        db_client.close()

class User(Document):
    username = StringField(require=True)
    calories = DictField()
