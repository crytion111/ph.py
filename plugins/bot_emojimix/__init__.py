
__doc__ = """emoji合成
使用举例：发送 🥳+👑

发送 emoji合成 获取帮助
"""

from botoy import GroupMsg, S, jconfig
from botoy.decorators import equal_content, ignore_botself, on_regexp

try:
    from .emojimix import help, mix_emoji
except ImportError:
    from emojimix import help, mix_emoji


@on_regexp(r"^([\u200d-\U0001fab5]+)\+([\u200d-\U0001fab5]+)$")
def process_emoji(ctx: GroupMsg):
    emoji_1, emoji_2 = ctx._match[1], ctx._match[2]

    data = None

    for i in ((emoji_1, emoji_2), (emoji_2, emoji_1)):

        ret = mix_emoji(*i)
        if ret:
            data = ret
            break

    if data:
        S.image(data, text ="合成成功")


@on_regexp(r"^([\u200d-\U0001fab5]+)([\u200d-\U0001fab5]+)$")
def process_emoji2(ctx: GroupMsg):
    emoji_1, emoji_2 = ctx._match[1], ctx._match[2]

    data = None

    for i in ((emoji_1, emoji_2), (emoji_2, emoji_1)):

        ret = mix_emoji(*i)
        if ret:
            data = ret
            break

    if data:
        S.image(data, text ="合成成功")



@equal_content('emoji合成')
def process_help(_):
    S.text(help())


@ignore_botself
def receive_group_msg(ctx:GroupMsg):
    process_help(ctx)
    if ctx.FromUserId == jconfig.superAdmin:
        process_emoji(ctx)
        process_emoji2(ctx)

@ignore_botself
def receive_friend_msg(ctx):
    process_help(ctx)
    process_emoji(ctx)
    process_emoji2(ctx)
