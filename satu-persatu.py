import asyncio
from telegram import Bot

# Token API dari BotFather
TOKEN = '7562323829:AAGr5jb4XNf6D_JOBPsF8yE4PqAgQFC82XM'

# ID Chat tujuan
CHAT_ID = '-1002292042831'

# Nama file txt yang berisi data
FILE_TXT = 'aktif.txt'

async def kirim_pesan(bot):
    try:
        with open(FILE_TXT, 'r') as file:
            data = file.readlines()
            for line in data:
                line = line.strip()
                if line:
                    await bot.send_message(chat_id=CHAT_ID, text=line)
                    await asyncio.sleep(1)  # Tunggu 1 detik sebelum mengirim pesan berikutnya
    except FileNotFoundError:
        print(f"File {FILE_TXT} tidak ditemukan.")

async def main():
    bot = Bot(TOKEN)
    await kirim_pesan(bot)

if __name__ == '__main__':
    asyncio.run(main())
