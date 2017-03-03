from wxpy import *

robot = Robot()

@robot.register()
def printMsg(msg):
    print(msg)

@robot.register(my_friend)
def reply(msg):
    return 'received: {} ({})' .format(msg.text, msg.type)

robot.start()