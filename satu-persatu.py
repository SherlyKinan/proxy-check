import asyncio
from telegram import Bot


# Token API dari BotFather
TOKEN = '7562323829:AAGr5jb4XNf6D_JOBPsF8yE4PqAgQFC82XM'

# ID Chat tujuan
CHAT_ID = '-1002292042831'

# Nama file txt yang berisi data
FILE_TXT = 'aktif.txt'

async def kirim_pesan():
    bot = Bot(TOKEN)
    try:
        with open(FILE_TXT, 'r') as file:
            data = file.read()
            await bot.send_message(chat_id=CHANNEL_ID, text=data)
    except FileNotFoundError:
        print(f"File {FILE_TXT} tidak ditemukan.")

async def main():
    await kirim_pesan()

if __name__ == '__main__':
    asyncio.run(main())
    
