import logging
import csv
import io
from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.request_method = request.method
            record.request_path = request.path
            record.ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            record.host = request.host.split(':', 1)[0]
            record.args = dict(request.args)

        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        self.writer.writerow([record.levelname, record.msg])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logging.root.handlers[0].setFormatter(CsvFormatter())

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('The file has been updated.')
logging.info('have a great day.')
logging.warning('please upload in the formal required.')