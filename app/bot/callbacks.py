from aiogram.filters.callback_data import CallbackData


class TaskAction(CallbackData, prefix="task"):
    """CallbackData для действий над задачей.
    Используется в inline-кнопках для передачи
    действия и идентификатора задачи.
    """

    action: str
    task_id: int


class EditField(CallbackData, prefix="edit"):
    """CallbackData для выбора поля редактирования задачи.
    Используется в FSM-сценарии редактирования задачи."""

    field: str  # title | description
