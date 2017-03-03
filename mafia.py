import sqlite3

conn = sqlite3.connect('mafia.db')

def init():
    try:
        db = conn.cursor()
        db.execute('create table user (id int primary key, name varchar(20))')
        db.close()
        db.commit()
        conn.close()
        print('用户数据不存在，正在创建...')
    except:
        print('用户数据已存在，加载用户数据...')

def reg(name):
    try:
        db = conn.cursor()
        # db.execute('select * from user ')
        db.execute('insert into user (id, name) values (2, ?)',(name,))
        res = db.fetchall()
        db.close()
        conn.commit()
        print(res)
        db.close()
    except:
        print('用户数据不存在，正在创建...')

def newGame():
    try:
        db = conn.cursor()
        db.execute('creat table game (player_id int primary key, player )')
        res = db.fetchall()
        db.close()
        conn.commit()
        print(res)
        db.close() 

reg('mike')