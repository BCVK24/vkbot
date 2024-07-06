import re
import vk_api
import requests 
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType


api_source_url = 'http://127.0.0.1:8080/'


def get_auth_token(vk_id):
    return requests.post(f'{api_source_url}user/auth/token').json()['access_token']


def is_valid_youtube_url(url):
    regex = (
        r'^(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    match = bool(re.match(regex, url))


def send_audio_message(url):
    response = requests.get(url)
    if response.status_code == 200:
        resp = request.post(f'{api_source_url}recording', files={
            'recording_file': response
        }, json={
        'recording': "chat_bot_recording"
        }, headers={
        'Authorization': 'Bearer 123'
        })


def get_recordnig_info(recording_id):
    requests.get(f'{api_source_url}recording/{recording_id}', headers={
        'Authorization': 'Bearer 123'
        })
        

def write_message(sender, message, attachments=None):
    if attachments is not None:
        auth.method("messages.send", {"user_id": sender, "message": message, "random_id": get_random_id(), "attachment": ','.join(attachments)})
    else:
        auth.method("messages.send", {"user_id": sender, "message": message, 'random_id': get_random_id()})


TOKEN = "ZVVFROvWHfT915K6LeJo1tG4ZycjvqSa3OhVrGpG2v7xry3JuEsbrZslYQm2oihIe4XxcWy3NDX4kjjjBbydBJNEVwxwtaIIxMd1qMlF68ikB1oPAczdoEDZS1ZssiQ2wfliin0V_0XCS_NeoHOHAma6YmTFIY_LGX6C3qGvgU_Qr-CMji11dc6XrKrUPZ7xpspHXA"
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
            write_message(sender=sender, message='Привет. Я бот VK CleanCast. С моей помощью ты сможешь улучшить запись своего голоса, удалив слова-паразиты, паузы и внешние шумы. Let\'s try!', attachments=attachments)
        
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
