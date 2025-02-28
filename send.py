from telegram import Bot
import datetime
from datetime import date
import pytz

BOT_TOKEN = "7562323829:AAGr5jb4XNf6D_JOBPsF8yE4PqAgQFC82XM"
CHAT_ID = -1001884100919
current_time = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
today = date.today()

def main():
    bot = Bot(BOT_TOKEN)
    file_paths = (
        "proxy.txt",
        "dead.txt",
        "active.txt",
        "proxylist1.txt",
        "proxylist2.txt",
    )

    for f in file_paths:
        with open(f, "rb") as fin:
            count = len(fin.readlines())
            # After the len(fin.readlines()) file's current position
            # will be at the end of the file. seek(0) sets the position
            # to the begining of the file so we can read it again during
            # sending.
            fin.seek(0)
            bot.send_document(
                CHAT_ID,
                document=fin,
                # Up to 1024 characters.
                # https://core.telegram.org/bots/api#inputmediadocument
                caption=f"Diperbarui pada: {current_time}\nLink: https://proxy.kuyshare.eu.org/{f}\nView Link: https://vless.5412.us.to/sub?proxy-list=https://proxy.kuyshare.eu.org/{f}"
            )


if __name__ == "__main__":
    main()
