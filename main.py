from importer.mail_file_extractor import MailFileExtractor


def run():
    extractor = MailFileExtractor()
    extractor.load_mails()


if __name__ == '__main__':
    run()
