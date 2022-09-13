sequenceMessages = []
messagesSent = []

import telegram
telegramToken = 'YOUR telegram token'
teleBot = telegram.Bot(telegramToken)


def SendRedMessage(self, table, tablesOnAlert):
    print(f'Deu \033[31mRED\033[m em {table}')
    SendMessageTelegram(f'''❌Red❌
por[{tablesOnAlert[table][2]}]
{table}
{tablesOnAlert[table][0][:len(tablesOnAlert[table][0])- 8]}''')


def SendAttentionMessage(self, table, x, reason):
    SaveMessageToList(f'''⏰ATENÇAO⏰
Sequencia de {x+1} numeros
{reason}
Em
{table}''')


def SendBetMessage(self, table, reason):
    SaveMessageToList(f'''⚠️ATENÇAO⚠️
Apostar em numeros
{reason}
em
{table}''')


def SendGreenMessage(table, numberList, reason, tablesOnAlert):
    print(f'Deu \033[32mGREEN\033[m em {table}')
    SendMessageTelegram(f'''✅GREEN✅
{table}
por [{reason}]
{numberList[:len(numberList)- 8]}''')
    tablesOnAlert.pop(table)


def SendMessageTelegram(message, telegramGroup):
    try:
        teleBot.send_message(
            chat_id=telegramGroup, text=message)

    except:
        print('Telebot was accused of Spamming')
        pass


def SaveMessageToList(self, message):
    if message not in sequenceMessages:
        sequenceMessages.append(message)

    if message not in messagesSent:
        messagesSent.append(message)
        SendMessageTelegram(message)


def RemoveMessageFromList(self):
    for message in messagesSent:
        if message not in sequenceMessages:
            messagesSent.remove(message)
