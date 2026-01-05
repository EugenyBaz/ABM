from aiogram.types import Message
from app.schemas.marketing import MarketingAttachment


async def extract_attachments(message: Message) -> list[MarketingAttachment]:
    attachments: list[MarketingAttachment] = []
    bot = message.bot

    # 📄 Documents (pdf, xlsx, docx, etc.)
    if message.document:
        file = await bot.get_file(message.document.file_id)
        buffer = await bot.download_file(file.file_path)

        attachments.append(
            MarketingAttachment(
                filename=message.document.file_name,
                content=buffer.read(),
                mime_type=message.document.mime_type
                or "application/octet-stream",
            )
        )

    # 🖼 Photos (берём самое большое)
    if message.photo:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        buffer = await bot.download_file(file.file_path)

        attachments.append(
            MarketingAttachment(
                filename=f"photo_{photo.file_id}.jpg",
                content=buffer.read(),
                mime_type="image/jpeg",
            )
        )

    # 🎥 Video
    if message.video:
        file = await bot.get_file(message.video.file_id)
        buffer = await bot.download_file(file.file_path)

        attachments.append(
            MarketingAttachment(
                filename=message.video.file_name or "video.mp4",
                content=buffer.read(),
                mime_type=message.video.mime_type or "video/mp4",
            )
        )

    return attachments