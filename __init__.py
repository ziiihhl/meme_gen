import os.path
from io import BytesIO
import httpx
from meme_generator import get_meme
from meme_gen.utils import meme_keywords
import base64
from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img

meme_gen = SV("表情包生成")
@meme_gen.on_command("表情包")
async def main(bot: Bot, event: Event):
    client = httpx.AsyncClient()
    avatar_url = event.sender['avatar']
    get_resp = await client.get(avatar_url)
    get_resp.raise_for_status()
    avatar = get_resp.content
    name = event.sender['nickname']
    text = event.text.strip()
    if text :
        if text != "帮助":
            try:
                meme = get_meme(text)
                result = meme(images=[avatar], texts=[], args={"circle": True})
                message = await convert_img(result.getvalue())
                await bot.send(await convert_img(avatar))
            except Exception as e:
                await bot.send(f"错误:{e}请输入有效的key！")
        else:
            await bot.send(await convert_img(os.path.dirname(os.path.abspath(__file__)) + "/docs/screenshot.png"))






"""
    meme = get_meme("kurogames_abby_eat")
    result = meme(images=["avatar.jpg"], texts=[], args={"circle": True})

    with open("result.gif", "wb") as f:
        f.write(result.getvalue())
"""

if __name__ == "__main__":
    main()