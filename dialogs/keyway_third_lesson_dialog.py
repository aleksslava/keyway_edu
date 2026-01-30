import operator
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Column, Multiselect, Group, Start, Back, Row, Cancel, Next, \
    ManagedMultiselect, Radio, ManagedRadio
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from fsm_forms.fsm_models import KeywayThirdLessonDialog
from aiogram.enums import ContentType
from aiogram_dialog.widgets.media import StaticMedia
from config.config import BASE_DIR
from service.questions_lexicon import questions_2 as questions
from service.service import pad_right, format_results, format_progress


# Геттер для вопросов
async def question_answers(dialog_manager: DialogManager, **kwargs):
    current_state = dialog_manager.current_context().state.state
    question_answers = questions.get(current_state).get("answers")
    title = questions.get(current_state).get("title")
    key = questions.get(current_state).get("key")
    dialog_manager.dialog_data[f"{key}_items"] = question_answers

    text_answers = 'Варианты ответов:\n'
    for index, item in enumerate(question_answers, start=1):
        text_answers += f'{index}) {item[0]}\n'

    max_answer_len = len(max(map(lambda x: x[0], question_answers), key=len))
    question_answers = [
        (pad_right(title, max_answer_len), opt_id, is_correct)
        for title, opt_id, is_correct in question_answers
    ]

    return {"question_answers": question_answers,
            "title": title,
            'quest_number': key[1:],
            'text_answers': text_answers}


# Хендлер для multiselect ответов
async def multiselect_question_answers_checked(
    event: CallbackQuery,
    widget: ManagedMultiselect,
    dialog_manager: DialogManager,
    item_id: str,
):
    checked_ids = set(widget.get_checked())
    state = dialog_manager.current_context().state.state
    key = questions.get(state).get("key")
    # (title, id, should_be_selected)
    items = dialog_manager.dialog_data.get(f"{key}_items", [])

    # Считаем "правильность" по каждому варианту
    per_option_result = {}
    for title, opt_id, should_be_selected in items:
        user_selected = opt_id in checked_ids
        per_option_result[title] = (user_selected == should_be_selected)

    # Записываем в нужном формате
    dialog_manager.dialog_data.setdefault("answers", {})
    dialog_manager.dialog_data["answers"][f"{key}"] = per_option_result

# Хендлер для radio вопросов
async def radio_question_answers_checked(
    event: CallbackQuery,
    widget: ManagedRadio,
    dialog_manager: DialogManager,
    item_id: str,
):
    checked_id = widget.get_checked()
    state = dialog_manager.current_context().state.state
    key = questions.get(state).get("key")
    # (title, id, should_be_selected)
    items = dialog_manager.dialog_data.get(f"{key}_items", [])

    # Считаем "правильность" по каждому варианту
    per_option_result = {}
    for title, opt_id, should_be_selected in items:
        user_selected = checked_id == opt_id
        per_option_result[title] = (user_selected == should_be_selected)

    # Записываем в нужном формате
    dialog_manager.dialog_data.setdefault("answers", {})
    dialog_manager.dialog_data["answers"][f"{key}"] = per_option_result


vebinar_1 = Window(
    Const(text="Запись второго вебинара по обучению Keyway"),
    StaticMedia(
        path=BASE_DIR / "media" / "video" / "vebinar_keyway_2.mp4",
        type=ContentType.VIDEO,
        media_params={"supports_streaming": True},
    ),
    Group(
        Row(
            Cancel(Const('Назад'), id='go_cancel_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        ))
    ,
    state=KeywayThirdLessonDialog.vebinar_1,
    )


first_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='first_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=multiselect_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.first_question,
    getter=question_answers
    )


second_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='second_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.second_question,
    getter=question_answers
    )

third_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='third_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.third_question,
    getter=question_answers
    )


fourth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='fourth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.fourth_question,
    getter=question_answers
    )

fifth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('️◻️ {item[0]}'),
                id='fifth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.fifth_question,
    getter=question_answers
    )

sixth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='sixth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.sixth_question,
    getter=question_answers
    )

seventh_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='seventh_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=multiselect_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.seventh_question,
    getter=question_answers
    )

eighth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('️◻️ {item[0]}'),
                id='eighth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.eighth_question,
    getter=question_answers
    )

ninth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='ninth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.ninth_question,
    getter=question_answers
    )

tenth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='tenth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.tenth_question,
    getter=question_answers
    )

eleventh_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='eleventh_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.eleventh_question,
    getter=question_answers
    )

twelth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='twelth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=multiselect_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.twelth_question,
    getter=question_answers
    )

thirteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='thirteth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.thirteth_question,
    getter=question_answers
    )

fourteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='fourteth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.fourteth_question,
    getter=question_answers
    )

fifteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='fifteth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.fifteth_question,
    getter=question_answers
    )

sixteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='sixteth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.sixteth_question,
    getter=question_answers
    )

seventeth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
                id='seventeth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.seventeth_question,
    getter=question_answers
    )

eighteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('️◻️ {item[0]}'),
                id='eighteth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayThirdLessonDialog.eighteth_question,
    getter=question_answers
    )

async def confirm_answers_getter(dialog_manager: DialogManager, **kwargs):
    first_lesson_answers = dialog_manager.dialog_data.get('answers')
    message = format_progress(first_lesson_answers, total_questions=18)
    return {'message': message}

confirm_answers = Window(
    Format(text='{message}'),
    Back(Const('Назад'), id='go_back_dialog'),
    Next(Const('Отправить на проверку'), id='go_next_dialog'),
    state = KeywayThirdLessonDialog.confirm_answers,
    getter=confirm_answers_getter
)

async def result_getter(dialog_manager: DialogManager, **kwargs):
    second_lesson_result = dialog_manager.dialog_data.get('answers')
    result = format_results(second_lesson_result, total_questions=18)
    return {'result': result}

result = Window(
    Const(text='Ваши результаты прохождения первого урока:'),
    Format(text="{result}"),
    Cancel(Const('К списку уроков'), id='cancel'),
    state=KeywayThirdLessonDialog.result_third_lesson,
    getter=result_getter
)

keyway_third_lesson_dialog = Dialog(vebinar_1, first_question, second_question, third_question, fourth_question,
                                    fifth_question, sixth_question, seventh_question, eighth_question, ninth_question,
                                    tenth_question, eleventh_question, twelth_question, thirteth_question,
                                    fourteth_question, fifteth_question, sixteth_question, seventeth_question,
                                    eighteth_question, result)