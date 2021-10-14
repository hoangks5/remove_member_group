from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import pandas
import time
import datetime

api_id = 8763319
api_hash = '28f53a40a4052cd950dab693a3a3c04c'
phone = '+84358259167'        
client = TelegramClient(phone, api_id, api_hash)
async def main():
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'Hello !!!!')
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter verification code: '))


chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('Danh Sách Group: ')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1
g_index = input("Chọn Group để quét danh sách thành viên: ")
target_group=groups[int(g_index)]

print('Đang quét...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print('Đang lưu thông tin vào file info.csv')
with open("info.csv","w",encoding='UTF-8') as f:#Enter your file name.
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['Username','ID', 'Access Hash','Tên','Group', 'Group id','Hoạt Động'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        if user.status:
            lastseen = user.status
        else:
            lastseen = ""
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id,lastseen])
import pandas
df = pandas.read_csv('info.csv')
print(df)
print('Đã quét thành công')
time.sleep(5)

##############################################################################################

users = []
with open(r"info.csv", encoding='UTF-8') as f:  # Enter your file name
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        user['lastseen'] = row[6]
        users.append(user)

time_kick = input('Xóa những người có hoạt động cách đây mấy ngày: ')
solg = 0
for usss in users:
    tgian = usss['lastseen']
    if tgian == "UserStatusRecently()":
        pass
    elif tgian == "UserStatusLastWeek()":
        pass
    elif tgian == "":
        pass
    elif tgian == "UserStatusLastMonth()":
        pass
    else:
        f = tgian.split('(')
        g = f[2].split(',')
        done = g[:5]
        tesst1 = usss['name'] + " online lần cuối vào "+done[3]+" giờ "+done[4]+" phút, ngày "+done[2]+" tháng "+done[1]+" năm "+done[0]
        tesst = done[0]+'/'+done[1]+'/'+done[2]+' '+done[3]+':'+done[4]
        dt = datetime.datetime.strptime(tesst,"%Y/ %m/ %d  %H: %M")
        dt1 = datetime.datetime.now()
        dt2 = dt1 - dt
        if dt2.days >= int(time_kick):
            print(tesst1)
            solg = solg+1
choi = input('\nBạn có muốn xóa '+str(solg)+' người này ra khỏi nhóm ?\n0. Có\n1. Không\nLựa chọn: ')
if choi == '1':
    pass
elif choi == '0':
    for usss in users:
        tgian = usss['lastseen']
        if tgian == "UserStatusRecently()":
            pass
        elif tgian == "UserStatusLastWeek()":
            pass
        elif tgian == "":
            pass
        elif tgian == "UserStatusLastMonth()":
            pass
        else:
            f = tgian.split('(')
            g = f[2].split(',')
            done = g[:5]
            tesst1 = usss['name'] + " online lần cuối vào "+done[3]+" giờ "+done[4]+" phút, ngày "+done[2]+" tháng "+done[1]+" năm "+done[0]
            tesst = done[0]+'/'+done[1]+'/'+done[2]+' '+done[3]+':'+done[4]
            dt = datetime.datetime.strptime(tesst,"%Y/ %m/ %d  %H: %M")
            dt1 = datetime.datetime.now()
            dt2 = dt1 - dt
            if dt2.days >= int(time_kick):
                try:
                    client.kick_participant(target_group, usss['id'])
                    print('Đã kick thành công '+usss['name'])
                except:
                    print('Không thể kick người này !!!')