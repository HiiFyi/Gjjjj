"""
 * @author        yasir <yasiramunandar@gmail.com>
 * @date          2022-12-01 09:12:27
 * @lastModified  2022-12-01 09:32:31
 * @projectName   MissKatyPyro
 * Copyright @YasirPedia All rights reserved
"""

import asyncio
import re
from logging import getLogger

from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from misskaty import app
from misskaty.core.decorator.errors import capture_err
from misskaty.helper.http import http
from misskaty.vars import COMMAND_HANDLER

LOGGER = getLogger(__name__)

headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}


@app.on_message(filters.command(["zonafilm"], COMMAND_HANDLER))
@capture_err
async def zonafilm(_, msg):
    m = await msg.reply("**__⏳ Please wait, scraping data ...__**", True)
    try:
        title = msg.text.split(" ", 1)[1]
    except IndexError:
        title = ""
    try:
        html = await http.get(f"https://zonafilm.icu/?s={title}", headers=headers)
        text = BeautifulSoup(html.text, "lxml")
        entry = text.find_all(class_="entry-header")
        if "Nothing Found" in entry[0].text:
            await m.delete()
            if not title:
                await msg.reply("404 Not FOUND!", True)
            else:
                await msg.reply(f"404 Not FOUND For: {title}", True)
            return
        data = []
        for i in entry:
            genre = i.find(class_="gmr-movie-on").text
            genre = f"{genre}" if genre != "" else "N/A"
            judul = i.find(class_="entry-title").find("a").text
            link = i.find(class_="entry-title").find("a").get("href")
            data.append({"judul": judul, "link": link, "genre": genre})
        head = f"<b>#Zonafilm Results For:</b> <code>{title}</code>\n\n" if title else f"<b>#Zonafilm Latest:</b>\n🌀 Use /{msg.command[0]} [title] to start search with title.\n\n"
        msgs = ""
        await m.delete()
        for c, i in enumerate(data, start=1):
            msgs += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Genre:</b> <code>{i['genre']}</code>\n"
            msgs += f"<b>Extract:</b> <code>/{msg.command[0]}_scrap {i['link']}</code>\n\n" if "/tv/" not in i["link"] else "\n"
            if len(head.encode("utf-8") + msgs.encode("utf-8")) >= 4000:
                await msg.reply(
                    head + msgs,
                    True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="❌ Close",
                                    callback_data=f"close#{msg.from_user.id}",
                                )
                            ]
                        ]
                    ),
                )
                await asyncio.sleep(2)
                msgs = ""
        if msgs != "":
            await msg.reply(
                head + msgs,
                True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="❌ Close",
                                callback_data=f"close#{msg.from_user.id}",
                            )
                        ]
                    ]
                ),
            )
    except Exception as e:
        LOGGER.error(e)
        await m.delete()
        await msg.reply(f"ERROR: <code>{e}</code>", True)


