import http.server
import json
import random
import os
from urllib.parse import urlparse, parse_qs

DB_QUIZ = [
    {
        "q": "Как переводится идиома 'Piece of cake'?",
        "a": ["Проще простого", "Кусок торта", "Сладкая жизнь", "Рецепт успеха"],
        "c": 0,
    },
    {
        "q": "Что означает фраза 'Break a leg'?",
        "a": ["Сломать ногу", "Удачи", "Сильно устать", "Прекратить работу"],
        "c": 1,
    },
    {
        "q": "Как перевести 'Bite the bullet'?",
        "a": [
            "Укусить пулю",
            "Стиснуть зубы / решиться",
            "Разозлиться",
            "Опоздать",
        ],
        "c": 1,
    },
    {
        "q": "Что означает выражение 'Under the weather'?",
        "a": ["Плохо себя чувствовать", "Промокнуть под дождем", "Быть в хорошем настроении", "Иметь зонт"],
        "c": 0,
    },
    {
        "q": "Как переводится 'Spill the beans'?",
        "a": ["Рассыпать фасоль", "Приготовить ужин", "Выдать секрет", "Громко смеяться"],
        "c": 2,
    },
    {
        "q": "Что значит 'When pigs fly'?",
        "a": ["Когда рак на горе свистнет", "Очень скоро", "Взлететь от счастья", "Сделать глупость"],
        "c": 0,
    },
    {
        "q": "Как перевести идиому 'Cost an arm and a leg'?",
        "a": ["Стоить очень дорого", "Быть опасным", "Требовать усилий", "Окупиться со временем"],
        "c": 0,
    },
    {
        "q": "Что означает фраза 'Let the cat out of the bag'?",
        "a": ["Выпустить кота", "Проболтаться", "Освободиться", "Начать сначала"],
        "c": 1,
    },
    {
        "q": "Как понять выражение 'Hit the sack'?",
        "a": ["Ударить мешок", "Пойти спать", "Заниматься спортом", "Уволиться"],
        "c": 1,
    },
    {
        "q": "Что значит 'Once in a blue moon'?",
        "a": ["Каждое полнолуние", "Очень редко", "Романтическим вечером", "Никогда в жизни"],
        "c": 1,
    },
    {
        "q": "Как переводится 'A penny for your thoughts'?",
        "a": ["О чем ты думаешь?", "Купи мне что-нибудь", "Это дешевая идея", "Посчитай деньги"],
        "c": 0,
    },
    {
        "q": "Что означает 'The elephant in the room'?",
        "a": ["Очевидная проблема, которую игнорируют", "Большой беспорядок", "Очень важный гость", "Чья-то неуклюжесть"],
        "c": 0,
    },
    {
        "q": "Как перевести 'Barking up the wrong tree'?",
        "a": ["Искать не там / идти по ложному следу", "Громко ругаться", "Заблудиться в лесу", "Обидеть невиновного"],
        "c": 0,
    },
    {
        "q": "Что значит выражение 'Burn the midnight oil'?",
        "a": ["Работать или учиться допоздна", "Устроить пожар", "Тратить деньги впустую", "Готовить ужин"],
        "c": 0,
    },
    {
        "q": "Как понять фразу 'Cry over spilled milk'?",
        "a": ["Плакать по пустякам / о невозвратном", "Быть неосторожным", "Жаловаться на голод", "Убирать грязь"],
        "c": 0,
    },
    {
        "q": "Что означает 'Don't judge a book by its cover'?",
        "a": ["Не суди по обложке / внешности", "Читай только хорошие книги", "Не покупай дешевые вещи", "Доверяй первому впечатлению"],
        "c": 0,
    },
    {
        "q": "Как переводится 'Hit the nail on the head'?",
        "a": ["Попасть в точку / угадать", "Промахнуться", "Сделать ремонт", "Сильно разозлиться"],
        "c": 0,
    },
    {
        "q": "Что значит 'Kill two birds with one stone'?",
        "a": ["Убить двух зайцев одним выстрелом", "Сделать глупость", "Потерять всё", "Быть жестоким"],
        "c": 0,
    },
    {
        "q": "Как понять 'Miss the boat'?",
        "a": ["Упустить шанс", "Опоздать на рейс", "Забыть что-то важное", "Плыть по течению"],
        "c": 0,
    },
    {
        "q": "Что означает выражение 'See eye to eye'?",
        "a": ["Смотреть пристально", "Сходиться во мнениях", "Иметь хорошее зрение", "Спорить"],
        "c": 1,
    },
    {
        "q": "Как переводится 'The ball is in your court'?",
        "a": ["Игра началась", "Твоя очередь действовать", "Ты проиграл", "Мяч улетел"],
        "c": 1,
    },
    {
        "q": "Что значит фраза 'Pull someone's leg'?",
        "a": ["Разыгрывать / обманывать кого-то", "Помогать подняться", "Мешать работать", "Бежать за кем-то"],
        "c": 0,
    },
    {
        "q": "Как перевести 'Straight from the horse's mouth'?",
        "a": ["Из первоисточника / надежных уст", "Громкие слухи", "Ложные новости", "Очень быстро"],
        "c": 0,
    },
    {
        "q": "Что означает 'To take something with a grain of salt'?",
        "a": ["Относиться к чему-то скептически", "Посолить еду", "Принять близко к сердцу", "Обидеться"],
        "c": 0,
    },
    {
        "q": "Как понять 'Best of both worlds'?",
        "a": ["Лучшее из обоих миров / двойная выгода", "Космическое путешествие", "Трудный выбор", "Идеальное совпадение"],
        "c": 0,
    },
    {
        "q": "Что означает 'Blessing in disguise'?",
        "a": ["Неприятность, обернувшаяся благом", "Секретный подарок", "Религиозный праздник", "Случайное совпадение"],
        "c": 0,
    },
    {
        "q": "Как переводится 'A hot potato'?",
        "a": ["Горячая / злободневная тема", "Вкусный ужин", "Быстрая работа", "Тяжелая ноша"],
        "c": 0,
    },
    {
        "q": "Что значит 'Cut corners'?",
        "a": ["Халтурить / экономить в ущерб качеству", "Отрезать лишнее", "Идти короткой дорогой", "Заниматься геометрией"],
        "c": 0,
    },
    {
        "q": "Как перевести идиому 'Add insult to injury'?",
        "a": ["Сыпать соль на рану / ухудшить ситуацию", "Оказать первую помощь", "Поссориться с другом", "Извиниться за ошибку"],
        "c": 0,
    },
    {
        "q": "Что означает 'Beat around the bush'?",
        "a": ["Ходить вокруг да около", "Охотиться в лесу", "Говорить прямо", "Срезать кусты"],
        "c": 0,
    },
    {
        "q": "Как понять фразу 'Call it a day'?",
        "a": ["Закончить работу / закруглиться", "Назвать дату", "Праздновать день рождения", "Сделать перерыв на обед"],
        "c": 0,
    },
    {
        "q": "Что значит 'Get out of hand'?",
        "a": ["Выйти из-под контроля", "Выронить вещь", "Освободить руки", "Стать самостоятельным"],
        "c": 0,
    },
    {
        "q": "Как переводится 'Go back to the drawing board'?",
        "a": ["Начать всё сначала", "Вернуться в школу", "Заняться рисованием", "Признать поражение"],
        "c": 0,
    },
    {
        "q": "Что означает 'Make a long story short'?",
        "a": ["Короче говоря", "Сократить текст", "Придумать сказку", "Забыть подробности"],
        "c": 0,
    },
    {
        "q": "Как понять выражение 'No pain, no gain'?",
        "a": ["Без труда не выловишь и рыбку из пруда", "Боль неизбежна", "Спорт вреден", "Легкие деньги"],
        "c": 0,
    },
    {
        "q": "Что значит 'On the ball'?",
        "a": ["Быть расторопным / схватывать на лету", "Играть в футбол", "Стоять на мяче", "Ошибаться"],
        "c": 0,
    },
    {
        "q": "Как перевести 'Speak of the devil'?",
        "a": ["Легок на помине / о волке речь", "Говорить о плохом", "Ругаться", "Рассказывать сказки"],
        "c": 0,
    },
    {
        "q": "Что означает фраза 'Through thick and thin'?",
        "a": ["Сквозь огонь и воду / и в горе, и в радости", "Быстро худеть", "Идти напролом", "Делать выбор"],
        "c": 0,
    },
    {
        "q": "Как переводится 'Time flies'?",
        "a": ["Время летит", "Часы сломались", "Опоздание", "Свободное время"],
        "c": 0,
    },
    {
        "q": "Что значит выражение 'Face the music'?",
        "a": ["Смело встречать критику / отвечать за поступки", "Слушать концерт", "Включить радио", "Игнорировать проблемы"],
        "c": 0,
    }
]


