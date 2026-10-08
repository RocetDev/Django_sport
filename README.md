
# Sport base list

Приложение позволяет сохранять спотрсменов в базе, добавляя их через форму или json фаил с определенной структурой.

## Quick-start
Запустите эти команды для запуска всего приложеняи у себя:

    git clone https://github.com/RocetDev/Django_sport.git
    cd Django_sport
    
    #если вы делаете через python pip
    pip install -r requirements.txt
    python manage.py runserver
    
    #если вы используете uv
    uv sync
    uv run manage.py runserver

## Структура загружаемого JSON файла
Загружаемый фаил json должен иметь определенный формат иначе возникнет ошибка при загрузке:

    [
	    {
		    "first_name": "adfa",
		    "last_name": "asdf",
		    "middle_name": "asdf",
		    "birth_date": "2026-09-01",
		    "sex": "M",
		    "sport": "swimming",
		    "rank": "1y",
		    "city": "Магнитогорск",
		    "team": "tema"
	    },
	    ...
    ]
