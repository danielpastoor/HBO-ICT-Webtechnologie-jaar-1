import re


class SpamFilter:
    def __init__(self):
        self.spam_keywords = ["free", "click here", "buy now", "subscribe", "credit", "loan"]
        self.spam_threshold = 0.05  # 5% of the words in the message
        self.url_regex = r'https?://\S+'
        self.domain_blacklist = ["spamdomain.com", "freespam.net"]

    def is_spam(self, message, email):
        return (self.check_keywords(message) or
                self.check_links(message) or
                self.check_suspicious_patterns(message) or
                self.check_domain_blacklist(email))

    def check_keywords(self, message):
        words = message.lower().split()
        spam_count = sum(word in self.spam_keywords for word in words)
        return spam_count / len(words) > self.spam_threshold

    def check_links(self, message):
        urls = re.findall(self.url_regex, message)
        return len(urls) > 2  # More than 2 URLs could be suspicious

    def check_suspicious_patterns(self, message):
        return bool(re.search(r'(!{2,})|(ALL CAPS)', message))

    def check_domain_blacklist(self, email):
        domain = email.split('@')[-1]
        return domain in self.domain_blacklist
