# coding: utf-8

from wxpy import *
import sqlite3
import random
import time
import asyncio

conn = sqlite3.connect('mafia.db')
conn.close()
robot = Robot('wx.cookie')

groupName = '天黑请闭眼'
game = {
    'create' : '新游戏',
    'join' : '加入',
    'quit' : '退出',
    'start' : '开始游戏',
    'end' : '结束游戏',
    'choose' : '票' 
}

@robot.register()
def mafia(data):
    msg = data.text
    msgFrom = str(data.chat)
    name = str(data.member)[9:-1]
    # 群消息处理
    if(msgFrom.find(groupName) != -1):  
        if(msg == game['create']):
            return newGame()
        if(msg == game['end']):
            return endGame()
        if(msg == game['join']):
            userid = data.raw['acturename']
            return joinGame(name, userid)
        if(msg == game['quit']):
            return quitGame(name)
        if(msg == game['start']):
            return startGame()
        
    # 私聊消息处理
    if gaming():
        players = getSpecialAll()
        for player in players:
            if(msgFrom.find(player) != -1):
                if(msg == game['choose']):
                    
                

    

def iinit():
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('create table if not exists user (id int primary key, name varchar(20))')
        db.close()
        conn.commit()
        conn.close()
        print('读取用户配置，如不存在则自动创建...')
    except:
        print('数据库连接失败')
def newGame():
    if not gaming():
        if not waiting():
            try:
                conn = sqlite3.connect('mafia.db')
                print('有人发起了新游戏')
                db = conn.cursor()
                db.execute('create table player (id int, user_id varchar(50), name text primary key, type int, status int, choose int, vote int, votable int)')
                db.close()
                conn.commit()
                conn.close() 
                return '游戏创建成功，正在等待玩家加入...\n发送"加入"即可加入游戏。'
            except:
                return '未知错误，请联系管理员。'
        else:
            return '当前有正在进行中的游戏，请结束游戏后在开新局。'
    else:
        return '当前有正在进行中的游戏，请结束游戏后在开新局。'
def joinGame(name, userid):
    if not gaming():
        if waiting():
            print('有人想加入游戏，游戏人数：'+ getWait())
            try:
                print('有人想加入游戏，游戏人数：'+ getWait())
                conn = sqlite3.connect('mafia.db')
                db = conn.cursor()
                db.execute('insert into player (id, user_id, name, votable) values (?, ?, ?, 0)',(getId(), userid, name,))
                db.close()
                conn.commit()
                conn.close() 
                return name + ' 加入了游戏。\n' + getWait()
            except:
                return '你已经加入游戏了。'
        else:
            return '操作失败，没有等待中的游戏。'
    else:
        return '操作失败，没有游戏。'
def quitGame(name):
    if not gaming():
        if waiting():
            try:
                print('有人退出游戏')
                conn = sqlite3.connect('mafia.db')
                db = conn.cursor()
                db.execute('select * from player where name = ?', (name,))
                if not db.fetchall():
                    db.close()
                    conn.commit()
                    conn.close() 
                    print('退出的玩家不在游戏中')
                    return '退出游戏失败，你不在游戏中。'
                else:
                    db.execute('delete from player where name = ?',(name,))
                    db.close()
                    conn.commit()
                    conn.close() 
                    return name + ' 退出了游戏。\n' + getWait(1)
            except:
                return '未知错误，请联系管理员。'
        else:
            return '操作失败，没有等待中的游戏。'
    else:
        return '操作失败，游戏已经开始了。'
def endGame():
    if not gaming():
        try:
            conn = sqlite3.connect('mafia.db')
            db = conn.cursor()
            db.execute('drop table player')
            db.close()
            conn.commit()
            conn.close()
            return '游戏结束成功，现在可以发起新的游戏。'
        except:
            return '未知错误。'
    else:
        return '操作失败，游戏未开始。'
def startGame():
    if not gaming():
        if waiting():
            player = getWait()
            killer = getKiller(player)
            actor = []
            n = 0
            while n < killer:
                n = n+1
                actor.append(1)
                actor.append(2)
            m = 0
            pm = player-killer*2
            while m < pm
                m = m+1
                actor.append(0)
            random.shuffle(actor)
            # 分配角色
            try:
                conn = sqlite3.connect('mafia.db')
                db = conn.cursor()
                num = player
                # 创建游戏进程
                db.execute('create table game (days int, time int, voting int)')
                db.execute('insert into game (days) values (1)')
                for actType in actor:
                    db.execute('update player set type=?,status=? where id=?', (actType, 1,num,))
                    # 发送身份
                    sendActById(num, act)
                    num = num-1
                db.close()
                conn.commit()
                conn.close()
                sendGroup(groupName, '游戏即将在10秒内开始，已将各位的身份私聊发送出去，请确认好自己的身份。')
                time.sleep(10)
                gaming = True
                sendGroup(groupName, '天黑了，所有人请闭眼。\n杀手出来杀人，私聊法官票选目标。')
            return '天黑了，所有人请闭眼。\n杀手出来杀人，私聊法官票选目标。'
            except:
                return '未知错误，请联系管理员'
        else:
            return '操作失败，没有等待中的游戏。'
    else:
         return '操作失败，没有游戏。'

