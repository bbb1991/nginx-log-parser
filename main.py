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
        print(request[0])
        req_ip, balancer_ip, req_date, req_type, url, code, size, _,  time = request[0]

        if not url.startswith("/court"):
            continue

        log_entry = LogModel(req_ip, datetime.strptime(req_date, settings.DATETIME_FORMAT), url, code, size, time)
        session.add(log_entry)
    session.commit()
    session.close()


def get_requests(f):
    log_lines = f.readlines()
    lines = []

    pat = (r''
           '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})\s([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})\s'
           '\[(.+)\]\s'  # datetime
           '"(GET|POST)\s(.+)\s\w+/.+"\s'  # requested type and file
           '(\d+)\s'  # status
           '(\d+)\s'  # bandwidth
           '"(.+)"\s'  # referrer and user-agent
           '(.+)'  # time process
           )

    for line in log_lines:
        lines.append(find(pat, line))

    return lines


def find(pat, text):
    match = re.findall(pat, text)
    if match:
        return match
    return False


if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError('Give me path to Nginx logs!')

    log_file = open(sys.argv[1], 'r')
    process_log(log_file)
    log_file.close()
