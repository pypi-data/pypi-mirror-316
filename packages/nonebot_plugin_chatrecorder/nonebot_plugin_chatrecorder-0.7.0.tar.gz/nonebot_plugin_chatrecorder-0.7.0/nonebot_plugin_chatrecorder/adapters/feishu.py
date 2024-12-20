import re
from datetime import datetime, timezone
from typing import Any, Optional

from nonebot.adapters import Bot as BaseBot
from nonebot.message import event_postprocessor
from nonebot_plugin_orm import get_session
from nonebot_plugin_uninfo import (
    Scene,
    SceneType,
    Session,
    SupportAdapter,
    SupportScope,
    Uninfo,
    User,
)
from nonebot_plugin_uninfo.orm import get_session_persist_id
from typing_extensions import override

from ..config import plugin_config
from ..message import (
    MessageDeserializer,
    MessageSerializer,
    register_deserializer,
    register_serializer,
    serialize_message,
)
from ..model import MessageRecord
from ..utils import record_type, remove_timezone

try:
    from nonebot.adapters.feishu import Bot, Message, MessageEvent

    adapter = SupportAdapter.feishu

    @event_postprocessor
    async def record_recv_msg(event: MessageEvent, session: Uninfo):
        session_persist_id = await get_session_persist_id(session)

        record = MessageRecord(
            session_persist_id=session_persist_id,
            time=remove_timezone(
                datetime.fromtimestamp(
                    int(event.event.message.create_time) / 1000, timezone.utc
                )
            ),
            type=record_type(event),
            message_id=event.event.message.message_id,
            message=serialize_message(adapter, event.get_message()),
            plain_text=event.get_plaintext(),
        )
        async with get_session() as db_session:
            db_session.add(record)
            await db_session.commit()

    _chat_info_cache: dict[str, dict[str, Any]] = {}

    async def get_chat_info(bot: Bot, chat_id: str) -> dict[str, Any]:
        if chat_id in _chat_info_cache:
            return _chat_info_cache[chat_id]
        params = {"method": "GET", "query": {"user_id_type": "open_id"}}
        resp = await bot.call_api(f"im/v1/chats/{chat_id}", **params)
        _chat_info_cache[chat_id] = resp
        return resp

    if plugin_config.chatrecorder_record_send_msg:

        @Bot.on_called_api
        async def record_send_msg(
            bot: BaseBot,
            e: Optional[Exception],
            api: str,
            data: dict[str, Any],
            result: Any,
        ):
            if not isinstance(bot, Bot):
                return
            if e or not result:
                return

            if not (
                api == "im/v1/messages" or re.match(r"im/v1/messages/\S+/reply", api)
            ):
                return

            result_data = result["data"]
            chat_id = result_data["chat_id"]
            resp = await get_chat_info(bot, chat_id)
            chat_mode = resp["data"]["chat_mode"]

            if chat_mode == "p2p":
                scene_type = SceneType.PRIVATE
            elif chat_mode == "group":
                scene_type = SceneType.GROUP

            session = Session(
                self_id=bot.self_id,
                adapter=adapter,
                scope=SupportScope.feishu,
                scene=Scene(id=chat_id, type=scene_type),
                user=User(id=bot.self_id),
            )
            session_persist_id = await get_session_persist_id(session)

            msg_type = result_data["msg_type"]
            content = result_data["body"]["content"]
            mentions = result_data.get("mentions")
            message = Message.deserialize(content, mentions, msg_type)

            record = MessageRecord(
                session_persist_id=session_persist_id,
                time=remove_timezone(
                    datetime.fromtimestamp(
                        int(result_data["create_time"]) / 1000, timezone.utc
                    )
                ),
                type="message_sent",
                message_id=result_data["message_id"],
                message=serialize_message(adapter, message),
                plain_text=message.extract_plain_text(),
            )
            async with get_session() as db_session:
                db_session.add(record)
                await db_session.commit()

    class Serializer(MessageSerializer[Message]):
        pass

    class Deserializer(MessageDeserializer[Message]):
        @classmethod
        @override
        def get_message_class(cls) -> type[Message]:
            return Message

    register_serializer(adapter, Serializer)
    register_deserializer(adapter, Deserializer)

except ImportError:
    pass
