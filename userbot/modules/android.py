# Copyright (C) 2021-2022 Team Repondeur.
#
# Licensed under the Team Repondeur Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to android"""

import json
import re

import requests
from bs4 import BeautifulSoup

from userbot import CMD_HELP
from userbot.events import register

GITHUB = "https://github.com"


@register(outgoing=True, pattern=r"^\.magisk$")
async def magisk(request):
    magisk_dict = {
        "Stable": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/stable.json",
        "Beta": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/beta.json",
        "Canary": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/canary.json",
    }
    releases = "**Latest Magisk Releases:**\n"
    for name, release_url in magisk_dict.items():
        data = requests.get(release_url).json()
        releases += (
            f'**{name} v{data["magisk"]["version"]}:** [APK]({data["magisk"]["link"]}) | '
            f'[Changelog]({data["magisk"]["note"]})\n'
        )
    await request.edit(releases)


@register(outgoing=True, pattern=r"^\.device(?: |$)(\S*)")
async def device_info(request):
    """get android device basic info from its codename"""
    textx = await request.get_reply_message()
    codename = request.pattern_match.group(1)
    if codename:
        pass
    elif textx:
        codename = textx.text
    else:
        await request.edit("**Usage:** `.device <codename/model>`")
        return
    data = json.loads(
        requests.get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = f"**Search results for** `{codename}`:\n\n"
        for item in results:
            reply += (
                f"Brand: `{item['brand']}`\n"
                f"Name: `{item['name']}`\n"
                f"Model: `{item['model']}`\n\n"
            )
    else:
        reply = f"`Couldn't find info about {codename}!`\n"
    await request.edit(reply)


@register(outgoing=True, pattern=r"^\.codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def codename_info(request):
    """search for android codename"""
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.edit("**Usage:** `.codename <brand> <device>`")
        return

    data = json.loads(
        requests.get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}  # Lower brand names in JSON
    devices = devices_lower.get(brand)
    results = [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]
    if results:
        reply = f"**Search results for** `{brand} {device}`:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"Device: `{item['device']}`\n"
                f"Name: `{item['name']}`\n"
                f"Model: `{item['model']}`\n\n"
            )
    else:
        reply = f"**Couldn't find the codename of** `{brand} {device}`\n"
    await request.edit(reply)


@register(outgoing=True, pattern=r"^\.specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def devices_specifications(request):
    """Mobile devices specifications"""
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.edit("**Usage:** `.specs <brand> <device>`")
        return
    all_brands = (
        BeautifulSoup(
            requests.get("https://www.devicespecifications.com/en/brand-more").content,
            "lxml",
        )
        .find("div", {"class": "brand-listing-container-news"})
        .findAll("a")
    )
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await request.edit(f"`{brand}` **is an unknown brand!**")
        return
    devices = BeautifulSoup(requests.get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await request.edit(f"**Can't find** `{device}`.")
        return
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(requests.get(url).content, "lxml")
        reply = "\n" + info.title.text.split("-")[0].strip() + "\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await request.edit(reply)


@register(outgoing=True, pattern=r"^\.twrp(?: |$)(\S*)")
async def twrp(request):
    """get android device twrp"""
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await request.edit("**Usage:** `.twrp <codename>`")
        return
    url = requests.get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"**Couldn't find TWRP downloads for** `{device}`!`\n"
        await request.edit(reply)
        return
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await request.edit(reply)


CMD_HELP.update(
    {
        "android": ">`.magisk`"
        "\nGet latest Magisk releases"
        "\n\n>`.device <codename>`"
        "\nUsage: Get info about android device codename or model."
        "\n\n>`.codename <brand> <device>`"
        "\nUsage: Search for android device codename."
        "\n\n>`.specs <brand> <device>`"
        "\nUsage: Get device specifications info."
        "\n\n>`.twrp <codename>`"
        "\nUsage: Get latest twrp download for android device."
    }
)
