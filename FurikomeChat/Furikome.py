import os
from watson_developer_cloud import NaturalLanguageClassifierV1

class Furikome:
    def __init__(self):
        self.natural_language_classifier = NaturalLanguageClassifierV1(
            username=os.environ["USER_ID"],
            password=os.environ["USER_PASS"])

    def judge(self, content):
        result = self.request(content)
        status = result["top_class"]
        return status

    def request(self, content):
        classes = self.natural_language_classifier.classify('beb9bfx46-nlc-100', content)
        return classes

if __name__ == "__main__":
    f = Furikome()
    print(f.judge("こんにちは"))
    print(f.judge("振り込んで"))
