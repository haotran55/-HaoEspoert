import os
import threading
import requests
import telebot  # Thêm dòng này để sử dụng telebot
from flask import Flask, request
from datetime import datetime
from io import BytesIO

# Lấy token từ biến môi trường
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
ALLOWED_GROUP_IDS = [-1002639856138]

# Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot đang hoạt động trên Render!"

import requests
from io import BytesIO

# Hàm lấy video
def get_random_video():
    try:
        res = requests.get("https://api.ffcommunity.site/randomvideo.php", timeout=5)
        data = res.json()
        return data.get("url")
    except:
        return None

@bot.message_handler(commands=['video'])
def random_video(message):
    if message.chat.id not in ALLOWED_GROUP_IDS:
        bot.reply_to(message, "Bot Chỉ Hoạt Động Trong Nhóm Này.\nLink: https://t.me/tranhao1166")
        return

    # Thông báo đang tải video (reply_to)
    loading_msg = bot.reply_to(message, "Đang tải video...")

    video_url = get_random_video()
    if video_url:
        try:
            bot.send_chat_action(message.chat.id, "upload_video")
            res = requests.get(video_url, stream=True, timeout=10)
            if res.status_code == 200:
                video_file = BytesIO(res.content)
                video_file.name = "video.mp4"
                bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    caption="Video gái xinh By @BotHaoVip_bot",
                    reply_to_message_id=message.message_id
                )
                bot.delete_message(message.chat.id, loading_msg.message_id)
            else:
                bot.edit_message_text(
                    "Không thể tải video từ nguồn.",
                    chat_id=message.chat.id,
                    message_id=loading_msg.message_id
                )
        except Exception as e:
            print("Lỗi gửi video:", e)
            bot.edit_message_text(
                "Lỗi khi gửi video.",
                chat_id=message.chat.id,
                message_id=loading_msg.message_id
            )
    else:
        bot.edit_message_text(
            "Không lấy được video, thử lại sau nhé!",
            chat_id=message.chat.id,
            message_id=loading_msg.message_id
        )

@bot.message_handler(commands=['start','help'])
def send_about(message):
    if message.chat.id not in ALLOWED_GROUP_IDS:
        bot.reply_to(message, "Bot Chỉ Hoạt Động Trong Nhóm Này.\nLink: https://t.me/tranhao1166")
        return

    user = message.from_user
    full_name = f"{user.first_name} {user.last_name or ''}".strip()

    bot.reply_to(message, f"""Xin Chào Bạn {full_name}
<blockquote>
Lệnh Cơ Bản
</blockquote>
<blockquote>
│» /help : Lệnh trợ giúp
│» /admin : Thông tin admin
│» /spam : Spam SMS FREE
│» /spamvip : Spam SMS VIP - Mua Vip 30k/Tháng
│» /share : Free 400 - Vip 1k share trên lần
│» /id : Lấy ID Tele Của Bản Thân
│» /voice : Đổi Văn Bản Thành Giọng Nói.
│» /tiktok : Check Thông Tin - Tải Video Tiktok.
│» /tool : Tải JirayTool
│» /time : check thời gian hoạt động
│» /ad : có bao nhiêu admin
│» /code : Lấy Code html của web
│» /tv : Đổi Ngôn Ngữ Sang Tiếng Việt
│» Lệnh Cho ADMIN
│» /rs : Khởi Động Lại
│» /add : Thêm người dùng sử dụng /spamvip
└───────────⧕
</blockquote>""", parse_mode="HTML")

# Webhook nhận update từ Telegram
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok', 200

# Khởi chạy Flask và bot song song
if __name__ == "__main__":
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
    if not WEBHOOK_URL:
        raise Exception("Thiếu biến môi trường WEBHOOK_URL")

    # Xóa webhook cũ và thiết lập webhook mới
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")

    # Chạy Flask (webhook listener)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

  
