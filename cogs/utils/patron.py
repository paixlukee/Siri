from pymongo import MongoClient
import pymongo
import config

client = MongoClient(config.mongo_client)
db = client['siri']

async def check(id):
    patron = db.utility.find_one({"utility": "patrons"})
    if id in patron['gold']:
        return 'GOLD'
    elif id in patron['silver']:
        return 'SILVER'
    elif id in patron['bronze']:
        return 'BRONZE'
    else:
        return None

async def all():
    patron = db.utility.find_one({"utility": "patrons"})
    all_list = []
    for x in patron['gold']:
        all_list.append(x)
    for x in patron['silver']:
        all_list.append(x)
    for x in patron['bronze']:
        all_list.append(x)
    return all_list
