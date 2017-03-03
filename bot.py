# coding: utf-8

from wxpy import *
import mafia

robot = Robot()

print('消息列表：' + robot.chats())
print('群：' + robot.friends())

group = robot.groups().search('狼人')[0]
game = {
    'create' : '新游戏',
    'join' : '加入',
    'quit' : '退出',
    'start' : '开始游戏'
}

@robot.register()
def printData(data):
    print(data)

@robot.register(group)
def mafia(data):
    msg = data.text
    if(msg == game['create']):
        return '创建游戏'

@robot.register()
def reply(data):
    return '收到：{} ({})'.format(data.text, data.type)


    

robot.start()