@app.on_message(filters.command(["nodrakor"], COMMAND_HANDLER))
@capture_err
async def nodrakor(_, msg):
    m = await msg.reply("**__⏳ Please wait, scraping data ...__**", True)
    try:
        title = msg.text.split(" ", 1)[1]
    except IndexError:
        title = ""
    try:
        html = await http.get(f"http://173.212.199.27/?s={title}", headers=headers)
        text = BeautifulSoup(html.text, "lxml")
        entry = text.find_all(class_="entry-header")
        if "Nothing Found" in entry[0].text:
            await m.delete()
            if not title:
                await msg.reply("404 Not FOUND!", True)
            else:
                await msg.reply(f"404 Not FOUND For: {title}", True)
            return
        data = []
        for i in entry:
            genre = i.find(class_="gmr-movie-on").text
            genre = f"{genre[:-2]}" if genre != "" else "N/A"
            judul = i.find(class_="entry-title").find("a").text
            link = i.find(class_="entry-title").find("a").get("href")
            data.append({"judul": judul, "link": link, "genre": genre})
        head = f"<b>#Nodrakor Results For:</b> <code>{title}</code>\n\n" if title else f"<b>#Nodrakor Latest:</b>\n🌀 Use /{msg.command[0]} [title] to start search with title.\n\n"
        msgs = ""
        await m.delete()
        for c, i in enumerate(data, start=1):
            msgs += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Genre:</b> <code>{i['genre']}</code>\n<b>Extract:</b> <code>/{msg.command[0]}_scrap {i['link']}</code>\n\n"
            if len(head.encode("utf-8") + msgs.encode("utf-8")) >= 4000:
                await msg.reply(
                    head + msgs,
                    True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="❌ Close",
                                    callback_data=f"close#{msg.from_user.id}",
                                )
                            ]
                        ]
                    ),
                )
                await asyncio.sleep(2)
                msgs = ""
        if msgs != "":
            await msg.reply(head + msgs, True, disable_web_page_preview=True)
    except Exception as e:
        LOGGER.error(e)
        await m.delete()
        await msg.reply(f"ERROR: <code>{e}</code>", True)


# Broken
@app.on_message(filters.command(["ngefilm21"], COMMAND_HANDLER))
@capture_err
async def ngefilm21(_, message):
    if len(message.command) == 1:
        return await message.reply("Masukkan query yang akan dicari..!!")
    title = message.text.split(" ", maxsplit=1)[1]

    msg = await message.reply("Sedang proses scrap, mohon tunggu..")
    try:
        html = await http.get(f"https://ngefilm.info/search?q={title}", headers=headers)
        soup = BeautifulSoup(html.text, "lxml")
        res = soup.find_all("h2")
        data = []
        for i in res:
            a = i.find_all("a")[0]
            judul = a.find_all(class_="r-snippetized")
            b = i.find_all("a")[0]["href"]
            data.append({"judul": judul[0].text, "link": b})
        if not data:
            return await msg.edit("Oops, data film tidak ditemukan.")
        res = "".join(f"<b>{i['judul']}</b>\n{i['link']}\n" for i in data)
        await msg.edit(
            f"<b>Hasil Scrap dari Ngefilm21:</b>\n{res}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❌ Close",
                            callback_data=f"close#{message.from_user.id}",
                        )
                    ]
                ]
            ),
        )
    except Exception as e:
        await msg.edit(f"ERROR: {str(e)}")


