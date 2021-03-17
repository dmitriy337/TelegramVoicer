# -*- coding: utf-8 -*-
from telethon import *
from gtts import gTTS
import random, time
import pyttsx3, os
import sqlite3


api_id = <YourId>
api_hash = "<YourHash>"


client = TelegramClient('anon', api_id, api_hash)
client.start()

#SqlLite init
conn = sqlite3.connect('DataBase.db')
curs = conn.cursor()
def InitDB():
    curs.execute("""CREATE TABLE AddChatToDB (
        ChatId STRING UNIQUE
                  NOT NULL,
        bld    INT
        );""")
    conn.commit()



def CheckInDb(ChatId):
        curs.execute(f"SELECT ChatId FROM AddChatToDB WHERE ChatId='{ChatId}'")
        if curs.fetchall() == []:
            return False
        else:
            return True

def AddNewInDb(ChatId):
        curs.execute(f'INSERT INTO AddChatToDB (ChatId, bld) VALUES({ChatId}, 1);')
        conn.commit()

def UpdateBldInDb(ChatId):
    curs.execute(f"SELECT * FROM AddChatToDB WHERE ChatId='{ChatId}'")
    #print(curs.fetchall()[0][1])

    if str(curs.fetchall()[0][1]) == '1':
        curs.execute(f"Update AddChatToDB set bld = 0 WHERE ChatId='{ChatId}' ")
        conn.commit()
    else: 
        curs.execute(f"Update AddChatToDB set bld = 1 WHERE ChatId='{ChatId}' ")
        conn.commit()




#Defs
def AddChatToDB(ChatId):
    try:
        if CheckInDb(ChatId):
            UpdateBldInDb(ChatId)
            #print('Есть')
        else:
            AddNewInDb(ChatId)
            #print('Нема')

    except Exception as e:
        print(e)

def CheckStatusCodeInDB(ChatId):
    curs.execute(f"SELECT * FROM AddChatToDB WHERE ChatId='{ChatId}'")
    if str(curs.fetchall()[0][1]) == '1':
        return True
    else:
        return False

def CheckOnOrOfInDB(ChatId):
    if CheckInDb(ChatId):
        if CheckStatusCodeInDB(ChatId):
            return True
        else:
            return False
    else:
        return False

@client.on(events.NewMessage(pattern='(^!SV)|(^!sv)', outgoing=True))
async def handler(event):
    try:  
        AddChatToDB(event.message.chat_id)
        await event.delete()
        await client.send_message(event.message.chat_id, 'Status was updated!!!')
    except Exception as e:
        print(e)

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    try:
        if CheckOnOrOfInDB(event.message.chat_id):
            if str(event.message.message) == '':
                return 1
            if str(event.message.message) == '!sv':
                return 0
            if str(event.message.message) == '!SV':
                return 0

            tetx = event.message.message
            await event.delete()
            tts = gTTS(text=(tetx), lang='ru', slow=False)
            tts.save('sd.mp3')
            await client.send_file(event.message.chat_id, 'sd.mp3', reply_to=event.reply_to_msg_id ,attributes=[types.DocumentAttributeAudio(duration=random.randint(3, 60), voice=True, waveform=utils.encode_waveform(bytes(((random.randint(3, 60), random.randint(3, 60), random.randint(1, 20), random.randint(1, 20), random.randint(1, 20),random.randint(1, 20), 31, 31)) * random.randint(1, 10))))])
            try:
                os.remove('sd.mp3')
            except:
                pass
        else:
            pass
    except Exception as e:
        print(e)




try:
    InitDB()
except:
    pass
if __name__ == '__main__':
    while True:
        try:
            print('(Press Ctrl+C to stop this)')
            client.run_until_disconnected()
        finally:
            client.disconnect()
