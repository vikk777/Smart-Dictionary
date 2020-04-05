class TestManager(object):
    def __init__(self):
        self._questions = dict()
        self._answers = dict()
        self._wrongAnswers = dict()

    def setQuestions(self, questions):
        self._questions = questions

    def setAnswers(self, answers):
        self._answers = answers

    # def wrongAnswers(self):
    #     return self._wrongAnswers

    def check(self):
        correct = 0
        incorrect = 0

        for orig in self._questions:

            if self._answers.get(orig) in self._questions.get(orig).split(', '):
                correct = correct + 1

            else:
                incorrect = incorrect + 1
                self._wrongAnswers[orig] = self._questions.get(orig)

        # return (correct, incorrect)
        return correct
