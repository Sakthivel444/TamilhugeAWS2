from pyrogram import Client
from os.path import exists
from os import remove
from sys import stdout, exit
import array as arr
import os
from pyrogram.errors import FloodWait
import time
from thumbnail import generate_thumbnail


import cv2

configfile = "tgd.txt"

if not exists(configfile):
    api_id = input("\nAPI ID: ")
    api_hash = input("API HASH: ") 
    check = input("Do you have String Session? (y/n): ")
    if check.lower() == "y":
        ss = input("SESSION STRING: ")
    else:
        print()
        with Client("TGD", api_id=api_id, api_hash=api_hash, in_memory=True) as temp:
            ss = temp.export_session_string()
        print()
    with open(configfile,"w") as file:
        file.write(api_id + "\n" + api_hash + "\n" + ss)
else:
    with open(configfile, "r") as file:
        data = file.readlines()
    try:
        api_id, api_hash, ss = data
    except:
        remove(configfile)
        print("Retry...")
        exit(0)
        

acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
try:
    with acc:
        me = acc.get_me()
        print("\nLogged in as:", me.id)
except:
    remove(configfile)
    print("\nMaybe Wrong Crenditals...")
    exit(0)
    
    
def progress(current, total, length=50):
    progress_percent = current * 100 / total
    completed = int(length * current / total)
    bar = f"[{'#' * completed}{' ' * (length - completed)}] {progress_percent:.1f}%"
    stdout.write(f"\r{bar}")
    stdout.flush()


print("""
Examples:

    https://t.me/xxxx/1423
    https://t.me/c/xxxx/10
    https://t.me/xxxx/1001-1010
    https://t.me/c/xxxx/101 - 120\n\n""")

#link = input("Enter the link: ")
#https://t.me/c/2131480022/2135
link = "https://t.me/c/2056802156/7000-20000"


print()


if link.startswith("https://t.me/"):
    datas = link.split("/")
    temp = datas[-1].replace("?single","").split("-")
    fromID = int(temp[0].strip())
    try: toID = int(temp[1].strip())
    except: toID = fromID

    if link.startswith("https://t.me/c/"):
        chatid = int("-100" + datas[4])
    else:
        chatid = datas[3]

else:
    print("Not a Telegram Link")
    exit(0)


#custo = arr.array('i', [1736,1737,1738,1744,1745,1746,1747,1748,1749,1750,1751,1752,1753,1754,1756,1757,1758,1759,1762,1763,1764,1765,1766,1767,1768,1769,1770,1771,1772,1773])


with acc:
    total = toID+1 - fromID
    for msgid in range(fromID, toID+1):
    #for element in custo:
        #msgid=element
        msg = acc.get_messages(chatid, msgid)
        
        print("Downloding:", msgid, f"({(msgid - fromID + 1)}/{total})")
        try:
            file = acc.download_media(msg, progress=progress)
            print("\nSaved at", file, "\n")
            
            #locas = "C:\Users\SAKTHIVEL\Downloads\photo_2024-02-14_12-16-35.jpg"
            
            vid = cv2.VideoCapture( r"{}".format(file))
            suc,vids = vid.read() 
            cv2.imwrite(r"downloads/1.jpeg", vids) 
            height:int = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)) # always 0 in Linux python3
            width:int  = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))  # always 0 in Linux python3
            framecount:int =int( vid.get(cv2.CAP_PROP_FRAME_COUNT ) )
            frames_per_sec:int =int( vid.get(cv2.CAP_PROP_FPS))
            duration:int = int( framecount / frames_per_sec)
            #print("{} {} {}".format( width , height,  duration))
            vid.release()
            time.sleep(1)
            print("+++++++++"+ file)
            if file.endswith(".jpg"):  
                print("uploading")                   
                acc.send_photo(-1002100096551,r"{}".format(file),progress=progress)
                acc.send_photo("tamilhuge",r"{}".format(file),progress=progress)
                os.remove(r"{}".format(file)) 
            
            #elif file in (FileType.VIDEO, FileType.ANIMATION, FileType.VIDEO_NOTE):
            elif file.endswith((".mp4")):    
                 print("uploading")
                 acc.send_video(-1002100096551,r"{}".format(file),progress=progress,supports_streaming = True,width=width,height=height,duration=duration,thumb=r"downloads/1.jpeg")
                 acc.send_video("tamilhuge",r"{}".format(file),progress=progress,supports_streaming = True,width=width,height=height,duration=duration,thumb=r"downloads/1.jpeg")
                 time.sleep(1)
                 os.remove(r"{}".format(file))    
                 os.remove(r"downloads/1.jpeg") 
            else:
                print("nope")           
    
        except ValueError as e:
            print(e, "\n")
        
            
            
            
input("Press enter to exit...")