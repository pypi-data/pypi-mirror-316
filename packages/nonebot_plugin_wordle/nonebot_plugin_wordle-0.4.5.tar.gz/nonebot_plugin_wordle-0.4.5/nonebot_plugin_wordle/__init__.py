import asyncio
from asyncio import TimerHandle
from typing import Annotated, Any

from nonebot import on_regex, require
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import Depends, EventToMe, RegexDict
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.utils import run_sync

require("nonebot_plugin_alconna")
require("nonebot_plugin_uninfo")

from nonebot_plugin_alconna import (
    AlcMatches,
    Alconna,
    AlconnaQuery,
    Args,
    At,
    Image,
    Option,
    Query,
    Text,
    UniMessage,
    on_alconna,
)
from nonebot_plugin_uninfo import Uninfo

from .data_source import GuessResult, Wordle
from .utils import dic_list, random_word

__plugin_meta__ = PluginMetadata(
    name="猜单词",
    description="wordle猜单词游戏",
    usage=(
        "@我 + “猜单词”开始游戏；\n"
        "答案为指定长度单词，发送对应长度单词即可；\n"
        "绿色块代表此单词中有此字母且位置正确；\n"
        "黄色块代表此单词中有此字母，但该字母所处位置不对；\n"
        "灰色块代表此单词中没有此字母；\n"
        "猜出单词或用光次数则游戏结束；\n"
        "发送“结束”结束游戏；发送“提示”查看提示；\n"
        "可使用 -l/--length 指定单词长度，默认为5；\n"
        "可使用 -d/--dictionary 指定词典，默认为CET4\n"
        f"支持的词典：{'、'.join(dic_list)}"
    ),
    type="application",
    homepage="https://github.com/noneplugin/nonebot-plugin-wordle",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", "nonebot_plugin_uninfo"
    ),
)


games: dict[str, Wordle] = {}
timers: dict[str, TimerHandle] = {}


def get_user_id(uninfo: Uninfo) -> str:
    return f"{uninfo.scope}_{uninfo.self_id}_{uninfo.scene_path}"


UserId = Annotated[str, Depends(get_user_id)]


def game_is_running(user_id: UserId) -> bool:
    return user_id in games


def game_not_running(user_id: UserId) -> bool:
    return user_id not in games


def same_user(game_user_id: str):
    def _same_user(user_id: UserId) -> bool:
        return user_id in games and user_id == game_user_id

    return _same_user


wordle_alc = Alconna(
    "wordle",
    Option("-l|--length", Args["length", int], help_text="单词长度"),
    Option("-d|--dictionary", Args["dictionary", str], help_text="词典"),
)

matcher_wordle = on_alconna(
    wordle_alc,
    aliases=("猜单词",),
    rule=game_not_running,
    use_cmd_start=True,
    block=True,
    priority=13,
)
matcher_hint = on_alconna(
    "wordle_hint",
    aliases=("提示", "猜单词提示"),
    rule=game_is_running,
    use_cmd_start=True,
    block=True,
    priority=13,
)
matcher_stop = on_alconna(
    "wordle_stop",
    aliases=("结束", "结束游戏", "结束猜单词"),
    rule=game_is_running,
    use_cmd_start=True,
    block=True,
    priority=13,
)
matchers_word: dict[str, type[Matcher]] = {}


def stop_game(user_id: str):
    if timer := timers.pop(user_id, None):
        timer.cancel()
    games.pop(user_id, None)
    if matcher := matchers_word.pop(user_id, None):
        matcher.destroy()


async def stop_game_timeout(matcher: Matcher, user_id: str):
    game = games.get(user_id, None)
    stop_game(user_id)
    if game:
        msg = "猜单词超时，游戏结束"
        if len(game.guessed_words) >= 1:
            msg += f"\n{game.result}"
        await matcher.send(msg)


def set_timeout(matcher: Matcher, user_id: str, timeout: float = 300):
    if timer := timers.get(user_id, None):
        timer.cancel()
    loop = asyncio.get_running_loop()
    timer = loop.call_later(
        timeout, lambda: asyncio.ensure_future(stop_game_timeout(matcher, user_id))
    )
    timers[user_id] = timer


@matcher_wordle.handle()
async def _(
    matcher: Matcher,
    user_id: UserId,
    alc_matches: AlcMatches,
    to_me: bool = EventToMe(),
    length: Query[int] = AlconnaQuery("length", 5),
    dictionary: Query[str] = AlconnaQuery("dictionary", "CET4"),
):
    header_match = str(alc_matches.header_match.result)
    command = str(wordle_alc.command)
    if not (to_me or bool(header_match.rstrip(command))):
        logger.debug("Not to me, ignore")
        matcher.block = False
        await matcher.finish()

    if length.result < 3 or length.result > 8:
        await matcher.finish("单词长度应在3~8之间")

    if dictionary.result not in dic_list:
        await matcher.finish("支持的词典：" + ", ".join(dic_list))

    word, meaning = random_word(dictionary.result, length.result)
    game = Wordle(word, meaning)

    games[user_id] = game
    set_timeout(matcher, user_id)
    matcher_word = on_regex(
        rf"^(?P<word>[a-zA-Z]{{{length.result}}})$",
        rule=same_user(user_id),
        block=True,
        priority=14,
    )
    matcher_word.append_handler(handle_word)
    matchers_word[user_id] = matcher_word

    msg = Text(
        f"你有{game.rows}次机会猜出单词，单词长度为{game.length}，请发送单词"
    ) + Image(raw=await run_sync(game.draw)())
    await msg.send()


@matcher_hint.handle()
async def _(matcher: Matcher, user_id: UserId):
    game = games[user_id]
    set_timeout(matcher, user_id)

    hint = game.get_hint()
    if not hint.replace("*", ""):
        await matcher.finish("你还没有猜对过一个字母哦~再猜猜吧~")

    await UniMessage.image(raw=await run_sync(game.draw_hint)(hint)).send()


@matcher_stop.handle()
async def _(matcher: Matcher, user_id: UserId):
    game = games[user_id]
    stop_game(user_id)

    msg = "游戏已结束"
    if len(game.guessed_words) >= 1:
        msg += f"\n{game.result}"
    await matcher.finish(msg)


async def handle_word(
    matcher: Matcher,
    uninfo: Uninfo,
    user_id: UserId,
    matched: dict[str, Any] = RegexDict(),
):
    game = games[user_id]
    set_timeout(matcher, user_id)

    word = str(matched["word"])
    result = game.guess(word)

    if result in [GuessResult.WIN, GuessResult.LOSS]:
        stop_game(user_id)

        await (
            UniMessage.template(
                (
                    "恭喜{user}猜出了单词！"
                    if result == GuessResult.WIN
                    else "很遗憾，没有人猜出来呢"
                )
                + "\n{result}\n{image}"
            )
            .format(
                user="你" if uninfo.scene.is_private else At("user", uninfo.user.id),
                result=game.result,
                image=Image(raw=await run_sync(game.draw)()),
            )
            .send()
        )

    elif result == GuessResult.DUPLICATE:
        await matcher.finish("你已经猜过这个单词了呢")

    elif result == GuessResult.ILLEGAL:
        await matcher.finish(f"你确定 {word} 是一个合法的单词吗？")

    else:
        await UniMessage.image(raw=await run_sync(game.draw)()).send()
