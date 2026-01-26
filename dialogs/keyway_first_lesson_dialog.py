import operator
from pprint import pprint

from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Column, Multiselect, Group, Start, Back, Row, Cancel, Next, \
    ManagedMultiselect, Radio, ManagedRadio
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from fsm_forms.fsm_models import MainDialog, KeywayFirstLessonDialog, KeywaySecondLessonDialog, KeywayThirdLessonDialog
from aiogram.enums import ContentType
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram_dialog.api.entities import MediaAttachment
from config.config import BASE_DIR
from service.questions_lexicon import questions
from service.service import pad_right, format_results


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

# Сообщение с вебинаром первого урока Keyway
vebinar = Window(
    Const(text="Запись первого вебинара по обучению Keyway"),
    StaticMedia(
        path=BASE_DIR / "media" / "video" / "vebinar_keyway_1.mp4",
        type=ContentType.VIDEO,
        media_params={"supports_streaming": True},
    ),
    Group(
        Row(
            Cancel(Const('Назад'), id='go_cancel_dialog'),
            Next(Const('К первому вопросу'), id='go_next_dialog'),
        ))
    ,
    state=KeywayFirstLessonDialog.vebinar,
    )


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




first_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('[ ] {item[0]}'),
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
    state=KeywayFirstLessonDialog.first_question,
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
    state=KeywayFirstLessonDialog.second_question,
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
    state=KeywayFirstLessonDialog.third_question,
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
    state=KeywayFirstLessonDialog.fourth_question,
    getter=question_answers
    )

fifth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
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
    state=KeywayFirstLessonDialog.fifth_question,
    getter=question_answers
    )

sixth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
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
    state=KeywayFirstLessonDialog.sixth_question,
    getter=question_answers
    )

seventh_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('[ ] {item[0]}'),
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
    state=KeywayFirstLessonDialog.seventh_question,
    getter=question_answers
    )

eighth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
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
    state=KeywayFirstLessonDialog.eighth_question,
    getter=question_answers
    )

ninth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
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
    state=KeywayFirstLessonDialog.ninth_question,
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
    state=KeywayFirstLessonDialog.tenth_question,
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
    state=KeywayFirstLessonDialog.eleventh_question,
    getter=question_answers
    )

twelth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('[ ] {item[0]}'),
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
    state=KeywayFirstLessonDialog.twelth_question,
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
    state=KeywayFirstLessonDialog.thirteth_question,
    getter=question_answers
    )

fourteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
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
    state=KeywayFirstLessonDialog.fourteth_question,
    getter=question_answers
    )

fifteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
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
    state=KeywayFirstLessonDialog.fifteth_question,
    getter=question_answers
    )

sixteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}\n\n{text_answers}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 Вариант {item[1]}'),
                unchecked_text=Format('⚪ Вариант {item[1]}'),
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
    state=KeywayFirstLessonDialog.sixteth_question,
    getter=question_answers
    )

seventeth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
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
    state=KeywayFirstLessonDialog.seventeth_question,
    getter=question_answers
    )

eighteth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
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
    state=KeywayFirstLessonDialog.eighteth_question,
    getter=question_answers
    )

nineteenth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='nineteenth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayFirstLessonDialog.nineteenth_question,
    getter=question_answers
    )

twentieth_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('[ ] {item[0]}'),
                id='twentieth_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=multiselect_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayFirstLessonDialog.twentieth_question,
    getter=question_answers
    )

twenty_first_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='twenty_first_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayFirstLessonDialog.twenty_first_question,
    getter=question_answers
    )

twenty_second_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='twenty_second_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayFirstLessonDialog.twenty_second_question,
    getter=question_answers
    )

twenty_third_question = Window(
    Format(text="Вопрос #{quest_number}:\n\n{title}"),
    Group(
        Column(
            Radio(
                checked_text=Format('🟢 {item[0]}'),
                unchecked_text=Format('⚪ {item[0]}'),
                id='twenty_third_question_answers_checked',
                item_id_getter=operator.itemgetter(1),
                items="question_answers",
                on_state_changed=radio_question_answers_checked,
            )),
        Row(
            Back(Const('Назад'), id='go_back_dialog'),
            Next(Const('Вперед'), id='go_next_dialog'),
        )
    ),
    state=KeywayFirstLessonDialog.twenty_third_question,
    getter=question_answers
    )

async def result_getter(dialog_manager: DialogManager, **kwargs):
    first_lesson_result = dialog_manager.dialog_data.get('answers')
    result = format_results(first_lesson_result, total_questions=23)
    return {'result': result}

result = Window(
    Const(text='Ваши результаты прохождения первого урока:'),
    Format(text="{result}"),
    Cancel(Const('К списку уроков'), id='cancel'),
    state=KeywayFirstLessonDialog.result_first_lesson,
    getter=result_getter
)

keyway_first_lesson_dialog = Dialog(vebinar, first_question, second_question, third_question, fourth_question,
                                    fifth_question, sixth_question, seventh_question, eighth_question, ninth_question,
                                    tenth_question, eleventh_question, twelth_question, thirteth_question,
                                    fourteth_question, fifteth_question, sixteth_question, seventeth_question,
                                    eighteth_question, nineteenth_question, twentieth_question,
                                    twenty_first_question, twenty_second_question, twenty_third_question, result)