DB_WORDS = [
    # Качества и описания (Прилагательные)
    {"ru": "красивый", "en": "beautiful"},
    {"ru": "точный", "en": "accurate"},
    {"ru": "великолепный", "en": "gorgeous"},
    {"ru": "удивительный", "en": "amazing"},
    {"ru": "полезный", "en": "useful"},
    {"ru": "сложный", "en": "complicated"},
    {"ru": "необходимый", "en": "necessary"},
    {"ru": "невозможный", "en": "impossible"},
    {"ru": "успешный", "en": "successful"},
    {"ru": "ответственный", "en": "responsible"},
    {"ru": "внимательный", "en": "attentive"},
    {"ru": "независимый", "en": "independent"},
    
    # Предметы и вещи (Существительные)
    {"ru": "журнал", "en": "magazine"},
    {"ru": "компьютер", "en": "computer"},
    {"ru": "словарь", "en": "dictionary"},
    {"ru": "путешествие", "en": "journey"},
    {"ru": "возможность", "en": "opportunity"},
    {"ru": "окружающая среда", "en": "environment"},
    {"ru": "достижение", "en": "achievement"},
    {"ru": "воображение", "en": "imagination"},
    {"ru": "поколение", "en": "generation"},
    {"ru": "правительство", "en": "government"},
    {"ru": "знание", "en": "knowledge"},
    {"ru": "опыт", "en": "experience"},
    
    # Действия и процессы (Глаголы)
    {"ru": "программировать", "en": "program"},
    {"ru": "развивать", "en": "develop"},
    {"ru": "исследовать", "en": "explore"},
    {"ru": "практиковать", "en": "practice"},
    {"ru": "улучшать", "en": "improve"},
    {"ru": "достигать", "en": "achieve"},
    {"ru": "рекомендовать", "en": "recommend"},
    {"ru": "праздновать", "en": "celebrate"},
    {"ru": "создавать", "en": "create"},
    {"ru": "переводить", "en": "translate"},
    
    # IT, учеба и технологии
    {"ru": "приложение", "en": "application"},
    {"ru": "интернет", "en": "internet"},
    {"ru": "база данных", "en": "database"},
    {"ru": "информация", "en": "information"},
    {"ru": "урок", "en": "lesson"},
    {"ru": "тренажер", "en": "trainer"}
]


