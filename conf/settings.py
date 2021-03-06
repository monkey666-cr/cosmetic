import os
import time
import configparser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

conf_path = os.path.join(BASE_DIR, "conf.ini")
if not os.path.exists(conf_path):
    conf_path = input("请输入配置文件路径(conf.ini.backup): \r\n")
    if not os.path.exists(conf_path):
        print(f"{conf_path} 不存在, 5秒后退出程序~ <> ~")
        time.sleep(5)
        exit(0)

conf = configparser.ConfigParser()

conf.read(conf_path, encoding="utf-8")

thread_conf = {item[0]: item[1] for item in conf.items('threading')}

proxy_conf = {item[0]: item[1] for item in conf.items("proxy")}
PROXY_HOST = proxy_conf.get("host")
PROXY_PORT = proxy_conf.get("port")


# 解析任务配置


def format_lambda(x): return {x[index][1]: {"min": float(x[index + 1][1]), "max": float(x[index + 2][1])}
                              for index in range(0, len(x), 3)}


# goldapple
GOLD_GROUP = format_lambda(conf.items('gold apple'))
# rive
RIVE_GROUP = format_lambda(conf.items('rive'))
# letu
LETU_GROUP = format_lambda(conf.items('letu'))
# iledebeaute
ILEDEBEAUTE_GROUP = format_lambda(conf.items('iledebeaute'))
# lancome
LANCOME_GROUP = format_lambda(conf.items("lancome"))
# clarins
CLARINS_GROUP = format_lambda(conf.items("clarins"))
# sephora
SEPHORA_GROUP = format_lambda(conf.items("sephora"))

# 邮箱配置
email_conf = {item[0]: item[1] for item in conf.items('email')}

# clarins 账号配置
CLARINS_ACCOUNT = conf.items("clarins account")[0][1]
CLARINS_PASSWORD = conf.items("clarins account")[1][1]

MAX_WORKS = int(thread_conf.get('max_works', 10))
INTERVAL = int(thread_conf.get('interval', 300))

try:
    USER = email_conf['user']
    PASSWORD = email_conf['password']
    SENDER = email_conf['sender']
    RECEIVER = email_conf['receiver'].split(",")
    SENDER_NAME = email_conf['sender_name']
except Exception as e:
    print(f"Load Email Conf Failed: {str(e)}")
    exit(0)
