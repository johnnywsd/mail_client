import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import sys
import logging

STMP_HOST = "smtp.gmail.com"
STMP_PORT = 587
IMAP4_SSL_HOST = 'imap.gmail.com'


def send_Gmail(gmail_account, gmail_password, to_str, subject_str,
               text_html_str, sender_name='Info',
               attach_path_str=None):
        """
        Send via Gmail
        """

        msg = MIMEMultipart()
        from_header = ('\"%s\" <' + gmail_account + '>') % sender_name

        msg['From'] = from_header
        msg['To'] = to_str
        msg['Subject'] = subject_str

        msg.attach(MIMEText(text_html_str, 'html'))

        if attach_path_str:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attach_path_str, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' \
                            % os.path.basename(attach_path_str))
            msg.attach(part)

        to_list = [to_str]

        mailServer = smtplib.SMTP(STMP_HOST, STMP_PORT)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmail_account, gmail_password)
        mailServer.sendmail(gmail_account, to_list, msg.as_string())
        mailServer.quit()


if __name__ == '__main__':
    usage = 'python mail_client.py <your_gmail_account> \
        <your_gmail_password> <reciever_email_account> <subject>\
        <content_as_html> [your name] [attachment_path]'
    logging.basicConfig(
        filename='mail_client.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)-5.5s]  %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    try:
        if len(sys.argv) > 6:
            gmail_account = sys.argv[1]
            gmail_password = sys.argv[2]
            to_str = sys.argv[3]
            subject_str = sys.argv[4]
            text_html_str = sys.argv[5]
            sender_name = 'Info'
            attach_path_str = None
            if len(sys.argv) == 7:
                sender_name = sys.argv[6]
            if len(sys.argv) == 8:
                sender_name = sys.argv[6]
                attach_path_str = sys.argv[7]
        send_Gmail(gmail_account, gmail_password,
                   to_str, subject_str, text_html_str,
                   sender_name, attach_path_str)
        logging.info("Email has been sent to %s", to_str)
    except:
        logging.error(usage)
