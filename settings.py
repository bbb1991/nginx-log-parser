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

# Начиная с какого времени нас интересует лог (включительно)
# если не нужно фильтровать, необходимо значение присвоить None
BEGIN_DATE = "12/Jul/2017:09:00:00 +0600"

# До какого времени (включительно)
# если не нужно фильтровать, необходимо значение присвоить None
END_DATE = None

TEST_SERVER_LOG_FORMAT = '$remote_addr - $remote_user [$time_local] "$request" ' \
                         '$status $body_bytes_sent "$http_referer" ' \
                         '"$http_user_agent" "$http_x_forwarded_for"'

PROD_SERVER_LOG_FORMAT = '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent ' \
                         '"$http_referer" ' \
                         '"$http_user_agent" "$http_x_forwarded_for" "upstream_response_time" "$upstream_response_time"'

# В каком формате nginx пишет логи
LOG_FORMAT = PROD_SERVER_LOG_FORMAT