# Scrape Web From Movieku.CC
@app.on_message(filters.command(["movieku"], COMMAND_HANDLER))
@capture_err
async def movikucc(_, msg):
    m = await msg.reply("**__⏳ Please wait, scraping data ...__**", True)
    data = []
    if len(msg.command) == 1:
        try:
            html = await http.get("https://107.152.37.223/")
            r = BeautifulSoup(html.text, "lxml")
            res = r.find_all(class_="bx")
            for i in res:
                judul = i.find_all("a")[0]["title"]
                link = i.find_all("a")[0]["href"]
                data.append({"judul": judul, "link": link})
            if not data:
                await m.delete()
                return await msg.reply("404 Result not FOUND!", True)
            await m.delete()
            head = f"<b>#Movieku Latest:</b>\n🌀 Use /{msg.command[0]} [title] to start search with title.\n\n"
            msgs = ""
            for c, i in enumerate(data, start=1):
                msgs += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Extract:</b> <code>/{msg.command[0]}_scrap {i['link']}</code>\n\n"
                if len(head.encode("utf-8") + msgs.encode("utf-8")) >= 4000:
                    await msg.reply(
                        head + msgs,
                        True,
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="❌ Close",
                                        callback_data=f"close#{msg.from_user.id}",
                                    )
                                ]
                            ]
                        ),
                    )
                    await asyncio.sleep(2)
                    msgs = ""
            if msgs != "":
                await msg.reply(
                    head + msgs,
                    True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="❌ Close",
                                    callback_data=f"close#{msg.from_user.id}",
                                )
                            ]
                        ]
                    ),
                )
        except Exception as e:
            LOGGER.error(e)
            await m.delete()
            await msg.reply(f"ERROR: {e}", True)
    else:
        title = msg.text.split(" ", 1)[1]
        try:
            html = await http.get(f"https://107.152.37.223/?s={title}")
            r = BeautifulSoup(html.text, "lxml")
            res = r.find_all(class_="bx")
            for i in res:
                judul = i.find_all("a")[0]["title"]
                link = i.find_all("a")[0]["href"]
                data.append({"judul": judul, "link": link})
            if not data:
                await m.delete()
                return await msg.reply("404 Result not FOUND!", True)
            await m.delete()
            head = f"<b>#Movieku Results For:</b> <code>{title}</code>\n\n"
            msgs = ""
            for c, i in enumerate(data, start=1):
                msgs += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Extract:</b> <code>/{msg.command[0]}_scrap {i['link']}</code>\n\n"
                if len(head.encode("utf-8") + msgs.encode("utf-8")) >= 4000:
                    await msg.reply(
                        head + msgs,
                        True,
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="❌ Close",
                                        callback_data=f"close#{msg.from_user.id}",
                                    )
                                ]
                            ]
                        ),
                    )
                    await asyncio.sleep(2)
                    msgs = ""
            if msgs != "":
                await msg.reply(
                    head + msgs,
                    True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="❌ Close",
                                    callback_data=f"close#{msg.from_user.id}",
                                )
                            ]
                        ]
                    ),
                )
        except Exception as e:
            LOGGER.error(e)
            await m.delete()
            await msg.reply(f"ERROR: {e}", True)


@app.on_message(filters.command(["savefilm21"], COMMAND_HANDLER))
@capture_err
async def savefilm21(_, msg):
    SITE = "https://185.99.135.215"
    try:
        title = msg.text.split(" ", 1)[1]
    except:
        title = None
    m = await msg.reply("**__⏳ Please wait, scraping data...__**", True)
    data = []
    try:
        if title is not None:
            html = await http.get(f"{SITE}/?s={title}", headers=headers)
            bs4 = BeautifulSoup(html.text, "lxml")
            res = bs4.find_all(class_="entry-title")
            for i in res:
                pas = i.find_all("a")
                judul = pas[0].text
                link = pas[0]["href"]
                data.append({"judul": judul, "link": link})
            if not data:
                await m.delete()
                return await msg.reply("404 Result not FOUND!", True)
            await m.delete()
            head = f"<b>#SaveFilm21 Results For:</b> <code>{title}</code>\n\n"
        else:
            html = await http.get(SITE, headers=headers)
            bs4 = BeautifulSoup(html.text, "lxml")
            res = bs4.find_all(class_="entry-title")
            for i in res:
                pas = i.find_all("a")
                judul = pas[0].text
                link = pas[0]["href"]
                data.append({"judul": judul, "link": link})
            await m.delete()
            head = f"<b>#SaveFilm21 Latest:</b>\n🌀 Use /{msg.command[0]} [title] to start search with title.\n\n"
        msgs = ""
        for c, i in enumerate(data, start=1):
            msgs += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Extract:</b> <code>/{msg.command[0]}_scrap {i['link']}</code>\n\n"
            if len(head.encode("utf-8") + msgs.encode("utf-8")) >= 4000:
                await msg.reply(
                    head + msgs,
                    True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="❌ Close",
                                    callback_data=f"close#{msg.from_user.id}",
                                )
                            ]
                        ]
                    ),
                )
                await asyncio.sleep(2)
                msgs = ""
        if msgs != "":
            await msg.reply(
                head + msgs,
                True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="❌ Close",
                                callback_data=f"close#{msg.from_user.id}",
                            )
                        ]
                    ]
                ),
            )
    except Exception as e:
        await m.delete()
        LOGGER.error(e)
        await msg.reply(f"ERROR: {e}", True)