# 获取游戏数据        
def getId():
    try:
        print('尝试获取玩家数...')
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select max(id) from player')
        print('数据库操作成功')
        value = db.fetchall()
        db.close()
        conn.close()
        Id = value[0][0]
        if not Id:
            print('没有玩家')
            Id = 0
        print('已有玩家：'+ str(Id))
        return '2'
    except:
        return '1'
def gaming():
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select * from game')
        value = db.fetchall()
        db.close()
        conn.close()
        return True
    except:
        return False
def waiting():   
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select * from player')
        value = db.fetchall()
        db.close()
        conn.close()
        return True
    except:
        return False
def getWait(plus=0):
    num = int(getId())-1
    if(num < 7):
        return '还需要 ' + str(7-num+plus) + ' 人即可开始游戏。'
    else:
        return '人数已达到要求。\n你可以继续等待或发送“开始游戏”来开始。'
def getKiller(num=8):
    last = num%4
    killer = (num-last)/4
    return killer
def getPlayerAll():
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select name from player')
        plist = db.fetchall()
        db.close()
        conn.close()
        return plist
    except:
        return [0]
def getSpecialAll():
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select name from player where type != 0')
        plist = db.fetchall()
        db.close()
        conn.close()
        return plist
    except:
        return [0]

def getNameById(userid):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select name from player where id = ?',(userid,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家名称失败。'
def getIdbyName(name):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select id from player where name = ?',(name,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家id失败。'
def getChoiceById(userid):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select choose from player where id = ?',(userid,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家投票目标失败。'
def getChoiceByName(name):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select choose from player where name = ?',(name,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家投票目标失败。'
def getVoteById(userid):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select vote from player where id = ?',(userid,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家票数失败。'
def getVoteByName(name):
     try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select vote from player where name = ?',(name,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家票数失败。'
def getTypeById(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select type from player where id = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家身份失败。'
def getTypeByName(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select type from player where name = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家身份失败。'
def getStatusById(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select status from player where id = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家生存状态失败。'
def getStatusByName(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select status from player where name = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家生存状态失败。'
def getUserIdById(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select user_id from player where id = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家user_id失败。'
def getUserIdByName(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select user_id from player where id = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取玩家user_id失败。'
def getVotableById(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select votable from player where id = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        if (res == 0):
            return False
        else:
            return True
    except:
        return False
def getVotableByName(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select user_id from player where name = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        if (res == 0):
            return False
        else:
            return True
    except:
        return False
def getGameDays(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select days from game',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取游戏天数失败。'
def getGameTime():
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select time from game',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return res
    except:
        return '获取白天黑夜失败。'
# 游戏过程
def setVotableById(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('update player set votable = 1 where id = ?',(ref,))
        db.close()
        conn.commit()
        conn.close()
        return True
    except:
        return False
def setVotableByName(ref):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('update player set votable = 1 where name = ?',(ref,))
        db.close()
        conn.commit()
        conn.close()
        return True
    except:
        return False
def nextDay():
     try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('select user_id from player where id = ?',(ref,))
        res = db.fetchall()
        res = res[0][0]
        db.close()
        conn.commit()
        conn.close()
        return '第二天到了。'
    except:
        return '错误，进入下一天失败。'
# 消息处理
def sendActById(num, act):
    actor = ''
    if (act == 0):
        actor = '平民'
    if  (act == 1):
        actor = ''
    conn = sqlite3.connect('mafia.db')
    db = conn.cursor()
    db.execute('select * from player where id = ?', (num,))
    name = db.fetchall()[0]['name']
    db.close()
    conn.close()
    friend = robot.friends().search(name)[0]
    friend.send('你的身份是： ' + actor)
def sendGroup(group, text):
    group = robot.groups().search(group)[0]
    group.send(text)
def vote(name, who):
    vote = 'choose=' + str(who)
    where = 'where name =' + name
    setValue(vote, where, 'player')
    return '你投票了 '+str(who)+' 号：'
def setValue(exe, where, table):
    try:
        conn = sqlite3.connect('mafia.db')
        db = conn.cursor()
        db.execute('update ? set ? where ?',(table, exe, where,))
        db.close()
        conn.commit()
        conn.close()
        return '修改字段值成功'
    except:
        return '获取字段值失败。'
robot.start()
