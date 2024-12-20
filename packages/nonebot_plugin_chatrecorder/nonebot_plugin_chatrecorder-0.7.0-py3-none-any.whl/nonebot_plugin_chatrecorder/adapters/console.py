import uuid
from dataclasses import asdict
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
    from nonebot.adapters.console import Bot, Message, MessageEvent, MessageSegment
    from nonechat import ConsoleMessage, Emoji, Text

    adapter = SupportAdapter.console

    def get_id() -> str:
        return uuid.uuid4().hex

    @event_postprocessor
    async def record_recv_msg(event: MessageEvent, session: Uninfo):
        session_persist_id = await get_session_persist_id(session)

        record = MessageRecord(
            session_persist_id=session_persist_id,
            time=remove_timezone(event.time.astimezone(timezone.utc)),
            type=record_type(event),
            message_id=get_id(),
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
            if e or api not in ["send_msg"]:
                return

            session = Session(
                self_id=bot.self_id,
                adapter=adapter,
                scope=SupportScope.console,
                scene=Scene(id=data["user_id"], type=SceneType.PRIVATE),
                user=User(id=bot.self_id),
            )
            session_persist_id = await get_session_persist_id(session)

            elements = ConsoleMessage(data["message"])
            message = Message()
            for elem in elements:
                if isinstance(elem, Text):
                    message += MessageSegment.text(elem.text)
                elif isinstance(elem, Emoji):
                    message += MessageSegment.emoji(elem.name)
                else:
                    message += MessageSegment(
                        type=elem.__class__.__name__.lower(),
                        data=asdict(elem),  # type: ignore
                    )

            record = MessageRecord(
                session_persist_id=session_persist_id,
                time=remove_timezone(datetime.now(timezone.utc)),
                type="message_sent",
                message_id=get_id(),
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
