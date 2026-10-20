import http.server
import json
import random
import socketserver
import threading
import tkinter as tk
import webbrowser
from urllib.parse import parse_qs

PORT = 8095

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
    "привет": "hello",
    "как дела": "how are you",
    "спасибо": "thank you",
    "пожалуйста": "please",
    "я люблю программировать": "i love programming",
    "английский язык": "english language",
    "я учусь": "i am learning",
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
        <button class="active" onclick="switchTab('quiz')">🧩 Квиз</button>
        <button onclick="switchTab('trainer')">✍️ Тренажер</button>
        <button onclick="switchTab('translator')">🌐 Переводчик</button>
        <button onclick="switchTab('lessons')">🦉 Уроки Duolingo</button>
        <button onclick="switchTab('profile')">👤 Кабинет</button>
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
                <p style="margin-bottom: 15px; color:#666;">Введите фразу на русском (например: привет, как дела, я учусь):</p>
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
        let currentQuizData = null, currentTrainerData = null;
        function switchTab(t) {
            document.querySelectorAll('.tab-content').forEach(e => e.classList.remove('active'));
            document.querySelectorAll('nav button').forEach(e => e.classList.remove('active'));
            document.getElementById(t).classList.add('active');
            event.currentTarget.classList.add('active');
            if (t === 'profile') updateStats();
            if (t === 'lessons') loadLessons();
        }
        function loadNextQuiz() {
            document.getElementById('quiz-res').textContent = "";
            fetch('/api/get_quiz').then(r => r.json()).then(d => {
                currentQuizData = d;
                document.getElementById('quiz-q').textContent = d.q;
                const o = document.getElementById('quiz-opts');
                o.innerHTML = "";
                d.a.forEach((opt, i) => {
                    let b = document.createElement('button');
                    b.className="action-btn";
                    b.textContent = opt;
                    b.onclick = () => submitQuizAnswer(i);
                    o.appendChild(b);
                });
            });
        }
        function submitQuizAnswer(i) {
            fetch('/api/check_quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `index=${i}&correct=${currentQuizData.c}`
            }).then(r => r.json()).then(res => {
                const rD = document.getElementById('quiz-res');
                if (res.status === 'success') {
                    rD.style.color = "#2ecc71";
                    rD.textContent = "🎉 Правильно!";
                    setTimeout(loadNextQuiz, 1000);
                } else {
                    rD.style.color = "#e74c3c";
                    rD.textContent = "❌ Неверно!";
                }
            });
        }
        function loadNextWord() {
            document.getElementById('train-input').value = "";
"""


class AdvancedRouterHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CODE.encode("utf-8"))
            return
        if self.path == "/api/get_quiz":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(random.choice(DB_QUIZ)).encode("utf-8"))
            return
        if self.path == "/api/get_word":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(random.choice(DB_WORDS)).encode("utf-8"))
            return
        if self.path == "/api/get_lessons":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            payload = {
                "lessons": DB_LESSONS,
                "completed": session_data["lessons_completed"],
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return
        if self.path == "/api/get_stats":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(session_data).encode("utf-8"))
            return
        self.send_error(404, "Not Found")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(post_data)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        if self.path == "/api/check_quiz":
            if params.get("index", [""]) == params.get("correct", [""]):
                session_data["quiz_score"] += 1
                response = {"status": "success"}
            else:
                response = {"status": "fail"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        if self.path == "/api/check_word":
            user = params.get("user_answer", [""]).strip().lower()
            corr = params.get("correct_answer", [""]).strip().lower()
            if user == corr:
                session_data["train_score"] += 1
                response = {"status": "success"}
            else:
                response = {"status": "fail"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        if self.path == "/api/translate":
            text = params.get("text", [""]).strip().lower()
            translated = TRANSLATE_DICT.get(
                text,
                "Фраза не найдена в демо-словаре. Попробуйте 'привет' или 'я учусь'",
            )
            self.wfile.write(json.dumps({"result": translated}).encode("utf-8"))
            return

        if self.path == "/api/check_lesson":
            les_id = int(params.get("id", ["0"]))
            ans = params.get("answer", [""]).strip()
            correct_ans = next(
                (l["correct"] for l in DB_LESSONS if l["id"] == les_id), ""
            )
            if ans == correct_ans:
                if session_data["lessons_completed"] < les_id:
                    session_data["lessons_completed"] = les_id
                response = {"status": "success"}
            else:
                response = {"status": "fail"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return


def start_server():
    with socketserver.TCPServer(("", PORT), AdvancedRouterHandler) as httpd:
        httpd.serve_forever()


def open_site():
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    open_site()
    root = tk.Tk()
    root.title("English Server Ultimate")
    root.geometry("350x120")
    tk.Label(
        root, text="Сервер English Ultimate запущен!", font=("Arial", 11, "bold")
    ).pack(pady=15)
    tk.Button(
        root,
        text="Перейти на сайт",
        font=("Arial", 11),
        bg="#1e3c72",
        fg="white",
        command=open_site,
    ).pack(pady=5)
    root.mainloop()
