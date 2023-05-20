import imaplib
import email
import os


class EmailConnect:

    def __init__(self):
        self.username = "ejlacsamana.dev@gmail.com"
        self.password = "qpbdkzojhykmkevh"
        self.server = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.login = self.server.login(self.username, self.password)

    def scrapeInbox(self):
        subject_filter = "Letter Sending Request"
        self.server.select("INBOX")
        status, data = self.server.search(
            None, f'(SUBJECT "{subject_filter}")')
        if status == "OK":
            email_ids = data[0].split()
            for email_id in email_ids:
                typ_data, msg_data = self.server.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        for part in msg.walk():
                            if part.get_content_disposition() is not None:
                                filename = part.get_filename()
                                if filename:
                                    filepath = os.path.join(
                                        './attachments', filename)
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))
                                    return "Downloaded attachment"

    def downloadAttachment(self):
        pass


emailing = EmailConnect()
print(emailing.scrapeInbox())
