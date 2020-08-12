from app import db
from .test_manager_model import TestModel
from .user import User
from random import randint


class TestManager():
    def __init__(self):
        # self._tempQuestions = dict()
        self._user = User()

    # def init(self, userId):
    #     if self._tempQuestions.get(userId) is None:
    #         self._tempQuestions[userId] = list()
    #         return True
    #     else:
    #         return False

    def isInit(self, userId):
        return True if TestModel.query.filter_by(user_id=userId).count()\
            else False

    def setQuestions(self, userId, questions):
        for question, answer in questions.items():
            if not self.haveQuestion(userId, question):
                self.addQuestion(userId, question, answer)
        return True

    def addQuestion(self, userId, question, answer):
        row = TestModel(user_id=userId,
                        question=question,
                        answer=answer)
        db.session.add(row)
        db.session.commit()
        return True

    def haveQuestion(self, userId, question):
        return True if TestModel.query.filter_by(
            user_id=userId,
            question=question).count() else False

    def rawQuestions(self, userId):
        return TestModel.query.filter_by(user_id=userId).all()

    def questions(self, userId):
        dict_ = dict()
        for question in self.rawQuestions(userId):
            dict_.update({question.question: question.answer})
        return dict_

    def setAnswer(self, userId, question, answer):
        # answer - touple
        question = question
        userAnswer = answer
        row = TestModel.query.filter_by(user_id=userId,
                                        question=question).first()
        row.user_answer = userAnswer
        row.passed = True
        db.session.commit()
        return True

    def nextQuestion(self, userId):
        questions = TestModel.query.filter_by(user_id=userId,
                                              passed=False).all()
        if questions:
            position = randint(0, len(questions) - 1)
            return questions.pop(position).question
        else:
            return None

    # def setTempQuestions(self, userId, questions):
    #     self._tempQuestions[userId] = questions
    #     return True

    # def tempQuestions(self, userId):
    #     return self._tempQuestions.get(userId)

    def mistakes(self, userId):
        words = dict()

        for word in self._user.mistakes(userId):
            words.update({word.original: word.translate})
        return words

    def check(self, userId):
        correct = 0
        total = self.total(userId)
        tempMistakes = list()

        for row in self.rawQuestions(userId):
            if row.user_answer in\
                    row.answer.split(', '):
                correct += 1
                if self._user.haveMistake(userId, row.question):
                    self._user.removeMistake(userId, row.question)
            else:
                tempMistakes.append({
                    'question': row.question,
                    'right': row.answer,
                    'wrong': row.user_answer or '[empty]'})

        # add mistakes to db
        # do not in loop above because
        # the mistake could be removed by
        # right answer on second question
        for mistake in tempMistakes:
            if not self._user.haveMistake(userId, mistake['question']):
                self._user.addMistake(userId, mistake['question'])

        self.abortTest(userId)

        return {'correct': correct,
                'total': total,
                'mistakes': tempMistakes}

    def total(self, userId):
        return TestModel.query.filter_by(user_id=userId).count()

    def notPassed(self, userId):
        return TestModel.query.filter_by(user_id=userId, passed=False).count()

    def progress(self, userId):
        """Current step and total steps"""
        return {'current': self.total(userId) - self.notPassed(userId),
                'total': self.total(userId)}

    def abortTest(self, userId):
        TestModel.query.filter_by(user_id=userId).delete()
        db.session.commit()
        return True
