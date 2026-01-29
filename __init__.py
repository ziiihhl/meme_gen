import json
import os.path
import aiofiles
from io import BytesIO
import httpx
from meme_generator import get_meme
from meme_gen.utils import meme_keywords
from gsuid_core.models import Message
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
        meme_key = ''
        if text != "帮助":
            try:
                async with aiofiles.open(os.path.dirname(os.path.abspath(__file__)) +"/utils/info.json",'r') as f:
                    content = f.read()
                    info = json.loads(content)
                for key,val in info.items():
                    if text in val:
                        meme_key=key
                        break
                if meme_key:
                    meme = get_meme(meme_key)
                    result = meme(images=[avatar], texts=[], args={"circle": True})
                    message = await convert_img(result.getvalue())
                    await bot.send(message)
                else :
                    raise ValueError
            except Exception as e:
                await bot.send(f"错误:{e}请输入有效的key！")
        else:
            async with aiofiles.open(os.path.dirname(os.path.abspath(__file__)) + "/docs/compressed.jpg","rb")as fp:
                img_bytes = await fp.read()
            img_bs64 =base64.b64encode(img_bytes).decode()
            file_bs64 =img_bs64
            message = Message("file",f"帮助(请点查看原图！).jpg|{file_bs64}")
            await bot.send(message)






"""
    meme = get_meme("kurogames_abby_eat")
    result = meme(images=["avatar.jpg"], texts=[], args={"circle": True})

    with open("result.gif", "wb") as f:
        f.write(result.getvalue())
"""

if __name__ == "__main__":
    main()