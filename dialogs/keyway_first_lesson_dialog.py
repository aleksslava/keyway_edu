from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from fsm_forms.fsm_models import MainDialog, KeywayFirstLessonDialog, KeywaySecondLessonDialog, KeywayThirdLessonDialog
from aiogram.enums import ContentType
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram_dialog.api.entities import MediaAttachment
from config.config import BASE_DIR

async def first_vebinar_video_getter(**kwargs):
    video = MediaAttachment(type=ContentType.VIDEO, path= BASE_DIR / "media" / "video" / "vebinar_keyway_1.mov")
    return {'video': video}

vebinar = Window(
    Const(text="Запись первого вебинара по обучению Keyway"),
    DynamicMedia('video'),
    getter=first_vebinar_video_getter,
    state=KeywayFirstLessonDialog.vebinar
    )



keyway_first_lesson_dialog = Dialog(vebinar)