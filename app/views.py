from . import app
from flask import request, redirect, render_template, url_for
from .model.smart_dictionary import SmartDictionary
from .forms.word import AddWordForm, AddWordSelectForm, ChangeWordForm, DeleteWordForm
from .forms.dictionary import AddDictionaryForm, DeleteDictionaryForm, ChangeDictionaryForm

smartDict = SmartDictionary()


@app.route('/')
def index():
    return redirect(url_for('addWord'))


@app.route('/add-word/', methods=['POST', 'GET'])
def addWord():
    form = AddWordSelectForm()
    form.dictionary.choices = smartDict.dictionaries()

    if form.validate_on_submit():
        dictionary = form.dictionary.data
        original = form.original.data
        translate = form.translate.data
        transcription = form.transcription.data
        smartDict.addWord(dictionary, original, translate, transcription)

    return render_template('add-word.html', form=form)


@app.route('/dictionaries/', methods=['POST', 'GET'])
def dictionaries():
    view = request.args.get('view')  # dict name for view
    words = smartDict.words(view) if view else []
    dicts = smartDict.dictionaries()
    viewDict = smartDict.dictionary(view) if view else ()
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
        smartDict.addDictionary(name, description)
        return redirect(url_for('dictionaries', view=name))

    return render_template('add-dictionary.html', form=form)


@app.route('/dictionaries/delete/', methods=['POST'])
def deleteDictionary():
    form = DeleteDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data
        smartDict.deleteDictionary(name)
        return redirect(url_for('dictionaries'))


@app.route('/dictionaries/change/', methods=['POST'])
def changeDictionary():
    form = ChangeDictionaryForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        old = form.old.data
        smartDict.changeDictionary(old, name, description)
        return redirect(url_for('dictionaries', view=name))


@app.route('/dictionaries/add-word/', methods=['POST'])
def addWordWrapper():
    addWord()
    form = AddWordForm()
    dictionary = form.dictionary.data
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
        smartDict.changeWord(dictionary, old, original,
                             translate, transcription)

    return redirect(url_for('dictionaries', view=dictionary))


@app.route('/dictionaries/delete-word/', methods=['POST'])
def deleteWord():
    form = DeleteWordForm()

    dictionary = form.dictionary.data
    original = form.original.data
    smartDict.deleteWord(dictionary, original)

    return redirect(url_for('dictionaries', view=dictionary))
