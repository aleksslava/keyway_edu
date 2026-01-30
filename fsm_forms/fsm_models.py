from aiogram.filters.state import StatesGroup, State



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
    confirm_answers = State()
    result_first_lesson = State()



class KeywaySecondLessonDialog(StatesGroup):
    vebinar_1 = State()
    vebinar_2 = State()
    vebinar_3 = State()
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
    confirm_answers = State()
    result_second_lesson = State()




class KeywayThirdLessonDialog(StatesGroup):
    vebinar_1 = State()
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
    confirm_answers = State()
    result_third_lesson = State()

