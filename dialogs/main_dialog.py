from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from fsm_forms.fsm_models import MainDialog, KeywayFirstLessonDialog, KeywaySecondLessonDialog, KeywayThirdLessonDialog


async def keyway_edu_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()

# Стартовое меню бота
main_window = Window(
    Const("Добро пожаловать в обучение по умным замкам Keyway.\nВыберите необходимый пункт меню!"),
    Column(
        Button(Const("Обучение"),
               id="1",
               on_click=keyway_edu_menu),
        Button(Const("Пустой раздел"),
               id="2",
               on_click=None),
        Button(Const("Пустой раздел"),
               id="3",
               on_click=None),
    ),
    state=MainDialog.main,
    )

async def back_to_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(MainDialog.main, mode=StartMode.NORMAL)

async def first_lesson_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(KeywayFirstLessonDialog.vebinar, mode=StartMode.NORMAL)

async def second_lesson_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(KeywaySecondLessonDialog.vebinar, mode=StartMode.NORMAL)

async def third_lesson_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(KeywayThirdLessonDialog.vebinar, mode=StartMode.NORMAL)

# Меню с выбором урока Keyway
keyway_lessons = Window(
    Const("Выберите урок для прохождения.\nУроки становятся доступны после прохождения предыдущих."),
    Column(
        Button(Const("Первый урок"),
               id="1",
               on_click=first_lesson_start,),
        Button(Const("Второй урок"),
               id="2",
               on_click=second_lesson_start),
        Button(Const("Третий урок"),
               id="3",
               on_click=third_lesson_start),
    Button(Const("В главное меню"),
               id="4",
               on_click=back_to_main_menu),
    ),
    state=MainDialog.keyway_lessons,
    )

main_menu_dialog = Dialog(main_window, keyway_lessons)