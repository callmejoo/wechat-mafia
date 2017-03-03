# coding: utf-8

from wxpy import *
import sqlite3
conn = sqlite3.connect('mafia.db')
conn.close()
robot = Robot('wx.cookie')

game = {
    'create' : '新游戏',
    'join' : '加入',
    'quit' : '退出',
    'start' : '开始游戏',
    'end' : '结束游戏'
}

@robot.register()
def mafia(data):
    msg = data.text
    msgFrom = str(data.chat)
    name = str(data.member)[9:-1]
    if(msgFrom.find('狼人') != -1):  
        if(msg == game['create']):
            return newGame()
        if(msg == game['end']):
            return endGame()
        if(msg == game['join']):
            return joinGame(name)
        if(msg == game['quit']):
            return quitGame(name)
        if(msg == game['start']):
            
            

def iinit():
    try:
        db = conn.cursor()
        db.execute('create table if not exists user (id int primary key, name varchar(20))')
        db.close()
        conn.commit()
        conn.close()
        print('读取用户配置，如不存在则自动创建...')
    except:
        print('数据库连接失败')
def newGame():
    try:
        conn = sqlite3.connect('mafia.db')
        print('有人发起了新游戏')
        db = conn.cursor()
        db.execute('create table player (id int, name text primary key, type int, status int, choose int, vote int)')
        db.close()
        conn.commit()
        conn.close() 
        return '游戏创建成功，正在等待玩家加入...\n发送"加入"即可加入游戏。'
    except:
        return '当前有正在进行中的游戏，请结束游戏后在开新局。'
def joinGame(name):
    if not gaming():
        if waiting():
            print('有人想加入游戏，游戏人数：'+ getWait())
            try:
                print('有人想加入游戏，游戏人数：'+ getWait())
                conn = sqlite3.connect('mafia.db')
                db = conn.cursor()
                db.execute('insert into player (id, name) values (?, ?)',(getId(), name,))
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
            num = int(getId())-1
            
        else:
            return '操作失败，没有等待中的游戏。'
    else:
         return '操作失败，没有游戏。'
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


robot.start()