DB_LESSONS = [
    {
        "id": 1,
        "title": "Урок 1: Знакомство",
        "task": "Соберите фразу: 'Я из Беларуси'",
        "words": ["from", "I", "Belarus", "am"],
        "correct": "I am from Belarus",
        "reward": 10,
    },
    {
        "id": 2,
        "title": "Урок 2: О себе",
        "task": "Соберите фразу: 'Мне нравится английский'",
        "words": ["English", "like", "I"],
        "correct": "I like English",
        "reward": 10,
    },
    {
        "id": 3,
        "title": "Урок 3: Работа",
        "task": "Соберите фразу: 'Я работаю здесь'",
        "words": ["work", "here", "I"],
        "correct": "I work here",
        "reward": 10,
    },
    {
        "id": 4,
        "title": "Урок 4: Приветствие",
        "task": "Соберите фразу: 'Доброе утро'",
        "words": ["morning", "Good"],
        "correct": "Good morning",
        "reward": 10,
    },
    {
        "id": 5,
        "title": "Урок 5: Имя",
        "task": "Соберите фразу: 'Как тебя зовут?'",
        "words": ["your", "What", "name", "is"],
        "correct": "What is your name",
        "reward": 10,
    },
    {
        "id": 6,
        "title": "Урок 6: Возраст",
        "task": "Соберите фразу: 'Мне 20 лет'",
        "words": ["old", "am", "twenty", "I", "years"],
        "correct": "I am twenty years old",
        "reward": 10,
    },
    {
        "id": 7,
        "title": "Урок 7: Прощание",
        "task": "Соберите фразу: 'Увидимся позже'",
        "words": ["later", "See", "you"],
        "correct": "See you later",
        "reward": 10,
    },
    {
        "id": 8,
        "title": "Урок 8: Семья",
        "task": "Соберите фразу: 'У меня есть сестра'",
        "words": ["a", "sister", "have", "I"],
        "correct": "I have a sister",
        "reward": 10,
    },
    {
        "id": 9,
        "title": "Урок 9: Дом",
        "task": "Соберите фразу: 'Это мой дом'",
        "words": ["house", "my", "is", "This"],
        "correct": "This is my house",
        "reward": 10,
    },
    {
        "id": 10,
        "title": "Урок 10: Питомец",
        "task": "Соберите фразу: 'Я люблю собак'",
        "words": ["dogs", "love", "I"],
        "correct": "I love dogs",
        "reward": 10,
    },
    {
        "id": 11,
        "title": "Урок 11: Погода",
        "task": "Соберите фразу: 'Сегодня солнечно'",
        "words": ["sunny", "is", "It", "today"],
        "correct": "It is sunny today",
        "reward": 10,
    },
    {
        "id": 12,
        "title": "Урок 12: Напитки",
        "task": "Соберите фразу: 'Я пью кофе'",
        "words": ["coffee", "drink", "I"],
        "correct": "I drink coffee",
        "reward": 10,
    },
    {
        "id": 13,
        "title": "Урок 13: Еда",
        "task": "Соберите фразу: 'Она ест яблоко'",
        "words": ["an", "eats", "apple", "She"],
        "correct": "She eats an apple",
        "reward": 10,
    },
    {
        "id": 14,
        "title": "Урок 14: Город",
        "task": "Соберите фразу: 'Это большой город'",
        "words": ["city", "big", "a", "is", "This"],
        "correct": "This is a big city",
        "reward": 10,
    },
    {
        "id": 15,
        "title": "Урок 15: Друзья",
        "task": "Соберите фразу: 'Мы друзья'",
        "words": ["friends", "are", "We"],
        "correct": "We are friends",
        "reward": 10,
    },
    {
        "id": 16,
        "title": "Урок 16: Время",
        "task": "Соберите фразу: 'Сейчас пять часов'",
        "words": ["o'clock", "five", "is", "It", "now"],
        "correct": "It is five o'clock now",
        "reward": 10,
    },
    {
        "id": 17,
        "title": "Урок 17: Цвета",
        "task": "Соберите фразу: 'Небо синее'",
        "words": ["blue", "sky", "is", "The"],
        "correct": "The sky is blue",
        "reward": 10,
    },
    {
        "id": 18,
        "title": "Урок 18: Хобби",
        "task": "Соберите фразу: 'Он умеет плавать'",
        "words": ["swim", "can", "He"],
        "correct": "He can swim",
        "reward": 10,
    },
    {
        "id": 19,
        "title": "Урок 19: Транспорт",
        "task": "Соберите фразу: 'У него есть машина'",
        "words": ["car", "has", "a", "He"],
        "correct": "He has a car",
        "reward": 10,
    },
    {
        "id": 20,
        "title": "Урок 20: Вопрос",
        "task": "Соберите фразу: 'Ты говоришь по-английски?'",
        "words": ["English", "you", "Do", "speak"],
        "correct": "Do you speak English",
        "reward": 10,
    },
    {
        "id": 21,
        "title": "Урок 21: Вечер",
        "task": "Соберите фразу: 'Я смотрю телевизор по вечерам'",
        "words": ["the", "evening", "TV", "in", "watch", "I"],
        "correct": "I watch TV in the evening",
        "reward": 10,
    },
    {
        "id": 22,
        "title": "Урок 22: Музыка",
        "task": "Соберите фразу: 'Они слушают музыку'",
        "words": ["music", "to", "listen", "They"],
        "correct": "They listen to music",
        "reward": 10,
    },
    {
        "id": 23,
        "title": "Урок 23: Школа",
        "task": "Соберите фразу: 'Книга лежит на столе'",
        "words": ["on", "table", "book", "is", "The", "the"],
        "correct": "The book is on the table",
        "reward": 10,
    },
    {
        "id": 24,
        "title": "Урок 24: Покупки",
        "task": "Соберите фразу: 'Сколько это стоит?'",
        "words": ["is", "it", "much", "How"],
        "correct": "How much is it",
        "reward": 10,
    },
    {
        "id": 25,
        "title": "Урок 25: Дни недели",
        "task": "Соберите фразу: 'Сегодня понедельник'",
        "words": ["is", "Monday", "It", "today"],
        "correct": "It is Monday today",
        "reward": 10,
    },
    {
        "id": 26,
        "title": "Урок 26: Чувства",
        "task": "Соберите фразу: 'Я очень устал сегодня'",
        "words": ["very", "tired", "am", "I", "today"],
        "correct": "I am very tired today",
        "reward": 10,
    },
    {
        "id": 27,
        "title": "Урок 27: Место",
        "task": "Соберите фразу: 'Где находится туалет?'",
        "words": ["bathroom", "the", "Where", "is"],
        "correct": "Where is the bathroom",
        "reward": 10,
    },
    {
        "id": 28,
        "title": "Урок 28: Просьба",
        "task": "Соберите фразу: 'Передайте мне соль, пожалуйста'",
        "words": ["please", "Pass", "me", "salt", "the"],
        "correct": "Pass me the salt please",
        "reward": 10,
    },
    {
        "id": 29,
        "title": "Урок 29: Направление",
        "task": "Соберите фразу: 'Поверните направо на углу'",
        "words": ["the", "corner", "at", "Turn", "right"],
        "correct": "Turn right at the corner",
        "reward": 10,
    },
    {
        "id": 30,
        "title": "Урок 30: Планы",
        "task": "Соберите фразу: 'Я собираюсь пойти гулять'",
        "words": ["a", "walk", "for", "go", "to", "going", "am", "I"],
        "correct": "I am going to go for a walk",
        "reward": 10,
    },
    {
        "id": 31,
        "title": "Урок 31: Спорт",
        "task": "Соберите фразу: 'Мой брат играет в футбол по выходным'",
        "words": ["weekends", "on", "football", "plays", "brother", "My"],
        "correct": "My brother plays football on weekends",
        "reward": 10,
    },
    {
        "id": 32,
        "title": "Урок 32: Будущее",
        "task": "Соберите фразу: 'Завтра пойдет дождь'",
        "words": ["rain", "will", "It", "tomorrow"],
        "correct": "It will rain tomorrow",
        "reward": 10,
    },
    {
        "id": 33,
        "title": "Урок 33: Прошлое",
        "task": "Соберите фразу: 'Вчера я видел хороший фильм'",
        "words": ["good", "yesterday", "saw", "movie", "a", "I"],
        "correct": "I saw a good movie yesterday",
        "reward": 10,
    },
    {
        "id": 34,
        "title": "Урок 34: Одежда",
        "task": "Соберите фразу: 'На ней теплое пальто'",
        "words": ["a", "wearing", "is", "She", "coat", "warm"],
        "correct": "She is wearing a warm coat",
        "reward": 10,
    },
    {
        "id": 35,
        "title": "Урок 35: Ресторан",
        "task": "Соберите фразу: 'Я бы хотел заказать столик'",
        "words": ["to", "table", "a", "book", "like", "would", "I"],
        "correct": "I would like to book a table",
        "reward": 10,
    },
    {
        "id": 36,
        "title": "Урок 36: Здоровье",
        "task": "Соберите фразу: 'У меня болит голова'",
        "words": ["a", "headache", "have", "I"],
        "correct": "I have a headache",
        "reward": 10,
    },
    {
        "id": 37,
        "title": "Урок 37: Отрицание",
        "task": "Соберите фразу: 'Я не знаю ответа'",
        "words": ["answer", "know", "the", "not", "do", "I"],
        "correct": "I do not know the answer",
        "reward": 10,
    },
    {
        "id": 38,
        "title": "Урок 38: Готовка",
        "task": "Соберите фразу: 'Моя мама печет пирог'",
        "words": ["cake", "a", "baking", "is", "mother", "My"],
        "correct": "My mother is baking a cake",
        "reward": 10,
    },
    {
        "id": 39,
        "title": "Урок 39: Путешествия",
        "task": "Соберите фразу: 'Где мой паспорт?'",
        "words": ["passport", "my", "is", "Where"],
        "correct": "Where is my passport",
        "reward": 10,
    },
    {
        "id": 40,
        "title": "Урок 40: Желания",
        "task": "Соберите фразу: 'Я хочу выучить английский язык'",
        "words": ["English", "learn", "to", "want", "I"],
        "correct": "I want to learn English",
        "reward": 10,
    },
    {
        "id": 41,
        "title": "Урок 41: Сравнение",
        "task": "Соберите фразу: 'Эта книга интереснее той'",
        "words": ["that", "one", "than", "interesting", "more", "is", "book", "This"],
        "correct": "This book is more interesting than that one",
        "reward": 10,
    },
    {
        "id": 42,
        "title": "Урок 42: Привычки",
        "task": "Соберите фразу: 'Он всегда встает рано'",
        "words": ["early", "up", "gets", "always", "He"],
        "correct": "He always gets up early",
        "reward": 10,
    },
    {
        "id": 43,
        "title": "Урок 43: Обязанности",
        "task": "Соберите фразу: 'Ты должен сделать это сейчас'",
        "words": ["now", "it", "do", "must", "You"],
        "correct": "You must do it now",
        "reward": 10,
    },
    {
        "id": 44,
        "title": "Урок 44: Разрешение",
        "task": "Соберите фразу: 'Можно мне войти?'",
        "words": ["come", "I", "in", "May"],
        "correct": "May I come in",
        "reward": 10,
    },
    {
        "id": 45,
        "title": "Урок 45: Опыт",
        "task": "Соберите фразу: 'Я уже бывал в Лондоне'",
        "words": ["London", "to", "been", "have", "already", "I"],
        "correct": "I have already been to London",
        "reward": 10,
    },
    {
        "id": 46,
        "title": "Урок 46: Длительность",
        "task": "Соберите фразу: 'Она живет здесь пять лет'",
        "words": ["years", "five", "for", "here", "lived", "has", "She"],
        "correct": "She has lived here for five years",
        "reward": 10,
    },
    {
        "id": 47,
        "title": "Урок 47: Предпочтения",
        "task": "Соберите фразу: 'Я предпочитаю чай вместо кофе'",
        "words": ["coffee", "to", "tea", "prefer", "I"],
        "correct": "I prefer tea to coffee",
        "reward": 10,
    },
    {
        "id": 48,
        "title": "Урок 48: Причина",
        "task": "Соберите фразу: 'Я опоздал из-за пробки'",
        "words": ["traffic", "the", "of", "because", "late", "was", "I"],
        "correct": "I was late because of the traffic",
        "reward": 10,
    },
    {
        "id": 49,
        "title": "Урок 49: Совет",
        "task": "Соберите фразу: 'Тебе следует пить больше воды'",
        "words": ["water", "more", "drink", "should", "You"],
        "correct": "You should drink more water",
        "reward": 10,
    },
    {
        "id": 50,
        "title": "Урок 50: Возможность",
        "task": "Соберите фразу: 'Сегодня вечером может пойти снег'",
        "words": ["tonight", "snow", "might", "It"],
        "correct": "It might snow tonight",
        "reward": 10,
    },
    {
        "id": 51,
        "title": "Урок 51: Пассивный залог",
        "task": "Соберите фразу: 'Это письмо было написано вчера'",
        "words": ["yesterday", "written", "was", "letter", "This"],
        "correct": "This letter was written yesterday",
        "reward": 10,
    },
    {
        "id": 52,
        "title": "Урок 52: Условие (Тип 1)",
        "task": "Соберите фразу: 'Если пойдет дождь, я останусь дома'",
        "words": ["home", "stay", "will", "I", "rains", "it", "If"],
        "correct": "If it rains I will stay home",
        "reward": 10,
    },
    {
        "id": 53,
        "title": "Урок 53: Одновременность",
        "task": "Соберите фразу: 'Он читал, пока она готовила'",
        "words": ["cooking", "was", "she", "while", "reading", "was", "He"],
        "correct": "He was reading while she was cooking",
        "reward": 10,
    },
    {
        "id": 54,
        "title": "Урок 54: Ожидание",
        "task": "Соберите фразу: 'Я с нетерпением жду встречи с вами'",
        "words": ["you", "meeting", "to", "forward", "looking", "am", "I"],
        "correct": "I am looking forward to meeting you",
        "reward": 10,
    },
    {
        "id": 55,
        "title": "Урок 55: Способности",
        "task": "Соберите фразу: 'Она умеет свободно говорить по-французски'",
        "words": ["fluently", "French", "speak", "can", "She"],
        "correct": "She can speak French fluently",
        "reward": 10,
    },
    {
        "id": 56,
        "title": "Урок 56: Предложение",
        "task": "Соберите фразу: 'Как насчет того, чтобы пойти в кино?'",
        "words": ["cinema", "the", "to", "going", "about", "How"],
        "correct": "How about going to the cinema",
        "reward": 10,
    },
    {
        "id": 57,
        "title": "Урок 57: Принятие решений",
        "task": "Соберите фразу: 'Я еще не принял решение'",
        "words": ["yet", "mind", "my", "up", "made", "not", "have", "I"],
        "correct": "I have not made up my mind yet",
        "reward": 10,
    },
    {
        "id": 58,
        "title": "Урок 58: Воспоминания",
        "task": "Соберите фразу: 'Я помню, как видел его в детстве'",
        "words": ["child", "a", "as", "him", "seeing", "remember", "I"],
        "correct": "I remember seeing him as a child",
        "reward": 10,
    },
    {
        "id": 59,
        "title": "Урок 59: Сравнение (Превосходная)",
        "task": "Соберите фразу: 'Это самый красивый вид в мире'",
        "words": ["world", "the", "in", "view", "beautiful", "most", "the", "is", "This"],
        "correct": "This is the most beautiful view in the world",
        "reward": 10,
    },
    {
        "id": 60,
        "title": "Урок 60: Завершение",
        "task": "Соберите фразу: 'Мы только что закончили проект'",
        "words": ["project", "the", "finished", "just", "have", "We"],
        "correct": "We have just finished the project",
        "reward": 10,
    },
    {
        "id": 61,
        "title": "Урок 61: Косвенная речь",
        "task": "Соберите фразу: 'Он сказал, что придет позже'",
        "words": ["later", "come", "would", "he", "that", "said", "He"],
        "correct": "He said that he would come later",
        "reward": 10,
    },
    {
        "id": 62,
        "title": "Урок 62: Предыдущее действие",
        "task": "Соберите фразу: 'Поезд уже ушел, когда я приехал'",
        "words": ["arrived", "I", "when", "left", "already", "had", "train", "The"],
        "correct": "The train had already left when I arrived",
        "reward": 10,
    },
    {
        "id": 63,
        "title": "Урок 63: Условие (Тип 2)",
        "task": "Соберите фразу: 'Если бы я был богат, я бы купил остров'",
        "words": ["island", "an", "buy", "would", "I", "rich", "were", "I", "If"],
        "correct": "If I were rich I would buy an island",
        "reward": 10,
    },
    {
        "id": 64,
        "title": "Урок 64: Модальные глаголы",
        "task": "Соберите фразу: 'Вам следовало запереть дверь на замок'",
        "words": ["door", "the", "locked", "have", "should", "You"],
        "correct": "You should have locked the door",
        "reward": 10,
    },
    {
        "id": 65,
        "title": "Урок 65: Зависимость",
        "task": "Соберите фразу: 'Все зависит от твоего решения'",
        "words": ["decision", "your", "on", "depends", "Everything"],
        "correct": "Everything depends on your decision",
        "reward": 10,
    },
    {
        "id": 66,
        "title": "Урок 66: Удивление",
        "task": "Соберите фразу: 'Я не ожидал увидеть тебя здесь'",
        "words": ["here", "you", "see", "to", "expect", "did", "not", "I"],
        "correct": "I did not expect to see you here",
        "reward": 10,
    },
    {
        "id": 67,
        "title": "Урок 67: Извинение",
        "task": "Соберите фразу: 'Простите за то, что заставил вас ждать'",
        "words": ["waiting", "you", "keeping", "for", "apologize", "I"],
        "correct": "I apologize for keeping you waiting",
        "reward": 10,
    },
    {
        "id": 68,
        "title": "Урок 68: Цель",
        "task": "Соберите фразу: 'Он усердно учится, чтобы сдать экзамен'",
        "words": ["exam", "the", "pass", "to", "hard", "studies", "He"],
        "correct": "He studies hard to pass the exam",
        "reward": 10,
    },
    {
        "id": 69,
        "title": "Урок 69: Сожаление",
        "task": "Соберите фразу: 'Жаль, что я не послушал твоего совета'",
        "words": ["advice", "your", "taken", "had", "I", "wish", "I"],
        "correct": "I wish I had taken your advice",
        "reward": 10,
    },
    {
        "id": 70,
        "title": "Урок 70: Сложный пассив",
        "task": "Соберите фразу: 'Дом сейчас ремонтируют'",
        "words": ["repaired", "being", "is", "house", "the", "The"],
        "correct": "The house is being repaired",
        "reward": 10,
    },
    {
        "id": 71,
        "title": "Урок 71: Концентрация",
        "task": "Соберите фразу: 'Ей трудно сосредоточиться на работе'",
        "words": ["work", "her", "on", "concentrate", "to", "hard", "it", "finds", "She"],
        "correct": "She finds it hard to concentrate on her work",
        "reward": 10,
    },
    {
        "id": 72,
        "title": "Урок 72: Уступка",
        "task": "Соберите фразу: 'Несмотря на дождь, мы пошли гулять'",
        "words": ["walk", "a", "for", "went", "we", "rain", "the", "Despite"],
        "correct": "Despite the rain we went for a walk",
        "reward": 10,
    },
    {
        "id": 73,
        "title": "Урок 73: Длительный перфект",
        "task": "Соберите фразу: 'Я жду здесь уже два часа'",
        "words": ["hours", "two", "for", "here", "waiting", "been", "have", "I"],
        "correct": "I have been waiting here for two hours",
        "reward": 10,
    },
    {
        "id": 74,
        "title": "Урок 74: Обвинение",
        "task": "Соберите фразу: 'Они обвинили его во лжи'",
        "words": ["lying", "of", "him", "accused", "They"],
        "correct": "They accused him of lying",
        "reward": 10,
    },
    {
        "id": 75,
        "title": "Урок 75: Вероятность в прошлом",
        "task": "Соберите фразу: 'Должно быть, он забыл свои ключи дома'",
        "words": ["home", "at", "keys", "his", "forgotten", "have", "must", "He"],
        "correct": "He must have forgotten his keys at home",
        "reward": 10,
    },
    {
        "id": 76,
        "title": "Урок 76: Избегание",
        "task": "Соберите фразу: 'Вам следует избегать совершения подобных ошибок'",
        "words": ["mistakes", "such", "making", "avoid", "should", "You"],
        "correct": "You should avoid making such mistakes",
        "reward": 10,
},
    {
        "id": 77,
        "title": "Урок 77: Каузатив",
        "task": "Соберите фразу: 'Завтра мне отремонтируют машину'",
        "words": ["tomorrow", "repaired", "car", "my", "have", "will", "I"],
        "correct": "I will have my car repaired tomorrow",
        "reward": 10,
    },
    {
        "id": 78,
        "title": "Урок 78: Условие (Тип 3)",
        "task": "Соберите фразу: 'Если бы ты учился, ты бы сдал тест'",
        "words": ["test", "the", "passed", "have", "would", "you", "studied", "had", "you", "If"],
        "correct": "If you had studied you would have passed the test",
        "reward": 10,
    },
    {
        "id": 79,
        "title": "Урок 79: Привыкание",
        "task": "Я постепенно привыкаю к новой погоде",
        "words": ["weather", "new", "the", "to", "used", "getting", "am", "I"],
        "correct": "I am getting used to the new weather",
        "reward": 10,
    },
    {
        "id": 80,
        "title": "Урок 80: Мнение",
        "task": "Соберите фразу: 'Насколько я могу судить, это правда'",
        "words": ["true", "is", "it", "concerned", "am", "I", "as", "far", "As"],
        "correct": "As far as I am concerned it is true",
        "reward": 10,
    },
    {
        "id": 81,
        "title": "Урок 81: Усложненная инверсия",
        "task": "Соберите фразу: 'Едва я приехал, как начался сильный дождь'",
        "words": ["started", "rain", "the", "than", "arrived", "I", "had", "Scarcely"],
        "correct": "Scarcely had I arrived than the rain started",
        "reward": 10,
    },
    {
        "id": 82,
        "title": "Урок 82: Продвинутое предположение",
        "task": "Соберите фразу: 'Этого проекта нигде не найти'",
        "words": ["found", "be", "to", "nowhere", "is", "project", "this", "Under", "no", "circumstances"],
        "correct": "Under no circumstances is this project to be found",
        "reward": 10,
    },
    {
        "id": 83,
        "title": "Урок 83: Смешанное условие 1",
        "task": "Соберите фразу: 'Если бы я вчера выиграл, я был бы богат сейчас'",
        "words": ["now", "rich", "be", "would", "I", "yesterday", "won", "had", "I", "If"],
        "correct": "If I had won yesterday I would be rich now",
        "reward": 10,
    },
    {
        "id": 84,
        "title": "Урок 84: Смешанное условие 2",
        "task": "Соберите фразу: 'Если бы она была умнее, она бы не совершила ту ошибку'",
        "words": ["mistake", "that", "made", "have", "not", "would", "she", "smarter", "were", "she", "If"],
        "correct": "If she were smarter she would not have made that mistake",
        "reward": 10,
    },
    {
        "id": 85,
        "title": "Урок 85: Продвинутый герундий",
        "task": "Соберите фразу: 'Бесполезно пытаться убедить его измениться'",
        "words": ["change", "to", "him", "persuading", "trying", "use", "no", "is", "It"],
        "correct": "It is no use trying persuading him to change",
        "reward": 10,
    },
    {
        "id": 86,
        "title": "Урок 86: Сложное подлежащее",
        "task": "Соберите фразу: 'Говорят, что он потерял все свое состояние'",
        "words": ["fortune", "his", "all", "lost", "have", "to", "said", "is", "He"],
        "correct": "He is said to have lost all his fortune",
        "reward": 10,
    },
    {
        "id": 87,
        "title": "Урок 87: Сложное дополнение",
        "task": "Соберите фразу: 'Я никогда не слышал, чтобы она так красиво пела'",
        "words": ["beautifully", "so", "sing", "her", "heard", "never", "have", "I"],
        "correct": "I have never heard her sing so beautifully",
        "reward": 10,
    },
    {
        "id": 88,
        "title": "Урок 88: Сослагательное наклонение",
        "task": "Соберите фразу: 'Я требую, чтобы он немедленно ушел'",
        "words": ["immediately", "leave", "he", "that", "demand", "I"],
        "correct": "I demand that he leave immediately",
        "reward": 10,
    },
    {
        "id": 89,
        "title": "Урок 89: Ограничение",
        "task": "Соберите фразу: 'Мы не только опоздали, но и потеряли багаж'",
        "words": ["luggage", "our", "lost", "we", "did", "also", "but", "late", "we", "were", "Only", "not"],
        "correct": "Only not were we late but also did we lose our luggage",
        "reward": 10,
    },
    {
        "id": 90,
        "title": "Урок 90: Эмфаза",
        "task": "Соберите фразу: 'Именно его высокомерие привело к его краху'",
        "words": ["downfall", "his", "to", "led", "arrogance", "his", "was", "it", "That"],
        "correct": "That it was his arrogance led to his downfall",
        "reward": 10,
    },
    {
        "id": 91,
        "title": "Урок 91: Идиома (Продвинутый уровень)",
        "task": "Соберите фразу: 'Нам нужно прекратить ходить вокруг да около'",
        "words": ["bush", "the", "around", "beating", "stop", "to", "need", "We"],
        "correct": "We need to stop beating around the bush",
        "reward": 10,
    },
    {
        "id": 92,
        "title": "Урок 92: Идиома (Продолжение)",
        "task": "Соберите фразу: 'Это решение стоит очень дорого'",
        "words": ["leg", "a", "and", "arm", "an", "costs", "decision", "this", "That"],
        "correct": "That this decision costs an arm and a leg",
        "reward": 10,
    },
    {
        "id": 93,
        "title": "Урок 93: Отрицательное условие",
        "task": "Соберите фразу: 'Если вы не поторопитесь, вы опоздаете на поезд'",
        "words": ["train", "the", "miss", "will", "you", "hurry", "you", "Unless"],
        "correct": "Unless you hurry you will miss the train",
        "reward": 10,
    },
    {
        "id": 94,
        "title": "Урок 94: Прошедшее нереальное",
        "task": "Соберите фразу: 'Лучше бы вы не рассказывали ему секрет вчера'",
        "words": ["yesterday", "secret", "the", "him", "told", "not", "had", "you", "rather", "would", "I"],
        "correct": "I would rather you had not told him the secret yesterday",
        "reward": 10,
    },
    {
        "id": 95,
        "title": "Урок 95: Сверхсложный пассив",
        "task": "Соберите фразу: 'Считается, что картина была украдена в прошлом веке'",
        "words": ["century", "last", "stolen", "been", "have", "to", "believed", "is", "painting", "The"],
        "correct": "The painting is believed to have been stolen last century",
        "reward": 10,
    },
    {
        "id": 96,
        "title": "Урок 96: Предосторожность",
        "task": "Соберите фразу: 'Возьми зонт на случай, если пойдет дождь'",
        "words": ["rains", "it", "case", "in", "umbrella", "an", "Take"],
        "correct": "Take an umbrella in case it rains",
        "reward": 10,
    },
    {
        "id": 97,
        "title": "Урок 97: Альтернатива",
        "task": "Соберите фразу: 'У нас нет другого выбора, кроме как принять их условия'",
        "words": ["terms", "their", "accept", "to", "but", "choice", "no", "have", "We"],
        "correct": "We have no choice but to accept their terms",
        "reward": 10,
    },
    {
        "id": 98,
        "title": "Урок 98: Вывод",
        "task": "Соберите фразу: 'Учитывая все обстоятельства, это был огромный успех'",
        "words": ["success", "huge", "a", "was", "it", "consideration", "into", "everything", "Taking"],
        "correct": "Taking everything into consideration it was a huge success",
        "reward": 10,
    },
    {
        "id": 99,
        "title": "Урок 99: Финал грамматики",
        "task": "Соберите фразу: 'Чем больше ты учишься, тем умнее становишься'",
        "words": ["get", "you", "smarter", "the", "learn", "you", "more", "the", "The"],
        "correct": "The more you learn the smarter you get",
        "reward": 10,
    },
    {
        "id": 100,
        "title": "Урок 100: Профессионал",
        "task": "Соберите фразу: 'Поздравляем, вы успешно прошли весь этот курс'",
        "words": ["course", "entire", "this", "passed", "successfully", "have", "you", "Congratulations"],
        "correct": "Congratulations you have successfully passed this entire course",
        "reward": 10,
    },
]


