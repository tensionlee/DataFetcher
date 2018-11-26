from pymongo import MongoClient
from configobj import ConfigObj


c = ConfigObj("db\config.ini", encoding='UTF8')
host = c['database']['host']
port = c['database']['port']
dbname = c['database']['db']
client = MongoClient(host=host, port=int(port))
mongo = client[dbname]


if __name__ == "__main__":
    collection = mongo.md
    print(c)
    print(mongo.monthly_data.count_documents({"date": "2018-10-31"}))
