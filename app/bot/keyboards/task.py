from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.callbacks import TaskAction


def task_keyboard(task_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔍 View",
                    callback_data=TaskAction(
                        action="view",
                        task_id=task_id,
                    ).pack()
                ),
                InlineKeyboardButton(
                    text="✏️ Edit",
                    callback_data=TaskAction(
                        action="edit",
                        task_id=task_id,
                    ).pack()
                ),
                InlineKeyboardButton(
                    text="✅ Done",
                    callback_data=TaskAction(
                        action="done",
                        task_id=task_id,
                    ).pack()
                ),
                InlineKeyboardButton(
                    text="🗑 Delete",
                    callback_data=TaskAction(
                        action="delete",
                        task_id=task_id,
                    ).pack()
                ),
            ]
        ]
    )