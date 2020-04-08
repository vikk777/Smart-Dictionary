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

        for answer in self._questions:

            if self._answers.get(answer) in self._questions.get(answer).split(', '):
                correct = correct + 1

                if answer in self._mistakesAnswers:
                    del self._mistakesAnswers[answer]

            else:
                incorrect = incorrect + 1

                if not (answer in self._mistakesAnswers):
                    self._mistakesAnswers[answer] = self._questions.get(answer)

        # return (correct, incorrect)
        return correct
