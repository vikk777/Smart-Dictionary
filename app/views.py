from . import app
from flask import request, redirect, render_template, url_for
from .model.smart_dictionary import SmartDictionary
from .forms.word import AddWordForm, ChangeWordForm, DeleteWordForm
from .forms.dictionary import AddDictionaryForm, DeleteDictionaryForm, ChangeDictionaryForm

smartDict = SmartDictionary()


@app.route('/')
def index():
    return redirect('/add-word')


@app.route('/add-word', methods=['POST', 'GET'])
def addWord():
    form = AddWordForm()
    form.makeDictSelectField()
    form.dictionary.choices = smartDict.dictionaries()

    if form.validate_on_submit():
        dictionary = form.dictionary.data
        original = form.original.data
        translate = form.translate.data
        transcription = form.transcription.data
        smartDict.addWord(dictionary, original, translate, transcription)

    return render_template('add-word.html', form=form)


@app.route('/dictionaries', methods=['POST', 'GET'])
def dictionaries():
    view = request.args.get('view')  # dict name for view

    if request.method == 'POST':
        if 'addDict' in request.form:
            name = request.form.get('name')
            description = request.form.get('description')
            smartDict.addDictionary(name, description)
            return redirect(url_for('dictionaries', view=name))

        if 'deleteDict' in request.form:
            name = request.form.get('name')
            smartDict.deleteDictionary(name)
            # view = ''
            return redirect(url_for('dictionaries'))

        if 'changeDict' in request.form:
            name = request.form.get('name')
            description = request.form.get('description')
            old = request.form.get('old')
            smartDict.changeDictionary(old, name, description)
            return redirect(url_for('dictionaries', view=name))

        if 'addWord' in request.form:
            dictionary = request.form.get('dictionary')
            original = request.form.get('original')
            translate = request.form.get('translate')
            transcription = request.form.get('transcription')
            smartDict.addWord(dictionary, original,
                              translate, transcription)

        if 'changeWord' in request.form:
            dictionary = request.form.get('dictionary')
            old = request.form.get('old')
            original = request.form.get('original')
            translate = request.form.get('translate')
            transcription = request.form.get('transcription')
            smartDict.changeWord(dictionary, old, original,
                                 translate, transcription)

        if 'deleteWord' in request.form:
            dictionary = request.form.get('dictionary')
            original = request.form.get('original')
            smartDict.deleteWord(dictionary, original)
    # else:

    viewDict = smartDict.dictionary(view) if view else ()
    forms = dict()

    if view:
        forms['addWord'] = AddWordForm()
        forms['changeWord'] = ChangeWordForm()
        forms['deleteWord'] = DeleteWordForm()
        forms['changeDict'] = ChangeDictionaryForm()
        forms['deleteDict'] = DeleteDictionaryForm()

    words = smartDict.words(view) if view else []
    dicts = smartDict.dictionaries()

    return render_template(
        'dictionaries.html',
        dicts=dicts,
        words=words,
        viewDict=viewDict,
        forms=forms)


@app.route('/dictionaries/add')
def addDictionary():
    form = AddDictionaryForm()
    return render_template('add-dictionary.html', form=form)
