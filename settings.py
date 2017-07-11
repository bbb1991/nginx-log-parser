# URL для коннекта к БД
"""
для PostgreSQL: 'postgresql://username:password@domain:5432/database'
Для MySQL: 'mysql://username:password@domain/database'
Для Oracle: 'oracle://username:password@domain:1521/database'

Подробнее в документаций: http://docs.sqlalchemy.org/en/latest/core/engines.html
"""
DB_URL = 'sqlite:///test.sqlite3'

# Таблица, куда следует записать спарсенный лог
DB_TABLE_NAME = 'nginx_log'

# Формат времени в лог файле
DATETIME_FORMAT = "%d/%b/%Y:%X %z"

# Следует ли гадить в консоль
DEBUG = True
