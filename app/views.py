from . import app, loginManager
from flask import request, redirect, render_template, url_for, flash, send_from_directory
from .model.smart_dictionary import SmartDictionary
from .forms.word import \
    AddWordForm,\
    AddWordSelectForm,\
    ChangeWordForm,\
    DeleteWordForm
from .forms.dictionary import \
    AddDictionaryForm,\
    DeleteDictionaryForm,\
    ChangeDictionaryForm
from .forms.test import TestStartForm, TestNextForm,\
    CorrectMistakesForm, AddQuestionForm
from .forms.import_words import ImportForm
from .forms.login import LoginForm, RegisterForm
from .sderrors import \
    DictionaryNotExistError,\
    DictionaryAlreadyExistError,\
    WordNotExistError,\
    UserAlreadyExistError,\
    InvalidUsernameOrPasswordError,\
    QuestionAlreadyAddedError
import app.functions as functions
from time import time
import app.consts as consts
from flask_login import login_required, current_user
from werkzeug.urls import url_parse
import os

smartDict = SmartDictionary()
loginManager.login_view = 'login'
loginManager.login_message_category = consts.ERROR


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico',
                               mimetype='image/x-icon')


@app.route('/')
def index():
    return render_template('base-page.html')
    # return redirect(url_for('addWord'))


@app.route('/dictionaries/', methods=['POST', 'GET'])
@login_required
def dictionaries():
    # view = request.args.get('view')  # dict name for view

    # try:
    #     words = smartDict.words(view) if view else list()
    #     viewDict = smartDict.dictionary(view) if view else tuple()
    # except DictionaryNotExistError:
    #     flash(consts.DICT_NOT_EXIST.format(view), consts.ERROR, consts.ERROR)
    #     words = list()
    #     viewDict = tuple()

    dicts = smartDict.dictionaries()
    total = smartDict.totalWords()
    # updateTime = functions.wordsUpdateTime(words)
    # forms = dict()

    # if view:
    #     forms['changeDict'] = ChangeDictionaryForm()
    #     forms['deleteDict'] = DeleteDictionaryForm()
    #     forms['changeWord'] = ChangeWordForm()
    #     forms['deleteWord'] = DeleteWordForm()
    #     forms['addWord'] = AddWordForm()
    #     forms['addQuestion'] = AddQuestionForm()

    return render_template(
        'dictionaries.html',
        dicts=dicts,
        total=total,
        # words=words,
        # viewDict=viewDict,
        # forms=forms,
        # updateTime=updateTime,
        active=consts.active.DICT)


# @app.route('/dictionaries/view/<name>', methods=['POST', 'GET'])
@app.route('/dictionaries/view/<name>', methods=['GET'])
@login_required
def viewDictionary(name):
    try:
        words = smartDict.words(name) if name else list()
        viewDict = smartDict.dictionary(name) if name else tuple()
        updateTime = functions.wordsUpdateTime(words)
        form = AddQuestionForm()
    except DictionaryNotExistError:
        flash(consts.DICT_NOT_EXIST.format(name), consts.ERROR)
        words = None
        viewDict = None
        updateTime = None
        form = None

    return render_template(
        'view-dictionary.html',
        words=words,
        viewDict=viewDict,
        form=form,
        updateTime=updateTime,
        active=consts.active.DICT)


@app.route('/dictionaries/edit/<name>', methods=['POST', 'GET'])
@login_required
def editDictionary(name):
    try:
        words = smartDict.words(name) if name else list()
        viewDict = smartDict.dictionary(name) if name else tuple()
        updateTime = functions.wordsUpdateTime(words)
    except DictionaryNotExistError:
        flash(consts.DICT_NOT_EXIST.format(name), consts.ERROR)
        words = None
        viewDict = None
        updateTime = None

    forms = dict()
    if name:
        forms['changeDict'] = ChangeDictionaryForm()
        forms['deleteDict'] = DeleteDictionaryForm()
        forms['changeWord'] = ChangeWordForm()
        forms['deleteWord'] = DeleteWordForm()
        forms['addWord'] = AddWordForm()
        forms['addQuestion'] = AddQuestionForm()

    return render_template(
        'edit-dictionary.html',
        words=words,
        viewDict=viewDict,
        forms=forms,
        updateTime=updateTime,
        active=consts.active.DICT)


@app.route('/dictionaries/add/', methods=['POST', 'GET'])
@login_required
def addDictionary():
    form = AddDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        try:
            smartDict.addDictionary(name, description)
            flash(consts.DICT_ADDED.format(name), consts.SUCCESS)
            return redirect(url_for('viewDictionary', name=name))

        except DictionaryAlreadyExistError:
            flash(consts.DICT_EXIST.format(name), consts.ERROR, consts.ERROR)
    else:  # form not valid
        functions.flashErrors(form)

    return render_template('add-dictionary.html', form=form,
                           active=consts.active.DICT)


