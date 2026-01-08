from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks import EditField


def edit_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Заголовок",
                    callback_data=EditField(field="title").pack(),
                ),
                InlineKeyboardButton(
                    text="📄 Описание",
                    callback_data=EditField(field="description").pack(),
                ),
            ]
        ]
    )
