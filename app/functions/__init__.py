from flask import flash


# Add form errors messages to flash
def flashErrors(form):
    flashed = form
    if flashed.errors:
        for field in flashed:
            for error in field.errors:
                flash('For field {0}: {1}'.format(field.name, error))


# Get dictionaries list from SmartDictionary for select tag
def choicesForSelect(smartDictionary):
    choices = list()
    dictionary = smartDictionary

    # take list of touples (name, name)
    # for <select>
    for item in dictionary.dictionaries():
        if dictionary.quantity(item[0]):
            choices.append((item[0], item[0]))
    return choices
