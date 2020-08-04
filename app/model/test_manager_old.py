from .user import User


class TestManager():
    def __init__(self):
        self._questions = dict()
        self._answers = dict()
        self._tempQuestions = dict()
        self._user = User()

    def init(self, userId):
        if self._questions.get(userId) is None:
            self._questions[userId] = dict()
            self._answers[userId] = dict()
            self._tempQuestions[userId] = list()
            return True
        else:
            return False

    def isInit(self, userId):
        return True if self._questions.get(userId) else False
        # and self._tempQuestions.get(userId) else False

    def setQuestions(self, userId, questions):
        self._questions[userId] = questions
        return True

    def addQuestion(self, userId, question, answer):
        self._questions[userId].update({question: answer})
        return True

    def haveQuestion(self, userId, question):
        return True if self._questions[userId].get(question) else False

    def questions(self, userId):
        return self._questions[userId]

    def setAnswer(self, userId, answer):
        self._answers[userId].update({answer[0]: answer[1]})
        return True

    def setTempQuestions(self, userId, questions):
        self._tempQuestions[userId] = questions
        return True

    def tempQuestions(self, userId):
        return self._tempQuestions.get(userId)

    def mistakes(self, userId):
        words = dict()

        for word in self._user.mistakes(userId):
            words.update({word.original: word.translate})
        return words

    def check(self, userId):
        correct = 0
        total = len(self._questions.get(userId))
        tempMistakes = list()

        for question in self._questions.get(userId):
            if self._answers.get(userId).get(question) in\
                    self._questions.get(userId).get(question).split(', '):
                correct += 1
                if self._user.haveMistake(userId, question):
                    self._user.removeMistake(userId, question)
            else:
                tempMistakes.append({
                    'question': question,
                    'right': self._questions.get(userId).get(question),
                    'wrong': self._answers.get(userId).get(
                        question) or '[empty]'})

        # add mistakes to db
        # do not in loop above because
        # the mistake could be removed by
        # right answer on second question
        for mistake in tempMistakes:
            if not self._user.haveMistake(userId, mistake['question']):
                self._user.addMistake(userId, mistake['question'])

        # self._questions.get(userId).clear()
        # self._answers.get(userId).clear()
        # self._tempQuestions.get(userId).clear()  # will be empty

        del self._questions[userId]
        del self._answers[userId]
        del self._tempQuestions[userId]

        return {'correct': correct,
                'total': total,
                'mistakes': tempMistakes}

    def progress(self, userId):
        """Current step and total steps"""
        return {'current':
                len(self._questions.get(userId)) - len(
                    self._tempQuestions.get(userId)),
                'total':
                len(self._questions.get(userId))}
