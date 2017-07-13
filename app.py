# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from re import search
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    ImageSendMessage, ImageSendMessage, VideoSendMessage, AudioSendMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

channel_access_token = str(os.environ.get('CHANNEL_ACCESS_TOKEN'))
channel_secret = str(os.environ.get('CHANNEL_SECRET'))
master_id = str(os.environ.get('MASTER_ID'))
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')#

"""
# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise
"""

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    daftar_jurus = {'naga kacang':'nagakacang.txt'}
    daftar_cmd = ['bye', 'help', 'info', 'jurus', 'tag', 'tags', 'ougi', 'panggil', 'profil']
    daftar_tag = ['gagal ambis']
    img_url = {'bye':
                   ['https://image.ibb.co/ibvkKa/akatsukileave.jpg','https://image.ibb.co/meYGQF/akatsukileave_prev.jpg'],
               'gagal ambis':
                   ['https://image.ibb.co/hH2Msv/gagal_ngambis.jpg','https://image.ibb.co/mkb35F/gagal_ngambis_prev.jpg'],
            
                }
    if text[0] == '#':
        cmd = search(r'\#(\w*)\s*(.*)', text)
        # bye
        if cmd.group() == '#bye':
            if isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
                image_message = ImageSendMessage(
                    original_content_url=img_url[cmd.group(1)][0],
                    preview_image_url=img_url[cmd.group(1)][1])
                text_message1 = TextMessage(text='"There are things you can only learn by accepting your weakness."')
                text_message2 = TextMessage(text='Selamat tinggal ^_^')
                line_bot_api.reply_message(event.reply_token, [image_message, text_message1, text_message2])
                try:
                    line_bot_api.leave_group(event.source.group_id)
                except:
                    line_bot_api.leave_room(event.source.room_id)   
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text="Mana bisa keluar dari personal chat qaqa ^-^"))
        # help
        elif cmd.group(1) == 'help':
            if cmd.group() == '#help':
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="""list perintah :"""+', '.join(daftar_cmd)+"""
                                                            Gunakan '#' di awal perintah
                                                            untuk lebih jelas ketik '#help <perintah>'
                                                            contoh: #help jurus"""))
            elif cmd.group(2) in daftar_cmd:
                f = open('helps/'+cmd.group(2)+'.txt', 'r')
                help_text = f.read()
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text="Bantuan untuk : '#"+cmd.group(2)+"'"), TextSendMessage(text=help_text)])
                f.close()
            else:
                line_bot_api.reply_message(
                    event.reply_token, [
                    TextSendMessage(text='Mana ada perintah itu'),
                    TextSendMessage(text='Berikut list perintah : '+', '.join(daftar_cmd))])
        # info
        elif cmd.group() == '#info':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Dibuat sebagai project pembelajaran oleh: Ikraduya Edian(line:ikraduya)'))
        # jurus
        elif cmd.group(1) == 'jurus':
            if cmd.group(2) in daftar_jurus:
                f = open('statics/' + daftar_jurus[cmd.group(2)], 'r')
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text=('JURUS '+cmd.group(2)).upper() + '!'),
                                        TextSendMessage(text=str(f.read()))])
                f.close()
            elif cmd.group(2) == '':
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text='Jurus apa qaqa??'))
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Mana ada jurus begitu.. untuk melihat list jurus ketik '#ougi'"))
        # tag
        elif cmd.group(1) == 'tag':
            if cmd.group(2) in daftar_tag:
                image_message = ImageSendMessage(
                    original_content_url=img_url[cmd.group(2)][0],
                    preview_image_url=img_url[cmd.group(2)][1])
                line_bot_api.reply_message(event.reply_token, image_message)
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Untuk melihat list tag ketik '#tags'"))
        # tags
        elif cmd.group() == '#tags':
            line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text='Berikut list tag : '+', '.join(daftar_tag)))
        # ougi
        elif cmd.group() == '#ougi':
            line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text='Daftar jurus : '+', '.join(daftar_jurus)))
        # panggil
        elif cmd.group() == '#panggil':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="It's curry night!"))
        # profil
        elif cmd.group() == '#profil':
            if isinstance(event.source, SourceUser) or isinstance(event.source, SourceRoom) or isinstance(event.source, SourceGroup):
                profile = line_bot_api.get_profile(event.source.user_id)
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(
                            text='Hai ' + profile.display_name
                        ),
                        TextSendMessage(
                            text='Status message mu: ' + profile.status_message
                        )
                    ]
                )
        # need help?
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="butuh bantuan? ketik '#help'"))
    # shortcut tag
    elif (text[0] == '/') and (text[len(text)-1] == '/'):
        judul_tag = search(r'\/(.*)',text).group(1)[:-1]
        if judul_tag in daftar_tag:
            image_message = ImageSendMessage(
                    original_content_url=img_url[cmd.group(2)][0],
                    preview_image_url=img_url[cmd.group(2)][1])
            line_bot_api.reply_message(event.reply_token, image_message)
        else:
            line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="Untuk melihat list tag ketik '#tags'"))
            

# handle join event
@handler.add(JoinEvent)
def handle_join(event):
    if event.source.type == 'group':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Watashinonamaeha akatsukidesu ;-;')
            )


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))



if __name__ == "__main__":
    
    # create tmp dir for download content
    #make_static_tmp_dir()
    
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)
