from django import template

register = template.Library()

SEX_CHOICES = {
    'M': 'Мужской',
    'F': 'Женский',
}

SPORT_CHOICES = {
    'football': 'Футбол',
    'basketball': 'Баскетбол',
    'swimming': 'Плавание',
    'athletics': 'Лёгкая атлетика',
    'martial_arts': 'Единоборства',
    'other': 'Другой вид спорта',
}

RANK_CHOICES = {
    'none': 'Без разряда',
    '3y': '3-й юношеский',
    '2y': '2-й юношеский',
    '1y': '1-й юношеский',
    '3': '3-й взрослый',
    '2': '2-й взрослый',
    '1': '1-й взрослый',
    'KMS': 'КМС',
    'MS': 'МС',
    'MSMK': 'МСМК',
}


@register.filter
def human_sex(value):
    return SEX_CHOICES.get(value, value)


@register.filter
def human_sport(value):
    return SPORT_CHOICES.get(value, value)


@register.filter
def human_rank(value):
    return RANK_CHOICES.get(value, value)