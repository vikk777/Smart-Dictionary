MISTAKE_DICT = '__mistakes__'
ALL_DICTS = '__all__'

WORD_ADDED = 'Word {0} was added to {1}.'
WORD_CHANGED = 'Word {0} was changed.'
WORD_DEL = 'Word {0} was deleted.'
WORD_NOT_EXIST = 'Word {0} doesn\'t exist!'
DICT_ADDED = 'Dictionary {0} created.'
DICT_DEL = 'Dictionary {0} was deleted.'
DICT_CHANGED = 'Dictionary {0} was changed.'
DICT_NOT_EXIST = 'Dictionary {0} doesn\'t exist!'
DICT_EXIST = 'Dictionary {0} already exist!'


class period:
    ALL_I = '-1'
    ALL_S = 'All period'
    LAST_DAY_I = '0'
    LAST_DAY_S = 'Last day'
    LAST_WEEK_I = '6'
    LAST_WEEK_S = 'Last week'
    LAST_MONTH_I = '30'
    LAST_MONTH_S = 'Last month'


class regexp:
    RU = '^[А-Яа-яЁё\s,]+$'
    RU_MSG = 'Russian letters and spaces only.'
    EN = '^[a-zA-Z\s]+$'
    EN_MSG = 'Latin letters and spaces only.'
    RU_EN_BASE = '^[a-zA-Zа-яА-ЯёЁ\s]'
    RU_EN_FULL = RU_EN_BASE + '+$'
    RU_EN_EMPTY = RU_EN_BASE + '*$'
    RU_EN_MSG = 'Latin and russian letters and spaces only.'
    IMPORT = '([a-zA-Z ]+)\s*-\s*((,? *[а-яА-ЯёЁ]+)+)'
