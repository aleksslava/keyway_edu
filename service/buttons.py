from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Column, Row, Group, Start, Back, Next, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const
from dialogs.main_dialog import MainDialog

# async def start_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.start(MainDialog.main)
#
# async def next_stack(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.next()
#
# async def back_stack(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.back()

base_menu = Group(
    Start(Const('В главное меню'), id='go_main_menu', state=MainDialog.main),
    Row(
        Back(Const('Назад'), id='go_back_dialog', when='back_state'),
        Cancel(Const('Назад'), id='go_cancel_dialog', when='first_state'),
        Next(Const('Вперед'), id='go_next_dialog'),
    ))