from . import app
from flask import request, redirect, render_template
from .model.smart_dictionary import SmartDictionary
# from .controller import SmartDictionary

smartDict = SmartDictionary()


@app.route('/')
def index():
    return redirect('/add-word')


@app.route('/add-word', methods=['POST', 'GET'])
def addWord():
    if request.method == 'POST':
        dictionary = request.form.get('dictionary')
        original = request.form.get('original')
        translate = request.form.get('translate')
        transcription = request.form.get('transcription')
        smartDict.addWord(dictionary, original, translate, transcription)

        # if transcription:
        # else:
        #     smartDict.addWord(dictionary, original, translate)

    return render_template('add-word.html', dicts=smartDict.dictionaries())


@app.route('/dictionaries', methods=['POST', 'GET'])
def dictionaries():
    if request.method == 'POST':
        if 'addDict' in request.form:
            name = request.form.get('name')
            description = request.form.get('description')
            smartDict.addDictionary(name, description)
            view = name

        if 'deleteDict' in request.form:
            name = request.form.get('name')
            smartDict.deleteDictionary(name)
            view = ''

        if 'changeDict' in request.form:
            name = request.form.get('name')
            description = request.form.get('description')
            old = request.form.get('old')
            smartDict.changeDictionary(old, name, description)
            view = name

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
    else:
        view = request.args.get('view')  # dict name for view

    viewDict = smartDict.dictionary(view) if view else ()
    words = smartDict.words(view) if view else []
    dicts = smartDict.dictionaries()

    return render_template(
        'dictionaries.html',
        dicts=dicts,
        words=words,
        viewDict=viewDict)


@app.route('/dictionaries/add')
def addDictionary():
    return render_template('add-dictionary.html')
