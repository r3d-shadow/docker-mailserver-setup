from imap_tools import MailBox, AND

# Get date, subject and body len of all emails from INBOX folder
with MailBox('mail.example.com').login('admin@mail.example.com', 'PASSWORD') as mailbox:
    for msg in mailbox.fetch():
        print(msg.date, msg.subject, len(msg.text or msg.html))
        print(msg.text)