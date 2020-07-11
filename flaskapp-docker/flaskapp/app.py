#import dash
#import dash_core_components as dcc
#import dash_html_components as html
#import dash_bootstrap_components as dbc
from flask import Flask,render_template, url_for

from flask_sqlalchemy import SQLAlchemy

import sqlite3
#from dash.dependencies import Input, Output, State
import paho.mqtt.client as mqtt
import time
import pandas as pd
import sqlite3
import os
import json
import pathlib
import base64
from sqlalchemy import create_engine
from datetime import datetime,timedelta


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
db_URI = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
engine = create_engine(db_URI)




class User(db.Model):
    __tablename__ = 'datatable'

    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(26))
    devId = db.Column(db.String(15))
    SPA = db.Column(db.String(10))
    TA = db.Column(db.String(10))

    def __repr__(self):
        return '<User %r %r  %r %r>' % (self.stamp, self.devId, self.SPA, self.TA)

class smb(db.Model):
    __tablename__ = 'smbtable'

    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(26))
    devId = db.Column(db.String(15))
    str1 = db.Column(db.String(10))
    str2 = db.Column(db.String(10))
    str3 = db.Column(db.String(10))
    str4 = db.Column(db.String(10))
    str5 = db.Column(db.String(10))
    str6 = db.Column(db.String(10))
    str7 = db.Column(db.String(10))
    str8 = db.Column(db.String(10))
    str9 = db.Column(db.String(10))
    str10 = db.Column(db.String(10))
    str11 = db.Column(db.String(10))
    str12 = db.Column(db.String(10))
    str13 = db.Column(db.String(10))
    vol1 = db.Column(db.String(10))
    vol2 = db.Column(db.String(10))
    vol3 = db.Column(db.String(10))
    vol4 = db.Column(db.String(10))
    vol5 = db.Column(db.String(10))
    vol6 = db.Column(db.String(10))
    vol7 = db.Column(db.String(10))
    vol8 = db.Column(db.String(10))
    vol9 = db.Column(db.String(10))
    vol10 = db.Column(db.String(10))
    vol11 = db.Column(db.String(10))
    vol12 = db.Column(db.String(10))
    vol13 = db.Column(db.String(10))
    temp = db.Column(db.String(10))
    stravg=db.Column(db.Float)
    volavg=db.Column(db.Float)
    poweravg =db.Column(db.Float)

    def __repr__(self):
        return '<User %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r>' % (self.stamp, self.devId, self.str1, self.str2, self.str3, self.str4, self.str5, self.str6, self.str7, self.str8, self.str9, 
                self.str10, self.str11, self.str12, self.str13, self.vol1, self.vol2, self.vol3, self.vol4, self.vol5, self.vol6, self.vol7, self.vol8, self.vol9, self.vol10, self.vol11, self.vol12, self.vol13, self.temp, self.stravg, self.volavg, self.poweravg)

db.create_all()

def on_connect(client, userdata, flags, rc):
    print("Connected!", rc)
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_publish(client, userdata, mid):
    print("Publish:", client)

def on_log(client, userdata, level, buf):
    print("log:", buf)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

