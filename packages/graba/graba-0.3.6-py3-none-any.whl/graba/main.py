import random
import string
from datetime import date, datetime, timedelta
from dateutil.parser import parse

class Any():

    def __init__(self, fuzzy_mode: bool=False):
        self._fuzzy_mode = fuzzy_mode

    def of(self, options: list):
        return random.choice(options)


    def listOf(self, min, max, factoryFunction):
        result = []
        amount = int(self.positiveNumber(min, max))
        for i in range(0, amount):
            data = factoryFunction()
            result.append(data)

        return result

    def subsetOf(self, min, max, items):
        items_randomized = random.sample(items, len(items))
        if min == None:
            min=1
        if max == None or max > len(items):
            max=len(items)-1

        amount_to_get = int(self.positiveNumber(min=min, max=max))
        return items_randomized[:amount_to_get]

    def positiveNumber(self, min: int = 0, max=9999) -> int:
        number=random.randrange(min, max)
        if self._fuzzy_mode == True:
            return self.of([int(number), str(number), float(number)])

        return number

    def negativeNumber(self, min: int = -9999, max=0) -> int:
        number = random.randrange(min, max)

        if self._fuzzy_mode == True:
            return self.of([int(number), str(number), float(number)])

        return number

    def anyNumber(self) -> int:
        return self.of([self.positiveNumber(), self.negativeNumber()])

    def rating(self) -> int:
        number = self.positiveNumber(min=0, max=5)

        if self._fuzzy_mode == True:
            return self.of([int(number), str(number), float(number)])

        return number

    def anyLetter(self) -> str:
        letter = self.of(list(string.ascii_lowercase))

        if self._fuzzy_mode == True:
            return self.of([f" {letter}", letter, f"{letter} ", f" {letter} "])

        return letter

    def word(self, min = 1, max = 30) -> str:
        length = int(self.positiveNumber(min, max))
        alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]

        word = ''.join(random.choice(alphabet) for i in range(length))

        if self._fuzzy_mode == True:
            return self.of([f" {word}", word, f"{word} ", f" {word} "])

        return word

    def sentence(self, min_words: int = 1, max_words: int = 5) -> str:
        amount_words = self.positiveNumber(min=min_words, max=max_words)
        words=[]
        for i in range(amount_words):
            words.append(Any.word())

        sentence = ' '.join(words)

        if self._fuzzy_mode == True:
            return self.of([f" {sentence}", sentence, f"{sentence} ", f" {sentence} "])

        return sentence

    def bytes(self, min=1, max=30) -> bytes:
        word = self.word(min, max)
        return word.encode('UTF-8')


    def url(self, min=1, max=4) -> str:
        length = self.positiveNumber(min, max)
        words = []
        for i in range(length):
            words.append(Any.word())

        return "http://www/"+'.'.join(words)

    def bool(self) -> bool:
        boolean = self.of([True, False])
        if self._fuzzy_mode == True:
            return self.of([boolean, "true", "True", 1, "false", "False", 0])

        return boolean

    def null(self):
        if self._fuzzy_mode == True:
            return self.of([None, "None", "none", "null"])

        return None


    def dateTimeInPast(self) -> datetime:
        now = datetime.now()
        return now - timedelta(days = int(self.positiveNumber()))


    def dateTimeInFuture(self) -> datetime:
        now = datetime.now()
        return now + timedelta(days=int(self.positiveNumber()))

    def dateTimeBefore(self, beforeDateTime) -> datetime:
        if isinstance(beforeDateTime, str):
            beforeDateTime = parse(beforeDateTime, fuzzy=True)

        return beforeDateTime - timedelta(days=int(self.positiveNumber()))

    def dateTimeAfter(self, afterDateTime) -> datetime:
        if isinstance(afterDateTime, str):
            afterDateTime = parse(afterDateTime, fuzzy=True)

        return afterDateTime + timedelta(days=int(self.positiveNumber()))

    def datetimeBetween(self, from_datetime, to_datetime) -> datetime:
        if isinstance(from_datetime, str):
            from_datetime = parse(from_datetime, fuzzy=True)

        if isinstance(to_datetime, str):
            to_datetime = parse(to_datetime, fuzzy=True)

        from_datetime_ts = from_datetime.timestamp()
        to_datetime_ts = to_datetime.timestamp()

        random_ts_between = int(self.positiveNumber(min=from_datetime_ts, max=to_datetime_ts))

        return datetime.fromtimestamp(random_ts_between)

    def dateTime(self) -> datetime:
        return self.of([self.dateTimeInPast(), self.dateTimeInFuture()])

    def date(self) -> date:
        return self.dateTime().date()

    def latitude(self, min: int = None, max: int = None) -> str:
        min=-90 if min == None else min
        max=90  if max == None else max
        decimal_places = 4
        random_lat = random.uniform(min, max)

        return f"{round(random_lat, decimal_places)}"

    def longitude(self, min: int = None, max: int = None) -> str:
        min = -180 if min == None else min
        max =  180 if max == None else max
        decimal_places = 4
        random_lat = random.uniform(min, max)

        return f"{round(random_lat, decimal_places)}"
