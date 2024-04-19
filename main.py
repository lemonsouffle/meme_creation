import requests
import telebot

url="https://api.imgflip.com/get_memes"
username="..."
password="..."
data=requests.get(url).json()['data']['memes']

a = 0
top='example'
bottom='example'

token = '...'
bot=telebot.TeleBot(token)

def give_images():
  data=requests.get(url).json()['data']['memes']
  res = ''
  for number, i in enumerate(data, 1):
    res += f'{number}\t{i["name"]}\n'
  return res

@bot.message_handler(commands=['start'])
def startbot(message):
  print('Someone uses our bot')
  bot.send_message(message.chat.id,'Hello! Welcome to meme creation bot.')
  bot.send_message(message.chat.id, give_images())
  bot.send_message(message.chat.id, 'Send the number of the picture you want to see.')


@bot.message_handler(content_types=['text'])
def get_text(message):
  username="finalproject"
  password="final_project11"
  if message.text.isdigit():
    global a
    global top
    global bottom
    global data
    global url
    a = int(message.text)
    if 0 < a <= 100:
      a = a - 1
      url="https://api.imgflip.com/get_memes"
      data=requests.get(url).json()['data']['memes']
      bot.send_photo(message.chat.id, data[a]['url'])
      bot.send_message(message.chat.id, 'If you want to see another meme, send the number of the picture you want to see.')
      bot.send_message(message.chat.id, 'If everything is all right. Write a text for the meme. Example:')
      bot.send_message(message.chat.id, '`top text:\nbottom text:`', parse_mode='Markdown')
    else:
      bot.send_message(message.chat.id, 'Incorrect number. Try again.')
  if not message.text.isdigit():
    if message.text.startswith('top text:'):
      i = message.text.find('bottom text:')
      top=message.text[9:i].strip()
      bottom=message.text[i+12:].strip()
      url_caption='https://api.imgflip.com/caption_image'
      parameters={
        'template_id':data[a]['id'],
        'username':username,
        'password':password,
        'text0':top,
        'text1':bottom
      }
      answer=requests.request("POST", url_caption, params=parameters)
      bot.send_message(message.chat.id, 'Your meme is here:')
      bot.send_photo(message.chat.id, answer.json()['data']['url'])
      bot.send_message(message.chat.id, 'If you want to start again, send /start')

bot.polling()
