from aiogram.filters.callback_data import CallbackData


class TaskAction(CallbackData, prefix="task"):
    action: str
    task_id: int


class EditField(CallbackData, prefix="edit"):
    field: str   # title | description