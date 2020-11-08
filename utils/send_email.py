import smtplib

from email.header import Header
from email.mime.text import MIMEText
from conf.settings import USER, RECEIVER, SENDER, PASSWORD

# {'website': 'Rive', 'product_id': '948720', 'product_name': 'Guerlain Abeille Royale Oil Set', 'low_price': '9015.0', 'price': '6310.0'}

email_format = """
<p>低价通知</p>
<div><p>你关注的网站《{}》的《{}》 已经补货，目前的价钱是《{}》 请及时购买。</p></div>
<p><a href="{}">点击购买</a></p>
"""
sender = SENDER  # 发送者
receivers = [RECEIVER]  # 接收者

user = USER
passwd = PASSWORD  # 发送者的授权码
# email_server = 'smtp.hoperun.com'  # 服务器
email_server = 'smtp.qq.com'  # 服务器


def send_email(url, content=None):
    if content is None:
        print("Send Email Failed!")
        return
    website = content.get("website", "")
    product_name = content.get("product_name", "")
    price = content.get("low_price", -1)

    html = email_format.format(website, product_name, price, url)

    message = MIMEText(html, 'html', 'utf-8')
    message['From'] = Header("奋斗小伙", 'utf-8')  # 发送者
    message['To'] = Header("奋斗小伙", 'utf-8')  # 接收者

    subject = '低价购买通知'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp_obj = smtplib.SMTP()

        smtp_obj.connect(email_server, 25)  # 25 为 SMTP 端口号
        smtp_obj.login(user, passwd)
        smtp_obj.sendmail(sender, receivers, message.as_string())
        print("Email Send Success")
        return True
    except smtplib.SMTPException:
        print("Email Send Failed")

    return False


if __name__ == '__main__':
    send_email("http://www.baidu.com")
