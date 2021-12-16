import random
import requests as requests
from HW8_var.question import Question


def get_authors_list(file_):
    """
    :param file_: файл со списком авторов
    :return: список авторов вопросов
    """
    list_ = []
    with open(file_, 'r', encoding="UTF-8") as file:
        for line in file:
            list_.append(line.rstrip())
        return list_


authors = get_authors_list("authors.txt")  # Список авторов вопросов


def read_file(url):
    list_ = []  # Список вопросов

    response = requests.get(url)
    questions_dict = response.json()

    for key, value in questions_dict.items():
        for i in value.keys():
            random.shuffle(authors)
            list_.append(Question(question_text=value[i]["question"], question_author=authors[0],
                                  question_complexity=i, correct_answers=value[i]["answer"], question_theme=key, ))
    return list_


def get_results(list_):
    """
    Обработка статистики на основе списка вопросов
    :param list_: список вопросов
    """
    stats = {
        "total_questions": 0,
        "correct": 0,
        "total_score": 0,
    }

    for i in list_:
        if i.is_question_asked:
            stats["total_questions"] += 1
            if i.is_users_answer_correct:
                stats["total_score"] += i.question_score
                stats["correct"] += 1

    if stats["correct"] == 1:
        end = ' '
    elif stats["correct"] in [2, 3, 4]:
        end = 'а '
    else:
        end = 'ов '

    print(f"Вот и всё!\nОтвечено {stats['correct']} вопрос{end}из {stats['total_questions']}\n"
          f"Вы заработали {stats['total_score']} баллов")


questions = read_file("https://jsonkeeper.com/b/K6GK")
random.shuffle(questions)

for question in questions:

    if not question.is_question_asked:
        question.build_question(question.get_complexity_level(), (questions.index(question) + 1))
        users_answer = input()
        if users_answer.lower() == "stop":
            break
        question.users_answer = users_answer
        question.is_question_asked = True

        if question.is_correct():
            print(f"Верно! Вы заработали {question.question_score} баллов\n")
            question.is_users_answer_correct = True

        else:
            print(f"Ответ неверный. Верный ответ – {question.correct_answers[0]}\n")

get_results(questions)
