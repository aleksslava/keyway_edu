from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog, Window, DialogManager, StartMode


class MainDialog(StatesGroup):
    main = State()
    keyway_lessons = State()
    phone = State()


class KeywayFirstLessonDialog(StatesGroup):
    vebinar = State()
    first_question = State()
    second_question = State()
    third_question = State()
    fourth_question = State()
    fifth_question = State()
    sixth_question = State()
    seventh_question = State()
    eighth_question = State()
    ninth_question = State()
    tenth_question = State()
    eleventh_question = State()
    twelth_question = State()
    thirteth_question = State()
    fourteth_question = State()
    fifteth_question = State()
    sixteth_question = State()
    seventeth_question = State()
    eighteth_question = State()
    nineteenth_question = State()
    twentieth_question = State()
    twenty_first_question = State()
    twenty_second_question = State()
    twenty_third_question = State()
    result_first_lesson = State()



class KeywaySecondLessonDialog(StatesGroup):
    vebinar = State()
    first_question = State()
    second_question = State()
    third_question = State()
    fourth_question = State()
    fifth_question = State()
    sixth_question = State()
    seventh_question = State()
    eighth_question = State()
    ninth_question = State()
    tenth_question = State()
    eleventh_question = State()
    twelth_question = State()
    thirteth_question = State()
    fourteth_question = State()
    fifteth_question = State()
    sixteth_question = State()
    seventeth_question = State()
    eighteth_question = State()




class KeywayThirdLessonDialog(StatesGroup):
    vebinar = State()
    first_question = State()
    second_question = State()
    third_question = State()
    fourth_question = State()
    fifth_question = State()
    sixth_question = State()
    seventh_question = State()
    eighth_question = State()
    ninth_question = State()
    tenth_question = State()
    eleventh_question = State()
    twelth_question = State()
    thirteth_question = State()
    fourteth_question = State()
    fifteth_question = State()
    sixteth_question = State()
    seventeth_question = State()
    eighteth_question = State()