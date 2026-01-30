def pad_right(s: str, width: int) -> str:
    # обычные пробелы иногда “съедаются”/выглядят странно в кнопках,
    # поэтому лучше NBSP (неразрывный пробел)
    return s + ("\u2800" * 50)

def format_results(answers: dict, total_questions: int) -> str:
    def q_num(q_key: str) -> int:
        return int(q_key[1:])  # 'q10' -> 10

    lines = []
    correct_cnt = 0

    for n in range(1, total_questions + 1):
        q_key = f"q{n}"

        # пропущенный вопрос = неверно
        if q_key not in answers or not isinstance(answers.get(q_key), dict) or not answers[q_key]:
            is_correct = False
        else:
            is_correct = all(answers[q_key].values())

        if is_correct:
            correct_cnt += 1

        status = "Верно" if is_correct else "Не верно"
        lines.append(f"Вопрос {n} - {status};")

    percent = round((correct_cnt / total_questions) * 100, 1) if total_questions else 0.0
    passed = percent > 80  # строго "более 80", как ты написал

    lines.append("")
    lines.append(f"Верных ответов: {correct_cnt}/{total_questions} ({percent}%)")
    lines.append("Урок пройден ✅" if passed else "Урок не пройден ❌")

    return "\n".join(lines)


def format_progress(answers: dict, total_questions: int) -> str:
    """
    answers: {'q1': {'вариант': True/False, ...}, ...}
    total_questions: общее число вопросов (например 23)

    Отвечен, если есть хотя бы один True.
    Пропущен, если:
      - нет ключа qN
      - или answers[qN] пустой/не dict
      - или все значения False
    """
    answered_nums = []
    missed_nums = []

    for n in range(1, total_questions + 1):
        q_key = f"q{n}"
        q_data = answers.get(q_key)

        if not isinstance(q_data, dict) or not q_data:
            missed_nums.append(n)
            continue

        has_selection = any(bool(v) for v in q_data.values())
        (answered_nums if has_selection else missed_nums).append(n)

    answered_cnt = len(answered_nums)
    missed_cnt = len(missed_nums)

    def fmt_nums(nums: list[int]) -> str:
        return ", ".join(map(str, nums)) if nums else "—"

    lines = [
        "🧾 Прогресс перед проверкой:",
        f"✅ Отвечено: {answered_cnt}/{total_questions}",
        f"⏭️ Пропущено: {missed_cnt}/{total_questions}",
        "",
        f"✅ Вопросы с ответами: {fmt_nums(answered_nums)}",
        f"⏭️ Пропущенные вопросы: {fmt_nums(missed_nums)}",
    ]

    # если есть пропуски — мягкий призыв
    if missed_nums:
        lines.append("")
        lines.append("Можно вернуться и ответить на пропущенные, или отправить как есть на проверку.")

    return "\n".join(lines)