TRANSLATE_DICT = {
    # === Базовая вежливость и приветствия ===
    "привет": "hello / hi / hey",
    "как дела": "how are you / how is it going / what's up",
    "доброе утро": "good morning",
    "добрый день": "good afternoon",
    "добрый вечер": "good evening",
    "пока": "bye / goodbye / see ya",
    "увидимся": "see you later / catch you later",
    "хорошего дня": "have a nice day",
    "спасибо": "thank you / thanks",
    "большое спасибо": "thank you very much / thanks a lot",
    "пожалуйста": "please",
    "не за что": "you are welcome / no problem / don't mention it",
    "извините": "excuse me / sorry",
    "простите": "i am so sorry",
    "все хорошо": "it is okay / everything is fine / no worries",
    "да": "yes / yeah",
    "нет": "no / nope",
    "конечно": "of course / sure / absolutely",
    "с удовольствием": "with pleasure / i'd love to",

    # === Легендарные английские идиомы (Крылатые выражения) ===
    "проще простого": "a piece of cake / as easy as pie",
    "удачи": "break a leg / good luck",
    "стиснуть зубы": "bite the bullet",
    "решиться": "bite the bullet / make up one's mind",
    "раскрыть секрет": "spill the beans / let the cat out of the bag",
    "проболтаться": "spill the beans / blab",
    "подлить масла в огонь": "add fuel to the fire / add insult to injury",
    "бить баклуши": "twiddle one's thumbs / loaf around",
    "кусать локти": "kick oneself",
    "делать из мухи слона": "make a mountain out of a molehill",
    "когда рак на горе свистнет": "when pigs fly / once in a blue moon",
    "быть на седьмом небе от счастья": "be on cloud nine / over the moon",
    "лить как из ведра": "rain cats and dogs / it's pouring",
    "черная полоса": "a run of bad luck",
    "время летит": "time flies",
    "лучше поздно, чем никогда": "better late than never",
    "рискнуть всем": "go all in",
    "взять себя в руки": "pull yourself together",
    "не вешай нос": "keep your chin up",
    "с чистого листа": "from scratch / clean slate",
    "доверять интуиции": "trust your gut",
    "поживем - увидим": "wait and see",
    "убить двух зайцев одним выстрелом": "kill two birds with one stone",
    "быть в одной лодке": "be in the same boat",
    "раз в сто лет": "once in a blue moon",
    "пройти сквозь огонь и воду": "go through thick and thin",
    "держать язык за зубами": "bite your tongue / keep your lips sealed",
    "строить замки из песка": "pipe dream / build castles in the air",
    "на воре и шапка горит": "if the shoe fits, wear it",
    "куй железо, пока горячо": "strike while the iron is hot",

    # === Разговорные фразы и реакции в диалоге ===
    "я имею в виду": "i mean",
    "кстати": "by the way / anyway",
    "на самом деле": "actually / in fact",
    "короче говоря": "in short / to make a long story short",
    "без обид": "no offense",
    "мне все равно": "i don't care / it doesn't matter / whatever",
    "это зависит от": "it depends on",
    "само собой разумеется": "it goes without saying",
    "так тебе и надо": "serves you right",
    "успокойся": "calm down / chill out / take it easy",
    "не парься": "don't sweat it / don't worry about it",
    "имеет смысл": "it makes sense",
    "это не имеет смысла": "it makes no sense",
    "я согласен": "i agree",
    "я не согласен": "i disagree",
    "я не знаю": "i do not know / i dunno / no idea",
    "я понимаю": "i understand / i get it",
    "я не понимаю": "i do not understand / i don't get it",
    "повторите, пожалуйста": "repeat, please / pardon?",
    "мне нужна помощь": "i need help",
    "без проблем": "no problem / piece of cake",
    "минутку, пожалуйста": "just a minute, please / hold on",
    "понятия не имею": "i have no idea / clueless",
    "это потрясающе": "that's awesome / amazing",
    "мне кажется": "it seems to me / i feel like",

    # === Учеба, языки и программирование ===
    "я люблю программировать": "i love programming / i like to code",
    "английский язык": "english language / english",
    "я учусь": "i am learning / i am studying",
    "я учу английский": "i am learning english / i study english",
    "мне нравится английский": "i like english",
    "я пишу код": "i am coding / i write code",
    "это сложная задача": "this is a difficult task / tough challenge",
    "практика ведет к совершенству": "practice makes perfect",
    "я хочу знать английский": "i want to know english / want to speak english",
    "учить языки полезно": "learning languages is useful / beneficial",
    "зубрить": "cram / study hard",
    "сдать экзамен": "pass an exam",
    "провалить экзамен": "fail an exam",
    "исправить ошибку": "fix a bug / correct a mistake",
    "искать информацию": "look for information / google it",

    # === Путешествия, шоппинг и повседневная жизнь ===
    "сколько это стоит": "how much is it / how much does it cost",
    "который час": "what time is it / got the time?",
    "где находится": "where is ... located?",
    "как добраться до": "how can i get to ... ?",
    "мне нужен счет, пожалуйста": "the bill, please / check, please",
    "где здесь туалет": "where is the restroom / bathroom?",
    "вызовите такси": "call a taxi / order a cab",
    "я потерялся": "i am lost",
    "помогите мне": "help me",
    "счастливого пути": "have a safe trip / bon voyage",
    "я просто смотрю": "i'm just looking / just browsing",
    "можно примерить": "can i try it on?",
    "где выход": "where is the exit?",
    "где вход": "where is the entrance?",
    "сделайте скидку": "can i get a discount?",
    "примите карту": "do you accept cards?",
    "только наличные": "cash only",
    "удачи в учебе": "good luck with your studies / happy learning"
}

