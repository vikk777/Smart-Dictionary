class TestManager(object):
    def __init__(self):
        self._questions = dict()
        self._answers = dict()

    def setQuestions(self, questions):
        self._questions = questions

    def setAnswers(self, answers):
        self._answers = answers

    def check(self):
        correct = 0
        incorrect = 0
        for original in self._questions.keys():
            if self._questions.get(original) == self._answers.get(original):
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        # return (correct, incorrect)
        return correct
