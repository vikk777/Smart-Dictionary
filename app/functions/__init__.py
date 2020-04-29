from flask import flash
from datetime import date
import re
import app.consts as consts


# Add form errors messages to flash
def flashErrors(form):
    if form.errors:
        for field in form:
            for error in field.errors:
                flash('For field {0}: {1}'.format(field.name, error),
                      consts.ERROR)


# Get dictionaries list from SmartDictionary for select tag
def choicesForSelect(dictionary, addAll=False):
    choices = list()

    # take list of touples (name, name)
    # for <select>
    for item in dictionary.dictionaries():
        if addAll:
            if dictionary.quantity(item[0]):
                choices.append((item[0], item[0]))
        else:
            choices.append((item[0], item[0]))

    # Add "All" option, if dictionaries more then 1
    if len(choices) > 1 and addAll:
        choices.append((consts.ALL_DICTS, 'All'))

    return choices


# Get dict {'word': date}
def wordsUpdateTime(words):
    timeDict = dict()
    updateTime = date.fromtimestamp(0)
    for word in words:
        if updateTime != date.fromtimestamp(word['updateTime']):
            updateTime = date.fromtimestamp(word['updateTime'])
            timeDict.update({word['original']:
                             updateTime.strftime('%d %b\'%y')})
    return timeDict


# Remove 2+ spaces, and align commas
def trim(string):
    pattern = r',+ +,+|\s\s+|,,+|^[, ]+|[, ]+$'

    while re.search(pattern, string):
        string = re.sub(r'\s\s+', ' ', string)
        string = re.sub(r',,+|,* +,+', ',', string)
        string = re.sub(r'^[, ]+|[, ]+$', '', string)

    string = re.sub(r'(\w) (,)', r'\1\2', string)
    return re.sub(r'(,)(\w)', r'\1 \2', string)


def search(pattern, string):
    return re.search(pattern, trim(string))


def generateLink(link, text):
    return '<a href="{0}">{1}</a>'.format(link, text)
