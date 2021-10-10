import os
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

from Sangtei.events import register as Sangtei


@Sangtei(pattern="^/yt(audio|video) (.*)")
async def download_video(v_url):
    """ For ytdl command, download media from YouTube and many other sites. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()
    lmao = await v_url.reply("Download tur a siamrem mek ani e 😉")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "256",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    elif type == "video":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await lmao.edit("Data lak-khawm ani, lo nghak lawk 😉")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await lmao.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await lmao.edit("`I thil download hi a tawi lulai hle ani.`")
        return
    except GeoRestrictedError:
        await lmao.edit(
            "`He video hi i awmna bial vel atangin download theih ani lo, a chhan chu bial then khat tan website lam atanga block ani.`"
        )
        return
    except MaxDownloadsReached:
        await lmao.edit("`Download theih chin zat a pel tawh tlat.`")
        return
    except PostProcessingError:
        await lmao.edit("`Post tur a siam anih lai mek in harsatna a awm tlat mai.`")
        return
    except UnavailableVideoError:
        await lmao.edit("`He media hi i duh ang format hian a awm lo tlat.`")
        return
    except XAttrMetadataError as XAME:
        await lmao.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await lmao.edit("`Info vel lak khawm anih dawn lai in harsatna a awm tlat mai.`")
        return
    except Exception as e:
        await lmao.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await lmao.edit(
            f"`Hla chu upload tur a siam ani:`\
        \n**{ytdl_data['title']}**\
        \nby **{ytdl_data['uploader']}**"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=str(ytdl_data["uploader"]),
                )
            ],
        )
        os.remove(f"{ytdl_data['id']}.mp3")
    elif video:
        await lmao.edit(
            f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby **{ytdl_data['uploader']}**"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data["title"],
        )
        os.remove(f"{ytdl_data['id']}.mp4")


__help__ = """
 • `/ytaudio <link>` or `/ytvideo <link>`*:* Downlods a video or audio from a youtube video to the bots local server and uploads to telegram
"""
__mod_name__ = "YouTube 🎬"
