from demo import app
from flask import request
from collections import deque
import time, json
from demo import lyutil

speaker = 'Alexa'
keys = deque(maxlen = 100)
scriptIndexDict = dict()
validNames = set(['Alexa', 'Sophia'])
Loop = 162

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/ask',methods=['GET',])
def ask():
    name = request.args.get('name')
    password = request.args.get('password')

    if name in validNames:
        speaker, index = getState(password)
        while speaker != name:
            time.sleep(1)
            speaker, index = getState(password)

        return str(index)

    return "-1"

@app.route('/getdata',methods=['GET',])
def getData():
    name = request.args.get('name')
    password = request.args.get('password')
    empty_response = json.dumps(dict(status = 'empty'))

    if name in validNames:
        speaker, index = getState(password)
        if speaker != name:
            wait_response = json.dumps(dict(status = 'wait'))
            return wait_response

        print('index = {}'.format(index))
        data = lyutil.getDataByIndex(index, name)
        if data is None:
            setNextState(name, password)
            return empty_response
            
        return data

    return empty_response

def getState(pw):
    global keys
    global scriptIndexDict
    if pw not in scriptIndexDict:
        if len(keys) >= keys.maxlen:
            p = keys.popleft()
            del scriptIndexDict[p]
        keys.append(pw)
        scriptIndexDict[pw] = ('Alexa', 0)
    return scriptIndexDict[pw]

def setNextState(name, pw):
    global keys
    global scriptIndexDict
    if pw not in scriptIndexDict:
        if len(keys) >= keys.maxlen:
            p = keys.popleft()
            del scriptIndexDict[p]
        keys.append(pw)
        scriptIndexDict[pw] = ('Alexa', 0)
    
    speaker, index = scriptIndexDict[pw]
    nextName = findNextSpeaker(name)
    if speaker == name:
        nextIndex = (index + 1) % Loop
        scriptIndexDict[pw] = (nextName, nextIndex)
    return None

def findNextSpeaker(name):
    for n in validNames:
        if n != name:
            return n
    return None

@app.route('/report',methods=['GET',])
def report():
    name = request.args.get('name')
    password = request.args.get('password')
    setNextState(name, password)
    return "Hello, report!"