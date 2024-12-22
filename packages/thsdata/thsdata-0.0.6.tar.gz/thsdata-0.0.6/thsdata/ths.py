from .quote_lib import QuoteLib
from .util import *
from .model import Reply
import re

ZipVersion = "2"


class ThsQuote:
    def __init__(self, quotelib=None):
        # 默认值是None，这样你可以传入一个 QuoteLib 实例
        if quotelib is None:
            self.quotelib = None
        elif isinstance(quotelib, QuoteLib):
            self.quotelib = quotelib
        else:
            raise TypeError("quotelib must be an instance of QuoteLib")

    def historyMinuteTimeData(self, code=str, date=str):
        # 检查code的长度和前四位         # if len(code) != 10 or not (code.startswith('USHA') or code.startswith('USZA')):
        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        # 检查date的格式
        if not re.match(r'^\d{8}$', date):
            raise ValueError("Date must be in the format YYYYMMDD, e.g. 20241220.")

        instance = rand_instance(8)
        zipVersion = ZipVersion
        data_type = "1,10,13,19,40"
        market = code[:4]
        short_code = code[4:]
        req = f"id=207&instance={instance}&zipversion={zipVersion}&code={short_code}&market={market}&datatype={data_type}&date={date}"
        response = self.quotelib.query_data(req.encode('utf-8'))
        if response == "":
            raise ValueError("No history data found.")

        reply = Reply(response)
        reply.convert_data()
        return reply.data
