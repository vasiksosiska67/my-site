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
]

DB_WORDS = [
    {"ru": "красивый", "en": "beautiful"},
    {"ru": "журнал", "en": "magazine"},
    {"ru": "точный", "en": "accurate"},
]

DB_LESSONS = [
    {
        "id": 1,
        "title": "Урок 1: Знакомство",
        "task": "Соберите фразу: 'Я из Беларуси'",
        "words": ["from", "I", "Belarus", "am"],
        "correct": "I am from Belarus",
    },
    {
        "id": 2,
        "title": "Урок 2: О себе",
        "task": "Соберите фразу: 'Мне нравится английский'",
        "words": ["English", "like", "I"],
        "correct": "I like English",
    },
    {
        "id": 3,
        "title": "Урок 3: Работа",
        "task": "Соберите фразу: 'Я работаю здесь'",
        "words": ["work", "here", "I"],
        "correct": "I work here",
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
        body { background: #f0f2f5; color: #333; padding-bottom: 60px; }
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
        <div id="quiz" class="tab-content active">
            <div class="card">
                <h2>Проверка знаний (Идиомы)</h2>
                <div class="quiz-question" id="quiz-q">Загрузка...</div>
                <div class="quiz-options" id="quiz-opts"></div>
                <div class="result" id="quiz-res"></div>
            </div>
        </div>
        <div id="trainer" class="tab-content">
            <div class="card">
                <h2>Тренажер правописания</h2>
                <div class="trainer-prompt" id="train-q">Загрузка...</div>
                <input type="text" id="train-input" placeholder="Введите ответ на английском" autocomplete="off">
                <div style="max-width: 200px; margin: 0 auto;">
                    <button class="action-btn" onclick="checkTrainer()">Проверить</button>
                </div>
                <div class="result" id="train-res"></div>
            </div>
        </div>
        <div id="translator" class="tab-content">
            <div class="card">
                <h2>Онлайн-переводчик фразеологизмов</h2>
                <p style="margin-bottom: 15px; color:#666;">Введите фразу на русском:</p>
                <textarea id="trans-input" rows="2" placeholder="Введите текст на русском..."></textarea>
                <div style="max-width: 200px; margin: 10px auto;">
                    <button class="action-btn" onclick="translateText()">Перевести</button>
                </div>
                <div class="trainer-prompt" style="margin-top:15px;">Результат перевода:</div>
                <div id="trans-output" style="font-size:1.3rem; color:#2a5298; font-weight:bold; min-height:30px;"></div>
            </div>
        </div>
        <div id="lessons" class="tab-content">
            <div class="card">
                <h2>Интерактивные уроки</h2>
                <div id="lessons-list"></div>
            </div>
        </div>
        <div id="profile" class="tab-content">
            <div class="card">
                <h2>Ваш прогресс в этой сессии</h2>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div>Квиз</div>
                        <div class="stat-val" id="stat-quiz">0</div>
                    </div>
                    <div class="stat-item">
                        <div>Слова</div>
                        <div class="stat-val" id="stat-train">0</div>
                    </div>
                    <div class="stat-item">
                        <div>Уроки</div>
                        <div class="stat-val" id="stat-lessons">0</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        let currentQuiz = {}, currentTrainer = {}, currentLesson = {}, selectedWords = [];
        
        function switchTab(t) {
            document.querySelectorAll('.tab-content').forEach(e => e.classList.remove('active'));
            document.querySelectorAll('nav button').forEach(e => e.classList.remove('active'));
            document.getElementById(t).classList.add('active');
            document.getElementById('btn-' + t).classList.add('active');
            if (t === 'profile') loadStats();
        }

        async function loadQuiz() {
            let r = await fetch('/api/get_quiz');
            currentQuiz = await r.get_quiz ? await r.json() : await r.json();
            document.getElementById('quiz-q').innerText = currentQuiz.q;
            let opts = document.getElementById('quiz-opts');
            opts.innerHTML = '';
            document.getElementById('quiz-res').innerText = '';
            currentQuiz.a.forEach((ans, idx) => {
                let btn = document.createElement('button');
                btn.className = 'action-btn';
                btn.innerText = ans;
                btn.onclick = () => checkQuiz(idx);
                opts.appendChild(btn);
            });
        }

        async function checkQuiz(idx) {
            let res = document.getElementById('quiz-res');
            let r = await fetch('/api/check_quiz', {
                method: 'POST',
                body: new URLSearchParams({index: idx, correct: currentQuiz.c})
            });
            let d = await r.json();
            if (d.status === 'success') {
                res.innerText = '✅ Правильно!';
                res.style.color = 'green';
            } else {
                res.innerText = '❌ Неверно. Правильный ответ: ' + currentQuiz.a[currentQuiz.c];
                res.style.color = 'red';
            }
            setTimeout(loadQuiz, 2000);
        }

        async function loadTrainer() {
            let r = await fetch('/api/get_word');
            currentTrainer = await r.json();
            document.getElementById('train-q').innerText = 'Как переводится: "' + currentTrainer.ru + '"?';
document.getElementById('train-input').value = '';
document.getElementById('train-res').innerText = '';
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
res.innerText = '✅ Отлично!';
res.style.color = 'green';
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
alert('Урок пройден успешно!');
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
