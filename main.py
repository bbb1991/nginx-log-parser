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
    if not url.startswith("/court"):
        return False
    if settings.BEGIN_DATE:
        if datetime.strptime(dt, settings.DATETIME_FORMAT) < datetime.strptime(settings.BEGIN_DATE, settings.DATETIME_FORMAT):
            return False
    if settings.END_DATE:
        if datetime.strptime(dt, settings.DATETIME_FORMAT) > datetime.strptime(settings.END_DATE, settings.DATETIME_FORMAT):
            return False
    return True


def process_log(log_file):
    requests = get_requests(log_file)

    engine = create_engine(settings.DB_URL, convert_unicode=True)
    engine.echo = settings.DEBUG
    engine.connect()

    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    session = db_session()

    Base.metadata.create_all(engine)

    for request in requests:

        if not request:
            continue

        request = request.groupdict()

        remote_addr = request['remote_addr']
        time_local = request['time_local']
        url = request['request']
        status = request['status']
        body_bytes_sent = request['body_bytes_sent']
        upstream_response_time = request['upstream_response_time']

        req_type, url, http_protocol = url.split()

        if not should_write_line(time_local, url):
            continue

        log_entry = LogModel(remote_addr, req_type, datetime.strptime(time_local, settings.DATETIME_FORMAT), url,
                             status, body_bytes_sent,
                             upstream_response_time)
        session.add(log_entry)

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

    if len(sys.argv) != 2:
        raise ValueError('Give me path to Nginx logs!')

    log_file = open(sys.argv[1], 'r')
    process_log(log_file)
    log_file.close()