smbdict={}
def on_message(client, userdata, message):

    payload = str(message.payload.decode("utf-8"))#+" "
    
    if payload[:4]=="Dev:":
        ind=payload.index(",Time")
        teststr=payload[:ind]+payload[ind+25:]
        smbdata = dict(x.split(":") for x in teststr.split(","))
        smbdata['Time']=payload[ind+21:ind+25]+"-"+payload[ind+18:ind+20]+"-"+payload[ind+15:ind+17]+"T"+payload[ind+6:ind+14]+".000000"
        
    if payload[:6]=="DevId:":   
        data1 = dict(x.split(":") for x in payload.split(","))
        print("data1=",data1,len(data1))
        admin = User(stamp=str(datetime.now()+timedelta(minutes=330)),devId=data1['DevId'],SPA=data1['SPA'],TA=data1['TA'])
        db.session.add(admin)
        db.session.commit()
        data1.clear()
        print("Tracker data saved to database")

   
    if len(smbdata)==4:
        if (smbdata['Dev'] not in smbdict):
            smbdict[smbdata['Dev']]={}
            smbdict[smbdata['Dev']]['Dev']=smbdata['Dev']
            smbdict[smbdata['Dev']]['Time']=smbdata['Time']

        if ((smbdata['Dev'] in smbdict) and ('Dev' in smbdata)):
            smbdict[smbdata['Dev']]['Dev']=smbdata['Dev']
            smbdict[smbdata['Dev']]['Time']=smbdata['Time']
            
        if ((smbdata['Dev'] in smbdict) and ('str1' in smbdata)):
            smbdict[smbdata['Dev']]['str1']=smbdata['str1']
            smbdict[smbdata['Dev']]['vol1']=smbdata['vol1']

        if ((smbdata['Dev'] in smbdict) and ('str2' in smbdata)):
            smbdict[smbdata['Dev']]['str2']=smbdata['str2']
            smbdict[smbdata['Dev']]['vol2']=smbdata['vol2']
        
        if ((smbdata['Dev'] in smbdict) and ('str3' in smbdata)):
            smbdict[smbdata['Dev']]['str3']=smbdata['str3']
            smbdict[smbdata['Dev']]['vol3']=smbdata['vol3']
        
        if ((smbdata['Dev'] in smbdict) and ('str4' in smbdata)):
            smbdict[smbdata['Dev']]['str4']=smbdata['str4']
            smbdict[smbdata['Dev']]['vol4']=smbdata['vol4']
        
        if ((smbdata['Dev'] in smbdict) and ('str5' in smbdata)):
            smbdict[smbdata['Dev']]['str5']=smbdata['str5']
            smbdict[smbdata['Dev']]['vol5']=smbdata['vol5']
        
        if ((smbdata['Dev'] in smbdict) and ('str6' in smbdata)):
            smbdict[smbdata['Dev']]['str6']=smbdata['str6']
            smbdict[smbdata['Dev']]['vol6']=smbdata['vol6']
        
        if ((smbdata['Dev'] in smbdict) and ('str7' in smbdata)):
            smbdict[smbdata['Dev']]['str7']=smbdata['str7']
            smbdict[smbdata['Dev']]['vol7']=smbdata['vol7']
        
        if ((smbdata['Dev'] in smbdict) and ('str8' in smbdata)):
            smbdict[smbdata['Dev']]['str8']=smbdata['str8']
            smbdict[smbdata['Dev']]['vol8']=smbdata['vol8']
        
        if ((smbdata['Dev'] in smbdict) and ('str9' in smbdata)):
            smbdict[smbdata['Dev']]['str9']=smbdata['str9']
            smbdict[smbdata['Dev']]['vol9']=smbdata['vol9']
        
        if ((smbdata['Dev'] in smbdict) and ('str10' in smbdata)):
            smbdict[smbdata['Dev']]['str10']=smbdata['str10']
            smbdict[smbdata['Dev']]['vol10']=smbdata['vol10']
        
        if ((smbdata['Dev'] in smbdict) and ('str11' in smbdata)):
            smbdict[smbdata['Dev']]['str11']=smbdata['str11']
            smbdict[smbdata['Dev']]['vol11']=smbdata['vol11']
        
        if ((smbdata['Dev'] in smbdict) and ('str12' in smbdata)):
            smbdict[smbdata['Dev']]['str12']=smbdata['str12']
            smbdict[smbdata['Dev']]['vol12']=smbdata['vol12']
        
        if ((smbdata['Dev'] in smbdict) and ('str13' in smbdata)):
            smbdict[smbdata['Dev']]['str13']=smbdata['str13']
            smbdict[smbdata['Dev']]['vol13']=smbdata['vol13']
       
    if ((len(smbdata)==3) and (len(smbdict[smbdata['Dev']])==28)):

        stravg=0
        stravg=float(smbdict[smbdata['Dev']]['str1'])+float(smbdict[smbdata['Dev']]['str2'])+float(smbdict[smbdata['Dev']]['str3'])+float(smbdict[smbdata['Dev']]['str4'])+float(smbdict[smbdata['Dev']]['str5'])+float(smbdict[smbdata['Dev']]['str6'])+float(smbdict[smbdata['Dev']]['str7'])+float(smbdict[smbdata['Dev']]['str8'])+float(smbdict[smbdata['Dev']]['str9'])+float(smbdict[smbdata['Dev']]['str10'])+float(smbdict[smbdata['Dev']]['str11'])+float(smbdict[smbdata['Dev']]['str12'])+float(smbdict[smbdata['Dev']]['str13'])
        stravg=float(stravg/13)
        smbdict[smbdata['Dev']]['stravg']=stravg 
        
        volavg=0
        volavg=float(smbdict[smbdata['Dev']]['vol1'])+float(smbdict[smbdata['Dev']]['vol2'])+float(smbdict[smbdata['Dev']]['vol3'])+float(smbdict[smbdata['Dev']]['vol4'])+float(smbdict[smbdata['Dev']]['vol5'])+float(smbdict[smbdata['Dev']]['vol6'])+float(smbdict[smbdata['Dev']]['vol7'])+float(smbdict[smbdata['Dev']]['vol8'])+float(smbdict[smbdata['Dev']]['vol9'])+float(smbdict[smbdata['Dev']]['vol10'])+float(smbdict[smbdata['Dev']]['vol11'])+float(smbdict[smbdata['Dev']]['vol12'])+float(smbdict[smbdata['Dev']]['vol13'])
        volavg=float(volavg/13)
        smbdict[smbdata['Dev']]['volavg']=volavg
        
        poweravg=0 
        poweravg=float((volavg*stravg)/1000)
        smbdict[smbdata['Dev']]['poweravg']=poweravg
        smbdict[smbdata['Dev']]['temp']=smbdata['temp']
        print("Inside temp smb dict=",smbdict)
        
        smbtotal = smb(stamp=smbdict[smbdata['Dev']]['Time'],devId=smbdict[smbdata['Dev']]['Dev'],temp=smbdict[smbdata['Dev']]['temp'],str1=smbdict[smbdata['Dev']]['str1'],vol1=smbdict[smbdata['Dev']]['vol1'],
                str2=smbdict[smbdata['Dev']]['str2'],vol2=smbdict[smbdata['Dev']]['vol2'],str3=smbdict[smbdata['Dev']]['str3'],vol3=smbdict[smbdata['Dev']]['vol3'],str4=smbdict[smbdata['Dev']]['str4'],vol4=smbdict[smbdata['Dev']]['vol4'],
                str5=smbdict[smbdata['Dev']]['str5'],vol5=smbdict[smbdata['Dev']]['vol5'],str6=smbdict[smbdata['Dev']]['str6'],vol6=smbdict[smbdata['Dev']]['vol6'],str7=smbdict[smbdata['Dev']]['str7'],vol7=smbdict[smbdata['Dev']]['vol7'],
                str8=smbdict[smbdata['Dev']]['str8'],vol8=smbdict[smbdata['Dev']]['vol8'],str9=smbdict[smbdata['Dev']]['str9'],vol9=smbdict[smbdata['Dev']]['vol9'],str10=smbdict[smbdata['Dev']]['str10'],vol10=smbdict[smbdata['Dev']]['vol10'],
                str11=smbdict[smbdata['Dev']]['str11'],vol11=smbdict[smbdata['Dev']]['vol11'],str12=smbdict[smbdata['Dev']]['str12'],vol12=smbdict[smbdata['Dev']]['vol12'],str13=smbdict[smbdata['Dev']]['str13'],vol13=smbdict[smbdata['Dev']]['vol13'],
                stravg=smbdict[smbdata['Dev']]['stravg'],volavg=smbdict[smbdata['Dev']]['volavg'],poweravg=smbdict[smbdata['Dev']]['poweravg'])
        db.session.add(smbtotal)
        db.session.commit()
        smbdict[smbdata['Dev']].clear()
        print("SMBdata saved to database")

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_connect = on_connect
client.on_message = on_message
time.sleep(1)

subtop="tracker/device/sub"
pubtop="tracker/device/pub"
#client.username_pw_set("cbocdpsu", "3_UFu7oaad-8")
client.connect('ec2-35-162-194-10.us-west-2.compute.amazonaws.com')
client.loop_start()
client.subscribe(subtop)
client.loop()



@server.route('/')
def plantview():
    return render_template("plantview.html")

@server.route('/tracker',methods=['GET'])
def tracker():
    post=User.query.all()
    return render_template("tracker.html", post=post)

@server.route('/smbs',methods=['GET'])
def smbs():
    data1=smb.query.all()
    return render_template("smbs.html", data1=data1)




if __name__ == '__main__':
    server.run(port=8000)


