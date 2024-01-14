class ContactFormEntity:
    def __init__(self, name, email, message, sent_on):
        self.name = name
        self.email = email
        self.message = message
        self.sent_on = sent_on

    def get_current(self):
        return {
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "sent_on": self.sent_on
        }