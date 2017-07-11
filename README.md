# Что это такое
~~Сам не знаю~~ Приложение для парсинга логов nginx с последующей записи данных в БД.

# Как запускать
для начала рекомендуется установить виртуальное окружение, 
```bash
virtualenv -p python3 venv
source venv/bin/activate
```
затем установить необходимые библиотеки
```bash
pip install -r requirements.txt
```
и запустить командой:
```bash
python main.py /path/to/nginx/log/access.log
```

# Как настраивать
Все настройки хранятся в файле `settings.py`.