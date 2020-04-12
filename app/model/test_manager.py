class TestManager(object):
    def __init__(self):
        self._questions = dict()
        self._answers = dict()
        self._tempQuestions = list()
        self._mistakes = dict()

    def setQuestions(self, questions):
        self._questions = questions

    def setAnswer(self, answer):
        self._answers.update({answer[0]: answer[1]})

    def setTempQuestions(self, questions):
        self._tempQuestions = questions

    def tempQuestions(self):
        return self._tempQuestions

    def mistakes(self):
        return self._mistakes

    def check(self):
        correct = 0
        total = len(self._questions)
        tempMistakes = list()

        for question in self._questions:
            if self._answers.get(question) in self._questions.get(question).split(', '):
                correct += 1
                if question in self._mistakes:
                    del self._mistakes[question]
            else:
                tempMistakes.append({'question': question,
                                     'right': self._questions.get(question),
                                     'wrong': self._answers.get(question)})

                if question not in self._mistakes:
                    self._mistakes.update({question: self._questions.get(question)})

        self._questions.clear()
        self._answers.clear()
        # self._tempQuestions.clear()  # will be empty

        return {'correct': correct,
                'total': total,
                'mistakes': tempMistakes}

    def progress(self):
        """Current step and total steps"""
        return {'current': len(self._questions) - len(self._tempQuestions),
                'total': len(self._questions)}
