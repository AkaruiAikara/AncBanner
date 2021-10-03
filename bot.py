import os

from PIL import Image, ImageFont, ImageDraw
from pyrogram import Client, filters

ENV = bool(os.environ.get("ENV", False))

if ENV:
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

    app = Client(":memory:",
        api_id = API_ID,
        api_hash = API_HASH,
        bot_token = BOT_TOKEN
    )
else:
    app = Client(":memory:", config_file="config.ini")

@app.on_message(filters.command("banner", prefixes="/"))
def banner(_, msg):
    args = msg.text.split(None, 1)
    if len(args) < 2:
        return msg.reply_text("format: `/banner [Device | Codename] & [maintainer]`")
    info = args[1].split(" & ")
    if len(info) < 2:
        return msg.reply_text("format: `/banner [Device | Codename] & [maintainer]`")

    line1 = "Update Coming !"
    line2 = info[0]
    line3 = "Maintained by "
    maintainer = info[1]

    banner = Image.open("assets/anci56template.png")

    font1 = ImageFont.truetype("assets/ProductSans-Regular.ttf", 70)
    font2 = ImageFont.truetype("assets/ProductSans-Regular.ttf", 45)
    font3 = ImageFont.truetype("assets/ProductSans-Italic.ttf", 45)

    edit = ImageDraw.Draw(banner)

    edit.text((500, 140), line1, (0, 0, 0), font=font1)
    edit.text((500, 225), line2, (0, 0, 0), font=font2)
    edit.text((500, 285), line3, (0, 0, 0), font=font2)
    edit.text((788, 285), maintainer, (0, 0, 0), font=font3)

    device = line2.split(" | ")
    if len(device) < 2:
        return msg.reply_text("Did you put '|' separator?")
    namefile = "{}.png".format(device[1])
    banner.save(namefile)
    msg.reply_document(namefile)
    if os.path.exists(namefile):
        return os.remove(namefile)

app.run()