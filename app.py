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
    CarouselTemplate, CarouselColumn, PostbackEvent,
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

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

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
        # profile
        if text == '#profile':
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
        elif text == '#bye':
            if isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
                image_message = ImageSendMessage(
                    original_content_url='https://s-media-cache-ak0.pinimg.com/736x/8e/0e/f1/8e0ef15e0ba7a598dbe69658c7b38379--nerd-art-cosplay-anime.jpg',
                    preview_image_url='https://a.wattpad.com/useravatar/tori_tatsu.128.745644.jpg')
                line_bot_api.reply_message(event.reply_token, image_message)
                try:
                    line_bot_api.leave_group(event.source.group_id)
                except:
                    line_bot_api.leave_room(event.source.room_id)   
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextMessage(text="Mana bisa keluar dari personal chat qaqa ^-^"))
        # confirm
        elif text == '#confirm':
            confirm_template = ConfirmTemplate(text='Do it ;-)?', actions=[
                MessageTemplateAction(label='Just Do It!', text='Just Do It!'),
                MessageTemplateAction(label='wat', text='wat'),
            ])
            template_message = TemplateSendMessage(
                alt_text='Confirm alt text', template=confirm_template)
            line_bot_api.reply_message(event.reply_token, template_message)
        # buttons
        elif text == '#buttons':
            buttons_template = ButtonsTemplate(
                title='Dipilih-dipilih', text='Hello, silahkan dipilih', actions=[
                    URITemplateAction(
                        label='Jangan tekan', uri='https://ikraduyae.blogspot.co.id'),
                    PostbackTemplateAction(label='ping', data='ping'),
                    PostbackTemplateAction(
                        label='ping with text', data='ping',
                        text='ping'),
                    MessageTemplateAction(label="Transliterasi 'Nasi'", text='米')
                ])
            template_message = TemplateSendMessage(
                alt_text='Hello, silahkan dipilih', template=buttons_template)
            line_bot_api.reply_message(event.reply_token, template_message)
        # info
        elif text == '#info':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Dibuat sebagai project pembelajaran oleh: Ikraduya Edian(line:ikraduya)'))
        # help
        elif text == '#help':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="""list perintah :
                                                        buttons, bye, confirm, help, info, naga kacang, panggil
                                                        Gunakan '#' di awal perintah
                                                        contoh: #profile"""))
        # panggil
        elif text == '#panggil':
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="It's curry night!"))
        # jurus naga kacang
        elif text == '#naga kacang':
            f = open('statics/nagakacang.txt', 'r')
            line_bot_api.reply_message(
                event.reply_token, [TextSendMessage(text='Jurus Naga Kacang!!'),
                                    TextSendMessage(text=str(f.read()))])
            f.close()
        # need help?
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="butuh bantuan? ketik '#help'"))

"""            
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )
"""

"""
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )
"""
"""
# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='File saved.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])
"""

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
