from . import app
from flask import request, redirect, render_template, url_for, flash
from .model.smart_dictionary import SmartDictionary
from .forms.word import AddWordForm, AddWordSelectForm, ChangeWordForm, DeleteWordForm
from .forms.dictionary import AddDictionaryForm, DeleteDictionaryForm, ChangeDictionaryForm
from .forms.test import TestStartForm, TestNextForm, CorrectMistakesForm
from .sderrors import DictionaryNotExistError, DictionaryAlreadyExistError, WordNotExistError
import app.functions as functions
import time
import app.consts as consts

smartDict = SmartDictionary()


@app.route('/')
def index():
    return redirect(url_for('addWord'))


@app.route('/add-word/', methods=['POST', 'GET'])
def addWord(wrapped=False):
    """
    wrapped is used for save flashed messages
    """
    form = AddWordSelectForm()
    choices = list()

    # take list of touples (name, name)
    # for <select>
    for touple in smartDict.dictionaries():
        choices.append((touple[0], touple[0]))

    form.dictionary.choices = choices

    if form.validate_on_submit():
        dictionary = form.dictionary.data
        original = form.original.data
        translate = form.translate.data
        transcription = form.transcription.data
        replace = form.replace.data
        createTime = time.time()

        try:
            smartDict.addWord(dictionary, original,
                              translate, transcription, createTime, replace)
            flash('Word {0} was added to {1}.'.format(
                original, dictionary))

        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(dictionary))

        return wrapped if wrapped else redirect(url_for('addWord'))

    else:  # form not valid
        functions.flashErrors(form)

    return wrapped if wrapped else render_template('add-word.html', form=form)


@app.route('/dictionaries/', methods=['POST', 'GET'])
def dictionaries():
    view = request.args.get('view')  # dict name for view

    try:
        words = smartDict.words(view) if view else []
        viewDict = smartDict.dictionary(view) if view else ()
    except DictionaryNotExistError:
        flash('Dictionary {} doesn\'t exist!'.format(view))
        words = []
        viewDict = ()

    dicts = smartDict.dictionaries()
    updateTime = functions.wordsUpdateTime(words)
    forms = dict()

    if view:
        forms['changeDict'] = ChangeDictionaryForm()
        forms['deleteDict'] = DeleteDictionaryForm()
        forms['changeWord'] = ChangeWordForm()
        forms['deleteWord'] = DeleteWordForm()
        forms['addWord'] = AddWordForm()

    return render_template(
        'dictionaries.html',
        dicts=dicts,
        words=words,
        viewDict=viewDict,
        forms=forms,
        updateTime=updateTime)


@app.route('/dictionaries/add/', methods=['POST', 'GET'])
def addDictionary():
    form = AddDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        try:
            smartDict.addDictionary(name, description)
            flash('Dictionary {} created.'.format(name))
            return redirect(url_for('dictionaries', view=name))

        except DictionaryAlreadyExistError:
            flash('Dictionary {} already exist!'.format(name))
    else:  # form not valid
        functions.flashErrors(form)

    return render_template('add-dictionary.html', form=form)


@app.route('/dictionaries/delete/', methods=['POST'])
def deleteDictionary():
    form = DeleteDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data

        try:
            smartDict.deleteDictionary(name)
            flash('Dictionary {} was deleted.'.format(name))
            return redirect(url_for('dictionaries'))

        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(name))

    else:  # form not valid
        functions.flashErrors(form)

    return redirect(request.referrer)


@app.route('/dictionaries/change/', methods=['POST'])
def changeDictionary():
    form = ChangeDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        old = form.old.data

        try:
            smartDict.changeDictionary(old, name, description)
            flash('Dictionary {} was changed.'.format(name))
            return redirect(url_for('dictionaries', view=name))

        except DictionaryAlreadyExistError:
            flash('Dictionary {} already exist!'.format(name))
        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(old))

    else:  # form not valid
        functions.flashErrors(form)

    return redirect(request.referrer)


@app.route('/dictionaries/add-word/', methods=['POST'])
def addWordWrapper():
    addWord(wrapped=True)
    return redirect(request.referrer)


@app.route('/dictionaries/change-word/', methods=['POST'])
def changeWord():
    form = ChangeWordForm()

    if form.validate_on_submit():
        old = form.old.data
        original = form.original.data
        translate = form.translate.data
        transcription = form.transcription.data
        dictionary = form.dictionary.data
        updateTime = time.time()

        try:
            smartDict.changeWord(dictionary, old, original,
                                 translate, transcription, updateTime)
            flash('Word {} was changed.'.format(old))
            return redirect(url_for('dictionaries', view=dictionary))

        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(dictionary))
        except WordNotExistError:
            flash('Word {} doesn\'t exist!'.format(old))

    else:  # form not valid
        functions.flashErrors(form)

    return redirect(request.referrer)


@app.route('/dictionaries/delete-word/', methods=['POST'])
def deleteWord():
    form = DeleteWordForm()

    if form.validate_on_submit():
        dictionary = form.dictionary.data
        original = form.original.data

        try:
            smartDict.deleteWord(dictionary, original)
            flash('Word {} was deleted.'.format(original))
            return redirect(url_for('dictionaries', view=dictionary))

        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(dictionary))
        except WordNotExistError:
            flash('Word {} doesn\'t exist!'.format(original))

    else:  # form not valid
        functions.flashErrors(form)

    return redirect(request.referrer)


@app.route('/test/start', methods=['POST', 'GET'])
def startTest():
    forms = dict()
    forms['startTest'] = TestStartForm()
    forms['startTest'].dictionary.choices = functions.choicesForSelect(smartDict)
    forms['startTest'].period.choices = [
        ('-1', 'All period'),
        ('0', 'Last day'),
        ('6', 'Last week'),
        ('30', 'Last month')]

    if smartDict.haveMistakes():
        forms['correctMistakes'] = CorrectMistakesForm()

    if 'startTest' in request.form:
        if forms['startTest'].validate_on_submit():
            try:
                dictionary = forms['startTest'].dictionary.data
                period = forms['startTest'].period.data
                smartDict.testInit(dictionary, period)
                return redirect(url_for('test'))
            except DictionaryNotExistError:
                flash('Dictionary {} doesn\'t exist!'.format(dictionary))
        else:  # form not valid
            functions.flashErrors(forms['startTest'])

    if 'correctMistakes' in request.form:
        smartDict.testInit(consts.MISTAKE_DICT)
        return redirect(url_for('test'))

    return render_template('start-test.html', forms=forms)


@app.route('/test', methods=['POST', 'GET'])
def test():
    form = TestNextForm()
    # if there are errors, last question will remains
    question = form.question.data

    if smartDict.testIsInit():
        if form.validate_on_submit():
            answer = form.answer.data
            smartDict.addAnswer((question, answer))
        else:
            functions.flashErrors(form)

        if not form.errors:
            question = smartDict.nextQuestion()

            if not question:
                result = smartDict.testResult()
                return render_template('finish-test.html', result=result)
    else:
        flash(
            'Please, <a href="{0}">choice the dictionary</a> to pass the test.'.format(url_for('startTest')))

    return render_template('test.html', form=form, question=question)


@app.route('/test/finish', methods=['POST', 'GET'])
def finishTest():
    pass
    return render_template('finish-test.html')