@app.route('/dictionaries/delete/', methods=['POST'])
@login_required
def deleteDictionary():
    form = DeleteDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data

        try:
            smartDict.deleteDictionary(name)
            flash(consts.DICT_DEL.format(name), consts.SUCCESS)
            return redirect(url_for('dictionaries'))

        except DictionaryNotExistError:
            flash(consts.DICT_NOT_EXIST.format(name), consts.ERROR)

    else:  # form not valid
        functions.flashErrors(form)

    return redirect(request.referrer)


@app.route('/dictionaries/change/', methods=['POST'])
@login_required
def changeDictionary():
    form = ChangeDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        old = form.old.data

        try:
            smartDict.changeDictionary(old, name, description)
            flash(consts.DICT_CHANGED.format(name), consts.SUCCESS)
            return redirect(url_for('editDictionary', name=name))

        except DictionaryAlreadyExistError:
            flash(consts.DICT_EXIST.format(name), consts.ERROR)
        except DictionaryNotExistError:
            flash(consts.DICT_NOT_EXIST.format(old), consts.ERROR)

    else:  # form not valid
        functions.flashErrors(form)

    return redirect(request.referrer)


@app.route('/add-word/', methods=['POST', 'GET'])
@login_required
def addWord(wrapped=False):
    """
    wrapped arg is used for save flashed messages
    """
    form = AddWordSelectForm()
    form.dictionary.choices = functions.choicesForSelect(smartDict)
    total = smartDict.totalWords()

    if form.validate_on_submit():
        dictionary = form.dictionary.data
        original = form.original.data
        translate = form.translate.data
        transcription = form.transcription.data
        replace = form.replace.data
        createTime = time()

        try:
            smartDict.addWord(dictionary, original,
                              translate, transcription,
                              createTime, replace)
            flash(consts.WORD_ADDED.format(
                original, functions.generateLink(
                    url_for('viewDictionary', name=dictionary), dictionary)),
                  consts.SUCCESS)

        except DictionaryNotExistError:
            flash(consts.DICT_NOT_EXIST.format(dictionary), consts.ERROR)

        return wrapped if wrapped else redirect(url_for('addWord'))

    else:  # form not valid
        functions.flashErrors(form)

    return wrapped if wrapped\
        else render_template('add-word.html', form=form,
                             total=total, active=consts.active.WORD)


@app.route('/dictionaries/add-word/', methods=['POST'])
@login_required
def addWordWrapper():
    addWord(wrapped=True)
    return redirect(request.referrer)


@app.route('/dictionaries/change-word/', methods=['POST'])
@login_required
def changeWord():
    form = ChangeWordForm()
    next_page = request.args.get('next')

    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('dictionaries')

    if form.validate_on_submit():
        old = form.old.data
        original = form.original.data
        translate = form.translate.data
        transcription = form.transcription.data
        dictionary = form.dictionary.data
        updateTime = time()

        try:
            smartDict.changeWord(dictionary, old, original,
                                 translate, transcription, updateTime)
            flash(consts.WORD_CHANGED.format(old), consts.SUCCESS)
            # return redirect(url_for('editDictionary', name=dictionary))
            return redirect(next_page)

        except DictionaryNotExistError:
            flash(consts.DICT_NOT_EXIST.format(dictionary), consts.ERROR)
        except WordNotExistError:
            flash(consts.WORD_NOT_EXIST.format(old), consts.ERROR)

    else:  # form not valid
        functions.flashErrors(form)

    return redirect(next_page)


@app.route('/dictionaries/delete-word/', methods=['POST'])
@login_required
def deleteWord():
    form = DeleteWordForm()
    next_page = request.args.get('next')

    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('dictionaries')

    if form.validate_on_submit():
        dictionary = form.dictionary.data
        original = form.original.data

        try:
            smartDict.deleteWord(dictionary, original)
            flash(consts.WORD_DEL.format(original), consts.SUCCESS)
            return redirect(url_for('editDictionary', name=dictionary))

        except DictionaryNotExistError:
            flash(consts.DICT_NOT_EXIST.format(dictionary), consts.ERROR)
        except WordNotExistError:
            flash(consts.WORD_NOT_EXIST.format(original), consts.ERROR)

    else:  # form not valid
        functions.flashErrors(form)

    return redirect(next_page)


