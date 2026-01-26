from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from fsm_forms.fsm_models import MainDialog, KeywayFirstLessonDialog, KeywaySecondLessonDialog, KeywayThirdLessonDialog
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def keyway_edu_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()

async def main_menu_getter(dialog_manager: DialogManager, **kwargs):
    user_authorized = dialog_manager.dialog_data.get("user_authorized", False)
    button_to_authorized = dialog_manager.dialog_data.get("button_to_authorized", True)
    return {'user_authorized': user_authorized,
            'button_to_authorized': button_to_authorized}


async def send_contact_keyboard(cq, _, dialog_manager):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Поделиться номером", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    # отправляем отдельным сообщением, т.к. aiogram-dialog работает с inline-клавиатурами
    msg = await cq.message.answer("-", reply_markup=kb)
    dialog_manager.dialog_data["contact_kb_msg_id"] = msg.message_id
    await dialog_manager.switch_to(MainDialog.phone)


# Стартовое меню бота
main_window = Window(
    Const("Добро пожаловать в обучение по умным замкам Keyway.\nВыберите необходимый пункт меню!",
          when="user_authorized"),
    Const("Для доступа к обучению, нажмите на кнопку авторизоваться и поделитесь номером телефона!",
          when="button_to_authorized"),
    Column(
        Button(Const("Обучение"),
               id="1",
               on_click=keyway_edu_menu,
               when="user_authorized"),
        Button(Const("Прогресс обучения"),
               id="2",
               on_click=None,
               when="user_authorized"),
        Button(Const("Авторизация"),
               id="3",
               on_click=send_contact_keyboard,
               when='button_to_authorized'),
    ),
    state=MainDialog.main,
    getter=main_menu_getter
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
async def on_contact(message: Message, _, dialog_manager):
    user_authorized = not dialog_manager.dialog_data.get("user_authorized", False)
    button_to_authorized = not dialog_manager.dialog_data.get("button_to_authorized", True)
    await message.answer("Спасибо! Номер получен ✅", reply_markup=ReplyKeyboardRemove())
    dialog_manager.dialog_data.update(user_authorized=user_authorized, button_to_authorized=button_to_authorized)
    await dialog_manager.switch_to(MainDialog.main)

phone = Window(
        Const("Отправь контакт кнопкой на клавиатуре ниже."),
        MessageInput(on_contact, ContentType.CONTACT),
        state=MainDialog.phone,
    )


main_menu_dialog = Dialog(main_window, keyway_lessons, phone)