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

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


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
    if text[0] == '#':
        cmd = search(r'\#(\w*)\s*(.*)', text)
        # profile
        if cmd.group() == '#profile':
            if isinstance(event.source, SourceUser):
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
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Aduuh.. perintah #profile harus digunakan melalui personal chat yaa"))
        # bye
        elif cmd.group() == '#bye':
            if isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
                image_message = ImageSendMessage(
                    original_content_url='https://image.ibb.co/dz0HXv/akatsukileave.jpg',
                    preview_image_url='https://image.ibb.co/bYMPCv/akatsukileave_prev.jpg')
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
        # info
        elif cmd.group() == '#info':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Dibuat sebagai project pembelajaran oleh: Ikraduya Edian(line:ikraduya)'))
        # help
        elif cmd.group() == '#help':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="""list perintah :
                                                        buttons, bye, confirm, help, info, naga kacang, panggil
                                                        Gunakan '#' di awal perintah
                                                        contoh: #profile"""))
        # panggil
        elif cmd.group() == '#panggil':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="It's curry night!"))
        # jurus
        elif cmd.group(1) == 'jurus':
            daftar_jurus = {'naga kacang':'nagakacang.txt'}
            if cmd.group(2) in daftar_jurus:
                f = open('statics/' + daftar_jurus[cmd.group(2)], 'r')
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text=('Jurus '+cmd.group(2).upper() + '!')),
                                        TextSendMessage(text=str(f.read()))])
                f.close()
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text='Mana ada jurus begitu..'))
        # need help?
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="butuh bantuan? ketik '#help'"))
        

# handle join event
@handler.add(JoinEvent)
def handle_join(event):
    if event.source.type == 'group':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Watashinonamaeha akatsukidesu')
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
    make_static_tmp_dir()
    
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)
