from telethon import TelegramClient, events
import asyncio
import random

# ========= CONFIG =========
api_id = 26628669
api_hash = "3464c396ae28845a98067837dfd99685"

SESSION_NAME = "relay_account"
ANON_BOT = "chatbot"
GROUP_ID = -5297949815

DELAY_RANGE = (1, 3)
# ==========================

client = TelegramClient(SESSION_NAME, api_id, api_hash)
relay_active = True


# ===== HARD CLEAR (HAPUS SEMUA) =====
async def hard_clear():
    async for msg in client.iter_messages(GROUP_ID):
        try:
            await msg.delete()
        except:
            pass
    await client.send_message(GROUP_ID, " ")


# ===== TERIMA DARI BOT (TEXT + STICKER) =====
@client.on(events.NewMessage(from_users=ANON_BOT))
async def from_bot(event):
    text = event.raw_text or ""

    low = text.lower()

    # blok feedback
    if "tinggalkan feedback" in low:
        return

    # hapus link bot
    text = text.replace("https://t.me/chatbot", "").strip()

    # kirim TEXT
    if text:
        await client.send_message(GROUP_ID, f"🕵️ Anonymous:\n{text}")

    # kirim MEDIA (sticker / gif / foto)
    if event.media:
        await client.send_file(GROUP_ID, event.media)


# ===== TERIMA DARI GRUP =====
@client.on(events.NewMessage(chats=GROUP_ID))
async def from_group(event):
    global relay_active

    # anti loop
    if event.out:
        return

    text = event.raw_text or ""

    # ===== COMMAND =====
    if text == "/c":
        await hard_clear()
        return

    if text == "/s":
        relay_active = True
        await client.send_message(ANON_BOT, "/start")
        return

    if text == "/st":
        relay_active = False
        return

    if text == "/n":
        await client.send_message(ANON_BOT, "/next")
        return

    if text == "/se":
        await client.send_message(ANON_BOT, "/search")
        return

    if not relay_active:
        return

    # ===== KIRIM TEXT =====
    if text.strip():
        async with client.action(ANON_BOT, 'typing'):
            await asyncio.sleep(random.randint(*DELAY_RANGE))
        await client.send_message(ANON_BOT, text)

    # ===== KIRIM MEDIA (STICKER DLL) =====
    if event.media:
        await client.send_file(ANON_BOT, event.media)


# ===== MAIN =====
async def main():
    print("🔥 RELAY MODE FINAL (STICKER + HARD CLEAR) AKTIF")
    await client.run_until_disconnected()


client.start()
client.loop.run_until_complete(main())
