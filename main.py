import re
import os
import vk_api
import asyncio
import requests
from dotenv import find_dotenv, load_dotenv
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

load_dotenv(find_dotenv())

api_source_url = 'http://127.0.0.1:8080/'


def get_auth_token(vk_id):
    return requests.post(f'{api_source_url}user/auth/token').json()['access_token']


def is_valid_youtube_url(url):
    regex = (
        r'^(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    match = bool(re.match(regex, url))


async def send_audio_message(url):
    response = requests.get(url) # Audio
    if response.status_code == 200:
        resp = requests.post(f'{api_source_url}recording', files={
            'recording_file': response.content
        }, json={
        'recording': "chat_bot_recording"
        }, headers={
        'Authorization': 'Bearer 123'
        })  # RETURN STRUCTURE FILE

        if resp.status_code == 200:
            return resp.content


async def get_recordnig_info(recording_id):
    resp = requests.get(f'{api_source_url}recording/{recording_id}', headers={
        'Authorization': 'Bearer 123'
        }) # RETURN FILE INFO
    if resp.status_code == 200:
        return resp.content


async def get_recording_bytes(recording_id):
    resp = requests.get(f'{api_source_url}recording/download/{recording_id}', headers={
        'Authorization': 'Bearer 123'
        }) # RETURN FILE BYTES
    if resp.status_code == 200:
        return resp.content


def get_result_bytes(result_id):
    resp = requests.get(f'{api_source_url}result/download/{result_id}')
    if resp.status_code == 200:
        return resp.content


def write_message(sender, message, attachments=None):
    if attachments is not None:
        auth.method("messages.send", {"user_id": sender, "message": message, "random_id": get_random_id(), "attachment": ','.join(attachments)})
    else:
        auth.method("messages.send", {"user_id": sender, "message": message, 'random_id': get_random_id()})


def get_admin_groups(user_id):
    try:
        response = vk.groups.get(user_id=user_id, extended=1, filter='admin')
        print("groups: ", response)
        groups = response['items']
        for group in groups:
            print(f"{group['id']} {group['name']}")
        return groups
    except vk_api.exceptions.ApiError as e:
        print(e)
        return None





auth = vk_api.VkApi(token=os.getenv("TOKEN"))
vk = auth.get_api()
longpoll =  VkLongPoll(auth)
upload = VkUpload(auth)

async def zxc():
    while True:
        print(os.listdir('jsons')) #TODO сделать поиск
        await asyncio.sleep(10)

# asyncio.run(zxc())


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        received_message = event.text
        sender = event.user_id
        attachments = []

        if received_message.lower() == "пост":
            admin_groups = get_admin_groups('706435489')
            if admin_groups:
                print('zxc: ', admin_groups)

        if received_message == " ":
            image = "images/Persik.png"
            upload_image = upload.photo_messages(photos=image)[0]
            attachments.append('photo{}_{}'.format(upload_image["owner_id"], upload_image["id"]))
            write_message(sender=sender, message='Привет. Я бот VK CleanCast. С моей помощью ты сможешь улучшить запись своего голоса, удалив слова-паразиты, паузы и внешние шумы. Let\'s try!', attachments=attachments)
        
        if is_valid_youtube_url(received_message) is True:
            write_message(sender=sender, message="Прости, я пока не умею работать с видео из Youtube, но скоро обязательно научусь!!!")


    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = vk.messages.getById(message_ids=event.message_id)['items'][0]
        if 'attachments' in message and message['attachments']:
            for attachment in message['attachments']:
                if attachment['type'] == 'audio_message':
                    audio_message = attachment['audio_message']
                    audio_url = audio_message['link_mp3']
                    asyncio.run(send_audio_message(audio_url))
