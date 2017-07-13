import pprint

__author__ = "Bagdat Bimaganbetov"
__email__ = "bagdat.bimaganbetov@gmail.com"
__license__ = "MIT"

import re
import sys
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import settings
from model import LogModel, Base


def should_write_line(dt, url):
    """
    Метод для проверки строки лога.
    По условию записываем только те строки, у которых :param url начинается с определенной строки
    и к тому же за определенный промежуток времени.
    :param dt: дата создания запроса
    :param url: куда был отправлен запрос
    :return: True, если нужно прошли все проверки и нужно записать, иначе False
    """
    if not url.startswith("/court"):  # Начинается ли строка с определенной подстроки
        return False
    if settings.BEGIN_DATE:  # Если указана верхняя граница, попадает ли наша строка
        if datetime.strptime(dt, settings.DATETIME_FORMAT) < datetime.strptime(settings.BEGIN_DATE,
                                                                               settings.DATETIME_FORMAT):
            return False
    if settings.END_DATE:  # Если указана нижняя граница, попадает ли наша строка
        if datetime.strptime(dt, settings.DATETIME_FORMAT) > datetime.strptime(settings.END_DATE,
                                                                               settings.DATETIME_FORMAT):
            return False
    return True


def process_log(log_file):
    requests = get_requests(log_file)

    # Создаем коннект к БД
    engine = create_engine(settings.DB_URL, convert_unicode=True)
    engine.echo = settings.DEBUG
    engine.connect()

    # Создаем сессию
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    session = db_session()

    # Создаем таблицу, если нет в БД
    Base.metadata.create_all(engine)

    for x in range(len(requests)):
        request = requests[x]

        if not request: # если метод find не смог спарсить строку, пропускаем
            continue

        request = request.groupdict()

        # Вытаскиваем необходимые поля
        remote_addr = request.get('remote_addr')
        time_local = request.get('time_local')
        url = request.get('request')
        status = request.get('status')
        body_bytes_sent = request.get('body_bytes_sent')
        upstream_response_time = request.get('upstream_response_time')

        # URL разбиваем на части
        try:
            req_type, url, http_protocol = url.split()
        except ValueError:
            try:
                req_type, url = url.split()
            except ValueError:
                continue

        # Проводим необходимые проверки, если хоть одна не прошла, пропускаем строку
        if not should_write_line(time_local, url):
            continue

        # Создаем и записываем в БД
        log_entry = LogModel(remote_addr, req_type, datetime.strptime(time_local, settings.DATETIME_FORMAT), url,
                             status, body_bytes_sent,
                             upstream_response_time)
        session.add(log_entry)
        if x % 1000 == 0:
            session.flush()
            session.commit()

    # После того, как закончили все наши темные делишки, комиттимся
    session.commit()
    session.close()


def get_requests(f):
    log_lines = f.readlines()
    lines = []

    pat = ''.join(
        '(?P<' + g + '>.*?)' if g else re.escape(c)
        for g, c in re.findall(r'\$(\w+)|(.)', settings.LOG_FORMAT))

    for line in log_lines:
        lines.append(find(pat, line))

    return lines


def find(pat, text):
    match = re.match(pat, text)
    if match:
        return match
    return False


if __name__ == '__main__':

    if len(sys.argv) != 2:  # Проверка что передан лог файл
        raise ValueError('Give me path to Nginx logs!')

    log_file = open(sys.argv[1], 'r')
    process_log(log_file)
    log_file.close()
