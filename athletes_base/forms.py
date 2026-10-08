import json
from datetime import date
from django import forms
from django.core.exceptions import ValidationError

SEX_CHOICES = [
    ("M", "Мужчина"),
    ("F", "Женщина")
]

RANK_CHOICES = [
    ('none', 'Без разряда'),
    ('3y', '3-й юношеский'), ('2y', '2-й юношеский'), ('1y', '1-й юношеский'),
    ('3', '3-й взрослый'), ('2', '2-й взрослый'), ('1', '1-й взрослый'),
    ('KMS', 'КМС'), ('MS', 'МС'), ('MSMK', 'МСМК'),
]

SPORT_CHOICES = [
    ('football', 'Футбол'),
    ('basketball', 'Баскетбол'),
    ('swimming', 'Плавание'),
    ('athletics', 'Легкая атлетика'),
    ('martial_arts', 'Единоборства'),
    ('other', 'Другой вид спорта'),
]


class AthleteForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=100)
    last_name = forms.CharField(label="Фамилия", max_length=100)
    middle_name = forms.CharField(label="Отчество", 
                                  max_length=100, 
                                  required=False)
    birth_date = forms.DateField(
        label="Дата рождения", 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    sex = forms.ChoiceField(
        label="Пол",
        choices=SEX_CHOICES,
        widget=forms.RadioSelect
    )

    sport = forms.ChoiceField(label="Вид спорта", choices=SPORT_CHOICES)
    rank = forms.ChoiceField(label="Разряд / Звание", choices=RANK_CHOICES)
    city = forms.CharField(label="Город", max_length=100, required=False)
    team = forms.CharField(label="Клуб / Команда", max_length=150, required=False)


    def clean_birth_date(self):
        birth_date_val = self.cleaned_data.get('birth_date')
        if birth_date_val > date.today():
            raise ValidationError("Дата рождения не может быть в будущем!")
        elif birth_date_val.year <= 1900:
            raise ValidationError("Столько не живут")
        return birth_date_val.strftime("%Y-%m-%d")


class JSONFileForm(forms.Form):
    json_file = forms.FileField(
        label="Загрузить JSON-фаил базы данных",
        help_text="Файл должен содержать список словарей в формате JSON."
    )

    def clean_json_file(self):
        uploaded_file = self.cleaned_data.get('json_file')

        if not uploaded_file.name.endswith('.json'):
            raise ValidationError("Допускается только JSON фаил (<filename>.json)!")

        try:
            file_data = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)

            data = json.loads(file_data)
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise ValidationError("Фаил поврежден или имеет невурную кодировку")
        except Exception as e:
            raise ValidationError(f"Непредвиденная ошибка при чтении фаила!\nОШИБКА: {str(e)}")

        if not isinstance(data, list):
            raise ValidationError("Неверная структура в корне файла. Должен Быть Список!")

        required_keys = {'last_name', 'first_name', 'middle_name', 'birth_date', 'sex', 'sport', 'rank'}
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValidationError(f"Элемент id:{idx} не является объектом Словарь (dict)")

            missing_keys = required_keys - set(item.keys())
            if missing_keys:
                raise ValidationError(
                    f"В элементе id:{idx} отсутсвуют обязательные поля: {', '.join(missing_keys)}"
                )

        return data