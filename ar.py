import amino
from amino import Client

print('Рейд клан AZATHOTH, скрипт от Пандоры и Души, антирейд бот :D');

mail=input('[AZATHOTH] логин(почта): ')
password=input('[AZATHOTH] пароль: ')
communityId = Client().get_from_code(str(input("[AZATHOTH] ссылка на сообщество: ")))
ndcId  = communityId.json["extensions"]["community"]["ndcId"];
CLIENT=amino.Client()
CLIENT.login(email=mail,password=password)
SUBCLIENT=amino.SubClient(comId=str(ndcId), profile=CLIENT)

chats = input("Войти во все чаты в сообществе? (Да/нет, не зависит от регистра): ").lower()
if chats == "да":
    print('\n[AZATHOTH] чаты в сообществе: ')
    x=0
    CLIENT_CHAT_IDS_MENU=[]
    chats = SUBCLIENT.get_public_chat_threads(size=200)
    for name, id in zip (chats.title, chats.chatId):
        if name!=None:
            print(x+1,":", name)
            CLIENT_CHAT_IDS_MENU.append(str(id))
            x+=1

    for j in CLIENT_CHAT_IDS_MENU:
        SUBCLIENT.join_chat(j)
        print(f"[AZATHOTH] {j}: бот присоединился к чату")
elif chats == "нет": print('Ok')
else: print('Сочту это за нет')

print()
print('[AZATHOTH] Антирейд запущен')

@CLIENT.event("on_message")
def on_message(data):

    chatid = data.message.chatId
    nickname = data.message.author.nickname
    content = data.message.content
    mtype = data.message.type
    chatname = SUBCLIENT.get_chat_thread(chatId=data.message.chatId).title
    messageid = data.message.messageId
    userid = data.message.author.userId
    global nazvanie
    global opisanie
    global fon
    
    print(f'{chatname}: {chatid}: {nickname}: {mtype}: {content}')

    if mtype in range(50,111):
        if  content == None:
            pass
        else:
            SUBCLIENT.kick(chatId=chatid, userId = userid, allowRejoin=False)
            SUBCLIENT.delete_message(chatId = chatid, messageId = messageid, asStaff = True, reason = 'Отправка системных сообщений')
            SUBCLIENT.strike(userId = userid, time = 1, reason = 'Отправка системных сообщений')
            SUBCLIENT.send_message(chatId = chatid, message = f'{nickname} отправил сообщение {mtype} типа! Режим чтения выдан.')

methods = []
for x in CLIENT.chat_methods:
    methods.append(CLIENT.event(CLIENT.chat_methods[x].__name__)(on_message))
