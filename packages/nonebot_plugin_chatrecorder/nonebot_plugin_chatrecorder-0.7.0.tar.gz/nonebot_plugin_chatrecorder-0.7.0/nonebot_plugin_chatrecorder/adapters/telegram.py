from datetime import datetime, timezone
from typing import Any, Optional

from nonebot.adapters import Bot as BaseBot
from nonebot.compat import type_validate_python
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
    from nonebot.adapters.telegram import Bot, Message
    from nonebot.adapters.telegram.event import MessageEvent
    from nonebot.adapters.telegram.model import Message as TGMessage

    adapter = SupportAdapter.telegram

    @event_postprocessor
    async def record_recv_msg(event: MessageEvent, session: Uninfo):
        session_persist_id = await get_session_persist_id(session)

        record = MessageRecord(
            session_persist_id=session_persist_id,
            time=remove_timezone(datetime.fromtimestamp(event.date, timezone.utc)),
            type=record_type(event),
            message_id=f"{event.chat.id}_{event.message_id}",
            message=serialize_message(adapter, event.get_message()),
            plain_text=event.get_plaintext(),
        )
        async with get_session() as db_session:
            db_session.add(record)
            await db_session.commit()

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

            if api in [
                "send_message",
                "send_photo",
                "send_audio",
                "send_document",
                "send_video",
                "send_animation",
                "send_voice",
                "send_video_note",
                "send_location",
                "send_venue",
                "send_contact",
                "send_poll",
                "send_dice",
                "send_sticker",
                "send_invoice",
            ]:
                tg_message = type_validate_python(TGMessage, result)
                chat = tg_message.chat
                message_id = f"{chat.id}_{tg_message.message_id}"
                message = Message.model_validate(result)

            elif api == "send_media_group":
                tg_messages = [type_validate_python(TGMessage, res) for res in result]
                tg_message = tg_messages[0]
                chat = tg_message.chat
                message_id = "_".join([str(msg.message_id) for msg in tg_messages])
                message_id = f"{chat.id}_{message_id}"
                message = Message()
                for res in result:
                    message += Message.model_validate(res)

            else:
                return

            message_thread_id = tg_message.message_thread_id
            chat_id = tg_message.chat.id
            parent = None
            if message_thread_id:
                scene_type = SceneType.CHANNEL_TEXT
                scene_id = str(message_thread_id)
                parent = Scene(id=str(chat_id), type=SceneType.GUILD)
            elif chat.type == "private":
                scene_type = SceneType.PRIVATE
                scene_id = str(chat_id)
            else:
                scene_type = SceneType.GROUP
                scene_id = str(chat_id)

            session = Session(
                self_id=bot.self_id,
                adapter=adapter,
                scope=SupportScope.telegram,
                scene=Scene(id=scene_id, type=scene_type, parent=parent),
                user=User(id=bot.self_id),
            )
            session_persist_id = await get_session_persist_id(session)

            record = MessageRecord(
                session_persist_id=session_persist_id,
                time=remove_timezone(
                    datetime.fromtimestamp(tg_message.date, timezone.utc)
                ),
                type="message_sent",
                message_id=message_id,
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
