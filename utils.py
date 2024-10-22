import time
from datetime import datetime
import requests
from credentials import *

file_name = os.path.basename(__file__)
file_name = os.path.splitext(file_name)[0]


def tg_sendMsg(
    msg: str | list = "no message",
    TOKEN=TG_BOT_TOKEN,
    chat_id=TG_ChatID,
    ps = "\n[send via utils]",
    *,
    sep_msg: bool = False,
) -> str:

    """send message via telegram api(url)\n
    url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    )"""
    # TOKEN = TOKEN
    # chat_id = chat_id
    _ps = ps
    isStr = type(msg) is str
    if isStr:
        msg = msg + _ps
    elif sep_msg and type(msg) == list:
        for m in msg:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={m + _ps}"
            requests.get(url).json()
        return True
    elif not sep_msg and type(msg) != str:
        msg = " \n".join([m for m in msg]) + _ps
    url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    )
    requests.get(url).json()


class Time:
    """Class for retrivig current timestamp\date"""

    def __init__(self) -> None:
        pass

    def get_timeNow(self, strformat: str = "%Y-%m-%d %H:%M:%S.%f") -> str:
        """Return DateTime value\n
        :strformat: default=%Y-%m-%d %H:%M:%S.%f
        """
        self.strformat = strformat
        self.now = datetime.now().strftime(self.strformat)  
        # print(self.now)
        return self.now

    @staticmethod
    def get_timestamp() -> int:
        """Return Timestamp value"""
        timestamp = round(time.time() * 1000)
        # print(timestamp)
        return timestamp

    @staticmethod
    def dt_to_timestamp(dt, strftime="%Y-%m-%d %H:%M:%S") -> int:
        """Convert datetime string to TS\n
        strftime='%Y-%m-%d %H:%M:%S' or strftime='%Y-%m-%d %H:%M:%S.%f' for ms"""
        
        date = datetime.strptime(dt, strftime)
        timestamp = datetime.timestamp(date)
        return round(timestamp)


    @staticmethod
    def ts_to_datetime(ts: int | str) -> str:
        """Convert ts to datetime | lens 1682460360 (seconds)"""
        dt = datetime.fromtimestamp(ts)
        return dt

    @staticmethod
    def get_timeDelta():
        pass


timeNow = Time().get_timeNow()[:-3]


def error_catchLine(
    e: Exception,
    file_path=__file__,
    log_path="exception_errors.txt",
    tg=False,
    log=True,
    show=True
) -> str:
    file_name = os.path.basename(__file__)
    # file_name = os.path.splitext(file_name)
    """Catch exception "type" Error,filepath,line no\n
    e: given Exception from exept block\n
    >>> type(e).__name__           # TypeError
    >>> __file__,                  # /tmp/example.py
    >>> e.__traceback__.tb_lineno  # 2"""
    if show:
        print(
            "*********************************************************\n",
            f"[{timeNow}]" "\tException:\n",
            type(e).__name__,  # TypeError
            e.__traceback__.tb_lineno,
            f'"{e}"',  # message
            "\n",
            file_path,
            "\n*********************************************************",  # /tmp/example.py
        )
    error = f'{timeNow} {type(e).__name__} {str(e.__traceback__.tb_lineno)} "{e}" {file_name}'
    if tg:
        tg_msg = f'[{timeNow}] {type(e).__name__}: \n"{e}" \n{file_name} at line {str(e.__traceback__.tb_lineno)}'
        tg_sendMsg(tg_msg)
    if log:
        with open(log_path, "a") as err:
            err.write(error + "\n")
    return error

# print(Time.ts_to_datetime(1682461254))