session_data = {"quiz_score": 0, "train_score": 0, "lessons_completed": 0}

HTML_CODE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Learn English Ultimate Pro</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
        body { background: #f0f2f5; color: #333; padding-bottom: 60px; padding-top: 50px; }
        header { background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 25px 20px; text-align: center; }
        header h1 { font-size: 2rem; margin-bottom: 5px; }
        nav { display: flex; justify-content: center; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.05); flex-wrap: wrap; }
        nav button { background: none; color: #555; padding: 15px 20px; font-size: 0.95rem; border: none; cursor: pointer; border-bottom: 3px solid transparent; }
        nav button.active { color: #2a5298; border-bottom-color: #2a5298; font-weight: bold; }
        .container { max-width: 800px; margin: 25px auto; padding: 0 20px; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.06); text-align: center; margin-bottom: 20px; }
        .card h2 { color: #1e3c72; margin-bottom: 15px; }
        .quiz-question, .trainer-prompt { font-size: 1.2rem; margin-bottom: 15px; font-weight: bold; color: #444; }
        .quiz-options { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; max-width: 500px; margin: 0 auto; }
        button.action-btn { background: #2a5298; color: white; border: none; padding: 12px; border-radius: 6px; font-size: 0.95rem; cursor: pointer; width: 100%; }
        button.action-btn:hover { background: #1e3c72; }
        input[type="text"], textarea { width: 100%; max-width: 500px; padding: 12px; font-size: 1rem; border: 2px solid #ddd; border-radius: 6px; margin-bottom: 15px; text-align: center; outline: none; }
        .result { margin-top: 15px; font-weight: bold; font-size: 1.05rem; min-height: 25px; }
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; max-width: 600px; margin: 20px auto; }
        .stat-item { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #e9ecef; }
        .stat-val { font-size: 1.8rem; font-weight: bold; color: #2a5298; margin-top: 5px; }
        .word-chip { display: inline-block; background: #e9ecef; padding: 8px 15px; margin: 5px; border-radius: 20px; cursor: pointer; user-select: none; font-weight: bold; }
        .word-chip:hover { background: #dee2e6; }
        .lesson-box { background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 8px; padding: 15px; margin-bottom: 15px; text-align: left; }
        .lesson-box.locked { opacity: 0.5; cursor: not-allowed; }
    </style>
</head>
<body>
    <!-- Вкладка магазина в левом верхнем углу -->
    <div style="position: fixed; top: 10px; left: 10px; z-index: 1001;">
        <button onclick="switchTab('shop')" id="btn-shop" style="background: #28a745; color: white; padding: 10px 15px; border: none; text-decoration: none; border-radius: 8px; font-weight: bold; font-family: Arial, sans-serif; cursor: pointer; font-size: 0.95rem; box-shadow: 0 2px 5px rgba(0,0,0,0.15);">
            🛒 Магазин
        </button>
    </div>

    <!-- Блок с монетами в правом верхнем углу -->
    <div style="position: fixed; top: 10px; right: 10px; background: #fff; border: 2px solid #2a5298; padding: 9px 15px; border-radius: 8px; z-index: 1001; font-family: Arial, sans-serif; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.15); color: #333;">
        💰 Монеты: <span id="user-coins-display" style="color: #2a5298; font-size: 1.05rem;">0</span>
    </div>

    <header>
        <h1>English Learning Ultimate</h1>
        <p>Квиз, тренажер, переводчик и интерактивные уроки</p>
    </header>
    <nav>
        <button class="active" id="btn-quiz" onclick="switchTab('quiz')">🧩 Квиз</button>
        <button id="btn-trainer" onclick="switchTab('trainer')">✍️ Тренажер</button>
        <button id="btn-translator" onclick="switchTab('translator')">🌐 Переводчик</button>
        <button id="btn-lessons" onclick="switchTab('lessons')">🦉 Уроки Duolingo</button>
        <button id="btn-profile" onclick="switchTab('profile')">👤 Кабинет</button>
    </nav>
    <div class="container">
        <!-- Блок Вкладки Магазина -->
        <div id="shop" class="tab-content">
            <div class="card">
                <h2>Магазин бонусов</h2>
                <p style="margin-bottom: 20px; color: #666;">Тратьте заработанные монеты на полезные улучшения!</p>
                <div style="display: flex; flex-direction: column; gap: 15px; max-width: 400px; margin: 0 auto;">
                    <div style="background: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <div style="text-align: left;">
                            <strong style="display: block;">Пропуск урока</strong>
                            <span style="font-size: 0.85rem; color: #666;">Позволяет пропустить сложный шаг</span>
                        </div>
                        <button class="action-btn" style="width: auto; background: #28a745; padding: 8px 12px;" onclick="buyItem('skip')">30 💰</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="quiz" class="tab-content active">
            <div class="card">
                <h2>Проверка знаний (Идиомы)</h2>
                <div class="quiz-question" id="quiz-q">Загрузка...</div>
                <div class="quiz-options" id="quiz-opts"></div>
                <div class="result" id="quiz-res"></div>
            </div>
        </div>

       async function updateCoins() {
    let r = await fetch('/api/get_coins');
    let d = await r.json();
    document.getElementById('user-coins-display').innerText = d.coins;
}

async function buyItem(itemType) {
    let r = await fetch('/api/buy_item', {
        method: 'POST',
        body: new URLSearchParams({ item: itemType })
    });
    let d = await r.json();
    if (d.status === 'success') {
        alert('Покупка совершена успешно!');
        updateCoins();
    } else {
        alert('Ошибка: ' + d.message);
    }
}

async function checkTrainer() {
    let ans = document.getElementById('train-input').value.trim().toLowerCase();
    let res = document.getElementById('train-res');
    let r = await fetch('/api/check_trainer', {
        method: 'POST',
        body: new URLSearchParams({user_ans: ans, correct_ans: currentTrainer.en.toLowerCase()})
    });
    let d = await r.json();
    if (d.status === 'success') {
        res.innerText = '✅ Отлично! +10 монет';
        res.style.color = 'green';
        updateCoins();
        setTimeout(loadTrainer, 1500);
    } else {
        res.innerText = '❌ Ошибка. Правильно: ' + currentTrainer.en;
        res.style.color = 'red';
    }
}

async function translateText() {
    let val = document.getElementById('trans-input').value.trim().toLowerCase();
    let r = await fetch('/api/translate', {
        method: 'POST',
        body: new URLSearchParams({text: val})
    });
    let d = await r.json();
    document.getElementById('trans-output').innerText = d.result;
}

async function loadLessons() {
    let r = await fetch('/api/get_lessons');
    let list = await r.json();
    let container = document.getElementById('lessons-list');
    container.innerHTML = '';
    list.forEach((l) => {
        let box = document.createElement('div');
        box.className = 'lesson-box';
        box.innerHTML = '<h3>' + l.title + '</h3><p>' + l.task + '</p>';
        let chipBlock = document.createElement('div');
        chipBlock.style.margin = '10px 0';
        l.words.forEach(w => {
            let chip = document.createElement('span');
            chip.className = 'word-chip';
            chip.innerText = w;
            chip.onclick = () => {
                selectedWords.push(w);
                ansDisplay.innerText = selectedWords.join(' ');
            };
            chipBlock.appendChild(chip);
        });
        box.appendChild(chipBlock);
        let ansDisplay = document.createElement('div');
        ansDisplay.style.fontStyle = 'italic';
        ansDisplay.style.margin = '10px 0';
        ansDisplay.innerText = 'Ваш ответ...';
        box.appendChild(ansDisplay);
        let checkBtn = document.createElement('button');
        checkBtn.className = 'action-btn';
        checkBtn.style.maxWidth = '150px';
        checkBtn.innerText = 'Проверить';
        checkBtn.onclick = async () => {
            let userStr = selectedWords.join(' ');
            let res = await fetch('/api/check_lesson', {
                method: 'POST',
                body: new URLSearchParams({user_ans: userStr, correct_ans: l.correct})
            });
            let d = await res.json();
            if(d.status === 'success') {
                alert('Урок пройден успешно! +10 монет');
                updateCoins();
            } else {
                alert('Неверно. Попробуйте еще раз.');
            }
            selectedWords = [];
            ansDisplay.innerText = 'Ваш ответ...';
        };
        box.appendChild(checkBtn);
        container.appendChild(box);
    });
}

// Вызываем обновление монет при первой загрузке страницы
updateCoins();
async function loadStats() {
    let r = await fetch('/api/get_stats');
    let d = await r.json();
    document.getElementById('stat-quiz').innerText = d.quiz_score;
    document.getElementById('stat-train').innerText = d.train_score;
    document.getElementById('stat-lessons').innerText = d.lessons_completed;
}

loadQuiz();
loadTrainer();
loadLessons();
updateCoins();
</script>
</body>
</html>
"""


class AdvancedRouterHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        url_path = urlparse(self.path).path

        if url_path == "/api/get_stats":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(session_data).encode("utf-8"))
            return

        if url_path == "/api/get_quiz":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(random.choice(DB_QUIZ)).encode("utf-8"))
            return

        if url_path == "/api/get_word":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(random.choice(DB_WORDS)).encode("utf-8"))
            return

        if url_path == "/api/get_lessons":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(DB_LESSONS).encode("utf-8"))
            return

        if url_path == "/" or url_path == "/index.html" or not url_path.startswith("/api/"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CODE.encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        url_path = urlparse(self.path).path
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(post_data)

        if url_path == "/api/check_quiz":
            user_idx = params.get("index", [""])[0]
            correct_idx = params.get("correct", [""])[0]
            if user_idx == correct_idx:
                session_data["quiz_score"] += 1
                response = {"status": "success"}
            else:
                response = {"status": "fail"}
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        if url_path == "/api/check_trainer":
            user_ans = params.get("user_ans", [""])[0]
            correct_ans = params.get("correct_ans", [""])[0]
            if user_ans == correct_ans:
                session_data["train_score"] += 1
                response = {"status": "success"}
            else:
                response = {"status": "fail"}
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        if url_path == "/api/translate":
            text = params.get("text", [""])[0]
            result = TRANSLATE_DICT.get(text, "Фраза не найдена в словаре")
            response = {"result": result}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        if url_path == "/api/check_lesson":
            user_ans = params.get("user_ans", [""])[0]
            correct_ans = params.get("correct_ans", [""])[0]
            if user_ans == correct_ans:
                session_data["lessons_completed"] += 1
                response = {"status": "success"}
            else:
                response = {"status": "fail"}
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 8000))
    server = http.server.HTTPServer(('0.0.0.0', PORT), AdvancedRouterHandler)
    print(f"Сервер успешно запущен на порту {PORT}")
    server.serve_forever()
