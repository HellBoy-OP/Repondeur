import asyncio
import time

from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import *
from userbot.utils import *
from userbot.events import *
import requests
perf = "[Repondeur]"
admin_mention = os.environ.get("ALIVE_NAME", None)
@bot.on(admin_cmd(pattern="song ?(.*)"))
async def _(event):
    query = event.text[6:]
    max_results = 1
    if query == "":
        return await eod(event, "__Please give a song name to search.__")
    admin = await eor(event, f"__Searching for__ `{query}`")
    hel_ = await song_search(event, query, max_results, details=True)
    x, title, views, duration, thumb = hel_[0], hel_[1], hel_[2], hel_[3], hel_[4]
    thumb_name = f'song.jpg'
    thumbnail = requests.get(thumb, allow_redirects=True)
    open(thumb_name, 'wb').write(thumbnail.content)
    url = x.replace("\n", "")
    try:
        await admin.edit("**Fetching Song**")
        with YoutubeDL(song_opts) as somg:
            admin_data = somg.extract_info(url)
    except DownloadError as DE:
        return await eod(admin, f"`{str(DE)}`")
    except ContentTooShortError:
        return await eod(admin, "`The download content was too short.`")
    except GeoRestrictedError:
        return await eod(admin, "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`")
    except MaxDownloadsReached:
        return await eod(admin, "`Max-downloads limit has been reached.`")
    except PostProcessingError:
        return await eod(admin, "`There was an error during post processing.`")
    except UnavailableVideoError:
        return await eod(admin, "`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        return await eod(admin, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await eod(admin, "`There was an error during info extraction.`")
    except Exception as e:
        return await eod(admin, f"{str(type(e)): {str(e)}}")
    c_time = time.time()
    await admin.edit(f"**🎶 Preparing to upload song 🎶 :** \n\n{admin_data['title']} \n**By :** {admin_data['uploader']}")
    await event.client.send_file(
        event.chat_id,
        f"{admin_data['id']}.mp3",
        supports_streaming=True,
        caption=f"**✘ Song -** `{title}` \n**✘ Views -** `{views}` \n**✘ Duration -** `{duration}` \n\n**✘ By :** {admin_mention}",
        thumb=thumb_name,
        attributes=[
            DocumentAttributeAudio(
                duration=int(admin_data["duration"]),
                title=str(admin_data["title"]),
                performer=perf,
            )
        ],
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "Uploading..", f"{admin_data['title']}.mp3")
        ),
    )
    await admin.delete()
    os.remove(f"{admin_data['id']}.mp3")


@bot.on(admin_cmd(pattern="vsong ?(.*)"))
async def _(event):
    query = event.text[7:]
    max_results = 1
    if query == "":
        return await eod(event, "__Please give a song name to search.__")
    admin = await eor(event, f"__Searching for__ `{query}`")
    hel_ = await song_search(event, query, max_results, details=True)
    x, title, views, duration, thumb = hel_[0], hel_[1], hel_[2], hel_[3], hel_[4]
    thumb_name = f'thumb{"video"}.jpg'
    thumbnail = requests.get(thumb, allow_redirects=True)
    open(thumb_name, 'wb').write(thumbnail.content)
    url = x.replace("\n", "")
    try:
        await admin.edit("**Fetching Video**")
        with YoutubeDL(video_opts) as somg:
            admin_data = somg.extract_info(url)
    except DownloadError as DE:
        return await eod(admin, f"`{str(DE)}`")
    except ContentTooShortError:
        return await eod(admin, "`The download content was too short.`")
    except GeoRestrictedError:
        return await eod(admin, "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`")
    except MaxDownloadsReached:
        return await eod(admin, "`Max-downloads limit has been reached.`")
    except PostProcessingError:
        return await eod(admin, "`There was an error during post processing.`")
    except UnavailableVideoError:
        return await eod(admin, "`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        return await eod(admin, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await eod(admin, "`There was an error during info extraction.`")
    except Exception as e:
        return await eod(admin, f"{str(type(e)): {str(e)}}")
    c_time = time.time()
    await admin.edit(f"**📺 Preparing to upload video 📺 :** \n\n{admin_data['title']}\n**By :** {admin_data['uploader']}")
    await event.client.send_file(
        event.chat_id,
        f"{admin_data['id']}.mp4",
        supports_streaming=True,
        caption=f"**✘ Video :** `{title}` \n\n**✘ By :** {admin_mention}",
        thumb=thumb_name,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "Uploading..", f"{admin_data['title']}.mp4")
        ),
    )
    await admin.delete()
    os.remove(f"{admin_data['id']}.mp4")


CMD_HELP.update(
    {
        "song": "`.song <Song Name>`"
        "\nUsage: Provides Song Via Youtube."
        "\n\n>`.vsong <Video Song Name>`"
        "\nUsage: Provides Video Song Via Youtube."
    }
)
