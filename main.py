import re
import vk_api
import requests 
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType


def is_valid_youtube_url(url):
    regex = (
        r'^(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    match = bool(re.match(regex, url))


def send_audio_message(url):
    response = requests.get(url)
    if response.status_code == 200:
        response.content
        # Вот сюдашки в апишку суешь вместо строчки выше
        

def write_message(sender, message, attachments=None):
    if attachments is not None:
        auth.method("messages.send", {"user_id": sender, "message": message, "random_id": get_random_id(), "attachment": ','.join(attachments)})
    else:
        auth.method("messages.send", {"user_id": sender, "message": message, 'random_id': get_random_id()})


TOKEN = "vk1.a.1OgMrmJ94L0cyLEOfzqz75193hU4Z6Dyg_14N6fnYxh5LahZma9KGjPnrwRsN0DuVgA9QwZ_sTMJJh02DX8SyivY6sE1CbWfg7WSZ5X05hJMWIZGerBi-IiJsWmjkxkKuy68Rb9BzohJcRT0j4D8sqg-PDmsmX-6iPdAui4zohZKOJiudDzzEYVgIUlbAmuQgJZ2pY97QqMceik75ynkEA"
auth = vk_api.VkApi(token=TOKEN)
vk = auth.get_api()
longpoll = VkLongPoll(auth)
upload = VkUpload(auth)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        received_message = event.text
        sender = event.user_id
        attachments = []
        
        if received_message == "Начать":
            image = "images/Persik.png"
            upload_image = upload.photo_messages(photos=image)[0]
            attachments.append('photo{}_{}'.format(upload_image["owner_id"], upload_image["id"]))
            write_message(sender=sender, message='Привет. Я бот VK Audio Clean. С моей помощью ты сможешь улучшить запись своего голоса, удалив слова-паразиты, паузы и внешние шумы. Let\'s try!', attachments=attachments)
        
        if is_valid_youtube_url(received_message) is True:
            write_message(sender=sender, message="Прости, я пока не умею работать с видео из Youtube, но скоро обязательно научусь!!!")


    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = vk.messages.getById(message_ids=event.message_id)['items'][0]
        print(message)  # Печатаем все сообщение для отладки
        if 'attachments' in message and message['attachments']:
            for attachment in message['attachments']:
                if attachment['type'] == 'audio_message':
                    audio_message = attachment['audio_message']
                    audio_url = audio_message['link_mp3']
                    send_audio_message(audio_url)