@app.route('/test/start/', methods=['POST', 'GET'])
@login_required
def startTest():
    do = request.args.get('do')
    forms = dict()
    forms['startTest'] = TestStartForm()
    forms['startTest'].dictionary.choices = list()

    if smartDict.isTestInit():
        forms['startTest'].dictionary.choices.append(
            (consts.ADDED_WORDS, consts.ADDED_WORDS_S))

    forms['startTest'].dictionary.choices += functions.choicesForSelect(
        smartDict, addAll=True)

    forms['startTest'].period.choices = [
        (consts.period.ALL_I, consts.period.ALL_S),
        (consts.period.LAST_DAY_I, consts.period.LAST_DAY_S),
        (consts.period.LAST_WEEK_I, consts.period.LAST_WEEK_S),
        (consts.period.LAST_MONTH_I, consts.period.LAST_MONTH_S)]

    mistakes = smartDict.mistakes()
    if mistakes:
        forms['correctMistakes'] = CorrectMistakesForm()

    if do == 'start':
        if forms['startTest'].validate_on_submit():
            try:
                dictionary = forms['startTest'].dictionary.data
                period = forms['startTest'].period.data
                smartDict.testInit(dictionary, period)
                return redirect(url_for('test'))

            except DictionaryNotExistError:
                flash(consts.DICT_NOT_EXIST.format(dictionary), consts.ERROR)
        else:  # form not valid
            functions.flashErrors(forms['startTest'])

    if do == 'mistakes':
        smartDict.testInit(consts.MISTAKE_DICT)
        return redirect(url_for('test'))

    return render_template('start-test.html',
                           forms=forms,
                           mistakes=mistakes,
                           active=consts.active.TEST)


@app.route('/test/add-question', methods=['POST', 'GET'])
@login_required
def addQuestion():
    form = AddQuestionForm()
    next_page = request.args.get('next')

    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('dictionaries')

    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data
        try:
            smartDict.addQuestion(question, answer)
            flash('Word {0} - {1} was added to Test.'.format(question, answer),
                  consts.SUCCESS)
        except QuestionAlreadyAddedError:
            flash('Word {0} - {1} have already added to Test.'
                  .format(question, answer), consts.ERROR)

    else:  # form not valid
        functions.flashErrors(form)

    # return redirect(request.referrer)
    return redirect(next_page)


@app.route('/test/', methods=['POST', 'GET'])
@login_required
def test():
    forms = dict()
    forms['testNext'] = TestNextForm()
    # if there are errors, last question will remains
    question = dict()
    question['question'] = forms['testNext'].question.data

    if smartDict.isTestInit():
        if forms['testNext'].validate_on_submit():
            answer = forms['testNext'].answer.data or ''
            smartDict.addAnswer((question['question'], answer))
        else:
            functions.flashErrors(forms['testNext'])

        if not forms['testNext'].errors:
            question = smartDict.nextQuestion()

            if not question:
                result = smartDict.testResult()

                forms['correctMistakes'] = CorrectMistakesForm(
                ) if smartDict.mistakes() else None

                return render_template(
                    'finish-test.html',
                    result=result,
                    form=forms['correctMistakes'],
                    active=consts.active.TEST)
    else:
        flash(
            'Please, <a href="{0}">choice the dictionary</a> \
            to pass the test.'.format(url_for('startTest')), consts.ERROR)

    return render_template(
        'test.html',
        form=forms['testNext'],
        question=question,
        active=consts.active.TEST)


@app.route('/import/', methods=['POST', 'GET'])
@login_required
def importWords():
    form = ImportForm()
    form.dictionary.choices = functions.choicesForSelect(smartDict)
    addedWords = list()

    if form.validate_on_submit():
        dictionary = form.dictionary.data
        words = form.words.data
        updateTime = time()

        try:
            addedWords = smartDict.importWords(dictionary, words, updateTime)
            if addedWords:
                flash('Next words were added:', consts.SUCCESS)
                for word in addedWords:
                    flash('{0} - {1}'.format(word[0], word[1]), consts.SUCCESS)
            else:
                flash('Words were not added.', consts.ERROR)
            return redirect(url_for('importWords'))
        except DictionaryNotExistError:
            flash(consts.DICT_NOT_EXIST.format(dictionary), consts.ERROR)

    else:  # form not valid
        functions.flashErrors(form)

    return render_template('import.html',
                           form=form,
                           addedWords=addedWords,
                           active=consts.active.IMPORT)


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        try:
            smartDict.registerUser(name, password)
            # flash('Registration successful.')
            # return redirect(url_for('login'))
            return redirect(url_for('index'))

        except UserAlreadyExistError:
            flash('User already exists.', consts.ERROR)

    else:  # form not valid
        functions.flashErrors(form)

    return render_template('register.html', form=form,
                           active=consts.active.REGISTER)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        # return redirect(url_for('addWord'))

    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        remember = form.remember.data

        try:
            smartDict.loginUser(name, password, remember)
            # flash('Authorization successful.')

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
                # return redirect(url_for('addWord'))
            return redirect(next_page)

        except InvalidUsernameOrPasswordError:
            flash('Invalid name or password.', consts.ERROR)

    else:  # form not valid
        functions.flashErrors(form)

    return render_template('login.html', form=form,
                           active=consts.active.LOGIN)


@app.route('/logout/')
@login_required
def logout():
    smartDict.logoutUser()
    # flash('You have been logged out.')
    return redirect(url_for('login'))
