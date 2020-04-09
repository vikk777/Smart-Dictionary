from flask import flash
import datetime


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
    updateTime = 0
    for word in words:
        if updateTime != word['updateTime']:
            updateTime = word['updateTime']
            strTime = datetime.date.fromtimestamp(updateTime)
            timeDict.update({word['original']: strTime.strftime('%d %b\'%y')})
    return timeDict
