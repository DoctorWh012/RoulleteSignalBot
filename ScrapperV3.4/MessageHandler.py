import telegram
import main
from colorama import Fore

# Telegram setup
telegramToken = 'YOUR TELEGRAM TOKEN'
teleBot = telegram.Bot(telegramToken)

# Telegram Functions


def SendMessageTelegram(message, telegramGroup):
    try:
        teleBot.send_message(
            chat_id=telegramGroup, text=message)

    except:
        print('Telebot was accused of Spamming')
        pass


def SendGreenMessage(table, numberList, reason, alertList, telegramGroup):
    print(Fore.GREEN + f'Deu GREEN em {table}')

    SendMessageTelegram(f'''✅GREEN✅
{table}
por [{reason}]
{numberList[:len(numberList)- 8]}''', telegramGroup)
    del alertList[table]


def SendRedMessage(table, alertList, telegramGroup):
    print(Fore.RED + f'Deu RED em {table}')

    SendMessageTelegram(f'''❌Red❌
por[{alertList[table][2]}]
{table}
{alertList[table][0][:len(alertList[table][0])- 8]}''', telegramGroup)


def SendAttentionMessage(table, x, reason, telegramGroup):
    pass
#     SaveMessageToList(f'''⏰ATENÇAO⏰
# Sequencia de {x+1} numeros
# {reason}
# Em
# {table}''', telegramGroup)


def SendBetMessage(table, reason, telegramGroup):
    SaveMessageToList(f'''⚠️ATENÇAO⚠️
Apostar em numeros
{reason}
em
{table}''', telegramGroup)

# List managing functions


def SaveMessageToList(message, telegramGroup):
    if message not in main.sequenceMessages:
        main.sequenceMessages.append(message)

    if message not in main.messagesSent:
        main.messagesSent.append(message)
        SendMessageTelegram(message, telegramGroup)


def RemoveMessageFromList():
    for message in main.messagesSent:
        if message not in main.sequenceMessages:
            main.messagesSent.remove(message)


def SendStartMessage(message):
    SendMessageTelegram(message, main.colorGroup)
    SendMessageTelegram(message, main.evenOddGroup)
    SendMessageTelegram(message, main.hiLoGroup)
    SendMessageTelegram(message, main.rowGroup)
    SendMessageTelegram(message, main.dozenGroup)
