from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Путь к файлу для хранения данных
DATA_FILE = 'data.json'

# Инициализация данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'text': 'Привет, мир!', 'visits': 0}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Загружаем данные при старте приложения
app_data = load_data()

@app.route('/')
def index():
    """Главная страница: отображает текст и увеличивает счетчик посещений."""
    global app_data
    app_data['visits'] += 1
    save_data(app_data)
    return render_template('index.html', display_text=app_data['text'], visits=app_data['visits'])

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Страница настроек: позволяет изменить текст и сбросить счетчик."""
    global app_data
    if request.method == 'POST':
        if 'new_text' in request.form:
            app_data['text'] = request.form['new_text']
        if 'reset_visits' in request.form:
            app_data['visits'] = 0
        save_data(app_data)
        return redirect(url_for('settings')) # Перенаправляем на страницу настроек после сохранения
    return render_template('settings.html', current_text=app_data['text'])

if __name__ == '__main__':
    app.run(debug=True) # debug=True позволяет автоматически перезагружать сервер при изменениях и показывает ошибки