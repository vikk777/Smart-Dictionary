from flask import flash


def flashErrors(form):
    flashed = form
    if flashed.errors:
        for field in flashed:
            for error in field.errors:
                flash('For field {0}: {1}'.format(field.name, error))
