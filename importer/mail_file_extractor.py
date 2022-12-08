import os
import pprint
import ssl
from csv import DictReader
from datetime import datetime
from io import BytesIO, StringIO
from zipfile import ZipFile

from dotenv import load_dotenv
from imap_tools import MailBoxTls, AND
from sqlalchemy import select

from base import session_factory
from models.mystrom_device import MystromDevice
from models.mystrom_result import MystromResult


class MailFileExtractor:

    def __init__(self):
        load_dotenv()
        self.session = session_factory()
        self.device = None

    def load_mails(self):

        try:
            mail_server = os.getenv('MAIL_SERVER')
            mail_server_port = os.getenv('MAIL_SERVER_PORT')
            mail_user = os.getenv('MAIL_USER')
            mail_passwd = os.getenv('MAIL_PASSWD')
            mail_inbox = os.getenv('MAIL_INBOX')

            # Load system's trusted SSL certificates
            ssl_context = ssl.create_default_context()

            with MailBoxTls(mail_server,
                            ssl_context=ssl_context,
                            port=mail_server_port).login(mail_user,
                                                         mail_passwd,
                                                         mail_inbox) as mailbox:
                self.process_mailbox(mailbox)

        except Exception as e:
            self.session.rollback()
            pprint.pprint(e)

        self.session.commit()

    def process_mailbox(self, mailbox):
        for msg in mailbox.fetch(AND(from_='noreply@mystrom.ch')):
            self.process_message(msg)

    def process_message(self, msg):
        for att in msg.attachments:
            if att.filename != 'reports.zip':
                continue
            self.process_attachment(att)

    def process_attachment(self, att):
        zipfile = ZipFile(BytesIO(att.payload))
        for zipped_file_name in zipfile.filelist:
            content = zipfile.read(zipped_file_name)
            self.process_csv_file(content)

    def process_csv_file(self, content):
        self.device = None
        reader = DictReader(StringIO(content.decode()))
        for row in reader:
            self.process_row(row)

    def process_row(self, row):
        if not self.device:
            self.find_or_create_device(row)

        self.find_or_create_result(row)

    def find_or_create_result(self, row):
        res = MystromResult()
        res.device_id = self.device.id
        res.date = datetime.fromisoformat(row['time'])
        res.power = row['power (Watt)']
        res.ws = row['energy (Ws)']
        res.temperature = row['temperature']
        result = self.session.scalars(select(
            MystromResult).where(
            MystromResult.date == res.date))
        if not result.first():
            self.session.add(res)

    def find_or_create_device(self, row):
        devices = self.session.scalars(select(
            MystromDevice).where(
            MystromDevice.name == row[
                'device_label']))
        first_device = devices.first()
        if first_device:
            self.device = first_device
        else:
            self.device = MystromDevice()
            self.device.name = row['device_label']
            self.device.active = True
            self.session.add(self.device)
            self.session.flush()
