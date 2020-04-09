class TestManager(object):
    def __init__(self):
        self._questions = dict()
        self._answers = dict()
        self._tempQuestions = list()
        self._mistakesAnswers = dict()

    def setQuestions(self, questions):
        self._questions = questions

    def setAnswers(self, answer):
        self._answers.update({answer[0]: answer[1]})

    def setTempQuestions(self, questions):
        self._tempQuestions = questions

    def tempQuestions(self):
        return self._tempQuestions

    def mistakesAnswers(self):
        return self._mistakesAnswers

    def check(self):
        correct = 0
        incorrect = 0
        # rights = list()
        # wrongs = list()

        # for question in self._questions:
        #     if self._answers.get(question) in self._questions.get(question).split(', '):
        #         correct += 1
        #         rights.append(question)
        #     else:
        #         incorrect += 1
        #         wrongs.append(question)

        # for right in rights:
        #     if right in self._mistakesAnswers:
        #         del self._mistakesAnswers[right]

        # for wrong in wrongs:
        #     if wrong not in self._mistakesAnswers:
        #         self._mistakesAnswers.update({wrong:self._questions.get(wrong)})

        for question in self._questions:
            if self._answers.get(question) in self._questions.get(question).split(', '):
                correct += 1
                del self._mistakesAnswers[question]
            else:
                incorrect += 1
                self._mistakesAnswers.update({question: self._questions.get(question)})

        self._questions.clear()
        self._answers.clear()
        self._tempQuestions.clear()

        # return (correct, incorrect)
        return correct
