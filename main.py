from fastapi import FastAPI 
import pydantic
from pydantic import BaseModel
import redis
import csv

class input_param(BaseModel):
    latitude: float 
    longitude: float 
    
def redis_string(t1,t2):
    file = open('data.csv')
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    print(header)
    rows = []
    cnt = 0
    r = redis.Redis(host='localhost',port=6379)
    for row in csvreader:
        d = {header[i]:row[i] for i in range(len(row))}
        r.hmset(row[2],d)
        r.geoadd("delivery-boy",[float(row[7]),float(row[6]),row[2]],nx=True,xx=False)
        cnt += 1
        if cnt==10:
            break
    name =  r.georadius("delivery-boy", t1, t2, 500)
    name = name[0]
    name = name.decode('utf-8')
    return r.hgetall(name)


app = FastAPI()
@app.post('/')
def fnc(inp1: input_param):
    longitude = inp1.longitude 
    latitude  = inp1.latitude 
    return redis_string(longitude,latitude)






