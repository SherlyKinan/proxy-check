import telegram
import os
import time

# --- Konfigurasi ---
# Ganti dengan Token API Bot Telegram Anda yang Anda dapatkan dari BotFather.
TELEGRAM_BOT_TOKEN = "7562323829:AAGr5jb4XNf6D_JOBPsF8yE4PqAgQFC82XM"

# Ganti dengan Channel ID Telegram Anda (contoh: -1001234567890).
# Pastikan bot Anda adalah administrator di channel ini dengan izin 'Post Messages'.
TELEGRAM_CHANNEL_ID = "-1002292042831"

# Nama file TXT yang berisi pesan-pesan yang akan dikirim, satu pesan per baris.
FILE_PESAN_PER_BARIS_TXT = "aktif.txt"

# Jeda waktu antar pengiriman pesan (dalam detik).
# Ini sangat penting untuk menghindari batasan laju (rate limit) Telegram API.
# Jika Anda mengirim terlalu cepat, bot Anda bisa diblokir sementara.
DELAY_ANTAR_PESAN_DETIK = 2

def kirim_pesan_per_baris_dari_file_txt():
    """
    Membaca setiap baris dari file TXT dan mengirimkannya sebagai pesan terpisah
    ke channel Telegram, dengan jeda waktu antar pengiriman untuk menghindari rate limit.
    """
    try:
        # Periksa apakah file TXT yang ditentukan ada di direktori yang sama.
        if not os.path.exists(FILE_PESAN_PER_BARIS_TXT):
            print(f"Error: File '{FILE_PESAN_PER_BARIS_TXT}' tidak ditemukan.")
            print("Pastikan file tersebut ada di direktori yang sama dengan skrip ini.")
            return

        # Inisialisasi objek bot Telegram dengan token API Anda.
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

        pesan_dikirim = 0
        # Buka dan baca file TXT baris per baris.
        with open(FILE_PESAN_PER_BARIS_TXT, 'r', encoding='utf-8') as f:
            for line in f:
                # Membersihkan spasi di awal/akhir baris dan karakter newline.
                pesan = line.strip()

                # Lewati baris kosong agar tidak mengirim pesan kosong.
                if not pesan:
                    continue

                try:
                    # Kirim pesan ke channel Telegram.
                    # Anda bisa menambahkan parse_mode='HTML' atau 'MarkdownV2'
                    # jika setiap baris pesan Anda mengandung formatting (misal: *bold*, _italic_).
                    # Contoh: bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=pesan, parse_mode='MarkdownV2')
                    bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=pesan)
                    print(f"Pesan berhasil dikirim: '{pesan}'")
                    pesan_dikirim += 1

                    # Jeda waktu sebelum mengirim pesan berikutnya.
                    time.sleep(DELAY_ANTAR_PESAN_DETIK)

                except telegram.error.BadRequest as e:
                    # Tangani error spesifik dari Telegram API (misal: pesan terlalu panjang, formatting salah).
                    print(f"Error mengirim pesan '{pesan}': {e}")
                    # Lanjutkan ke pesan berikutnya meskipun ada error pada satu pesan.
                except Exception as e:
                    # Tangani error tak terduga lainnya saat pengiriman pesan.
                    print(f"Terjadi kesalahan tak terduga saat mengirim pesan '{pesan}': {e}")
                    # Jika error kritis, mungkin lebih baik berhenti.
                    break

        print(f"\nSelesai! Total {pesan_dikirim} pesan berhasil dikirim dari '{FILE_PESAN_PER_BARIS_TXT}'.")

    except telegram.error.Unauthorized:
        # Tangani error jika token bot tidak valid.
        print("Error: Token Bot Telegram tidak valid. Periksa TELEGRAM_BOT_TOKEN Anda.")
    except Exception as e:
        # Tangani error umum yang terjadi pada skrip.
        print(f"Terjadi kesalahan umum pada skrip: {e}")

# --- Cara Penggunaan Skrip ---
if __name__ == "__main__":
