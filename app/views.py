from . import app
from flask import request, redirect, render_template, url_for, flash
from .model.smart_dictionary import SmartDictionary
from .forms.word import AddWordForm, AddWordSelectForm, ChangeWordForm, DeleteWordForm
from .forms.dictionary import AddDictionaryForm, DeleteDictionaryForm, ChangeDictionaryForm
from .sderrors import DictionaryNotExistError, DictionaryAlreadyExistError, WordNotExistError
from .functions import flashErrors

smartDict = SmartDictionary()


@app.route('/')
def index():
    return redirect(url_for('addWord'))


@app.route('/add-word/', methods=['POST', 'GET'])
def addWord(externForm=None):
    if externForm:
        form = externForm
    else:
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

        try:
            smartDict.addWord(dictionary, original,
                              translate, transcription, replace)
        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!').format(dictionary)

        flash('Word {0} was added to {1}.'.format(
            original, dictionary))

        if externForm:
            return form
        else:
            return redirect(url_for('addWord'))

    if externForm:
        return form
    else:
        return render_template('add-word.html', form=form)


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
        forms=forms)


@app.route('/dictionaries/add/', methods=['POST', 'GET'])
def addDictionary():
    form = AddDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        try:
            smartDict.addDictionary(name, description)
        except DictionaryAlreadyExistError:
            flash('Dictionary {} already exist!'.format(name))

        flash('Dictionary {} created.'.format(name))

        return redirect(url_for('dictionaries', view=name))

    return render_template('add-dictionary.html', form=form)


@app.route('/dictionaries/delete/', methods=['POST'])
def deleteDictionary():
    form = DeleteDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data

        try:
            smartDict.deleteDictionary(name)
        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(name))

        flash('Dictionary {} was deleted.'.format(name))

    return redirect(url_for('dictionaries'))


@app.route('/dictionaries/change/', methods=['POST'])
def changeDictionary():
    form = ChangeDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        old = form.old.data

        try:
            smartDict.changeDictionary(old, name, description)
        except DictionaryAlreadyExistError:
            flash('Dictionary {} already exist!'.format(name))
        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(old))

        flash('Dictionary {} was changed.'.format(name))
        return redirect(url_for('dictionaries', view=name))

    flashErrors(form)
    return redirect(request.referrer)


@app.route('/dictionaries/add-word/', methods=['POST'])
def addWordWrapper():
    form = addWord(AddWordForm())
    dictionary = form.dictionary.data
    if form.errors:
        flashErrors(form)

    return redirect(url_for('dictionaries', view=dictionary))


@app.route('/dictionaries/change-word/', methods=['POST'])
def changeWord():
    form = ChangeWordForm()

    if form.validate_on_submit():
        old = form.old.data
        original = form.original.data
        translate = form.translate.data
        transcription = form.transcription.data
        dictionary = form.dictionary.data

        try:
            smartDict.changeWord(dictionary, old, original,
                                 translate, transcription)
        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(dictionary))
        except WordNotExistError:
            flash('Word {} doesn\'t exist!'.format(old))

    if form.errors:
        flashErrors(form)

    return redirect(url_for('dictionaries', view=dictionary))


@app.route('/dictionaries/delete-word/', methods=['POST'])
def deleteWord():
    form = DeleteWordForm()

    if form.validate_on_submit():
        dictionary = form.dictionary.data
        original = form.original.data

        try:
            smartDict.deleteWord(dictionary, original)
        except DictionaryNotExistError:
            flash('Dictionary {} doesn\'t exist!'.format(dictionary))
        except WordNotExistError:
            flash('Word {} doesn\'t exist!'.format(original))

    if form.errors:
        flashErrors(form)

    return redirect(url_for('dictionaries', view=dictionary))
