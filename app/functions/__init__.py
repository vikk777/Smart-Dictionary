from flask import flash
from datetime import date


# Add form errors messages to flash
def flashErrors(form):
    if form.errors:
        for field in form:
            for error in field.errors:
                flash('For field {0}: {1}'.format(field.name, error))


# Get dictionaries list from SmartDictionary for select tag
def choicesForSelect(dictionary):
    choices = list()

    # take list of touples (name, name)
    # for <select>
    for item in dictionary.dictionaries():
        if dictionary.quantity(item[0]):
            choices.append((item[0], item[0]))

    # Add "All" option, if dictionaries more then 1
    if len(choices) > 1:
        choices.append(('__all__', 'All'))

    return choices


def wordsUpdateTime(words):
    timeDict = dict()
    updateTime = date.fromtimestamp(0)
    for word in words:
        if updateTime != date.fromtimestamp(word['updateTime']):
            updateTime = date.fromtimestamp(word['updateTime'])
            timeDict.update({word['original']: updateTime.strftime('%d %b\'%y')})
    return timeDict
