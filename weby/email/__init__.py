import smtplib
import email


def send_email(sender, recipient, subject, body, send=True):
    message = email.mime.text.MIMEText(body)

    message[u'Subject'] = subject
    message[u'From'] = sender
    message[u'To'] = recipient

    if send:
        s = smtplib.SMTP()
        s.connect()
        s.sendmail(sender, [recipient], message.as_string())
        s.close()

    return message

#TODO: jperla: allow creation of html and mixed emails
def create_text_message(sender, recipients, subject, body):
    message = email.mime.text.MIMEText(body)

    message[u'Subject'] = subject
    message[u'From'] = sender
    #TODO: jperla: allow this to be more complicated:
    # i.e. tuples of (name,email)
    message[u'To'] = u', '.join(recipients)

    return message

def sender_and_recipients_from_message(message, bcc=None):
    bcc = [] if bcc is None else bcc
    sender = message[u'From']
    #TODO: jperla: strip out emails between <> maybe?
    recipients = [e.strip() for e in message[u'To'].split(u',')]
    recipients.extend(bcc)
    return sender, recipients


class MailServer(object):
    def __init__(self):
        raise NotImplementedError

    def send_message(self):
        raise NotImplementedError


class LocalMailServer(object):
    def __init__(self):
        pass
    
    def send_message(self, message, bcc=None):
        sender, recipients = sender_and_recipients_from_message(message)
        s = smtplib.SMTP()
        s.connect()
        s.sendmail(sender, recipients, message.as_string())
        s.close()

class TestMailServer(object):
    def __init__(self):
        self.sent_email = []
    
    def send_message(self, message, bcc=None):
        sender, recipients = sender_and_recipients_from_message(message)
        self.sent_email.append((message, sender, recipients,))

