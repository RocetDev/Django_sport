from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

from . import storage
from .forms import AthleteForm, JSONFileForm
from .models import Athlete


def index(request):
    source = request.GET.get('source', 'json')
    context = {
        'source': source,
        'athletes': [],
        'db_athletes': [],
    }

    if source == 'db':
        context['db_athletes'] = Athlete.objects.all()
    else:
        context['athletes'] = storage.read_base()

    return render(request, 'index.html', context)


def search_db(request):
    """(API): AJAX-поиск по записям в БД."""
    query = request.GET.get('q', '').strip().lower()

    athletes = []
    for a in Athlete.objects.all():
        fields = [a.first_name, a.last_name, a.middle_name, a.city, a.team]
        if any(query in (f or '').lower() for f in fields):
            athletes.append(a)

    data = []
    for a in athletes:
        data.append({
            'id': a.id,
            'full_name': str(a),
            'birth_date': a.birth_date.strftime('%d.%m.%Y'),
            'sex': 'Муж' if a.sex == 'M' else 'Жен',
            'sport': a.get_sport_display(),
            'rank': a.get_rank_display(),
            'city': a.city or '—',
            'team': a.team or '—',
        })

    return JsonResponse({'athletes': data})


def add_form(request):
    if request.method == "POST":
        form = AthleteForm(request.POST)
        if form.is_valid():
            storage_type = request.POST.get('db_type')

            if storage_type == 'database':
                data = form.cleaned_data

                # проверка на дубликат
                exists = Athlete.objects.filter(
                    last_name=data['last_name'],
                    first_name=data['first_name'],
                    birth_date=data['birth_date'],
                ).exists()

                if exists:
                    messages.error(request, 'Такая запись уже есть в базе данных!')
                else:
                    Athlete.objects.create(**data)
                    messages.success(request, 'Запись сохранена в базу данных.')

                return redirect('index')

            current_data = storage.read_base()
            current_data.append(form.cleaned_data)
            storage.write_base(current_data)
            messages.success(request, 'Запись сохранена в файл JSON.')

            return redirect('index')
    else:
        form = AthleteForm()

    return render(request, 'add_form.html', {'form': form})


def upload_file(request):
    if request.method == "POST":
        form = JSONFileForm(request.POST, request.FILES)
        if form.is_valid():
            storage_type = request.POST.get('db_type')
            uploaded_data = form.cleaned_data['json_file']

            if storage_type == 'database':
                # добавляем только те записи, которых ещё нет в БД
                added = 0
                skipped = 0
                for item in uploaded_data:
                    exists = Athlete.objects.filter(
                        last_name=item['last_name'],
                        first_name=item['first_name'],
                        birth_date=item['birth_date'],
                    ).exists()

                    if exists:
                        skipped += 1
                    else:
                        Athlete.objects.create(**item)
                        added += 1

                messages.success(
                    request,
                    f'Добавлено записей: {added}, пропущено дубликатов: {skipped}.'
                )
            else:
                current_data = storage.read_base()
                current_data.extend(uploaded_data)
                storage.write_base(current_data)
                messages.success(request, 'Записи добавлены в файл JSON.')

            return redirect('index')
    else:
        form = JSONFileForm()

    return render(request, 'upload_form.html', {'form': form})


def edit_form(request, athlete_id):
    athlete = get_object_or_404(Athlete, id=athlete_id)

    if request.method == "POST":
        form = AthleteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # проверка на дубликат кроме самой этой записи
            exists = Athlete.objects.filter(
                last_name=data['last_name'],
                first_name=data['first_name'],
                birth_date=data['birth_date'],
            ).exclude(id=athlete.id).exists()

            if exists:
                messages.error(request, 'Такая запись уже есть в базе данных!')
            else:
                for field, value in data.items():
                    setattr(athlete, field, value)
                athlete.save()
                messages.success(request, 'Запись обновлена.')
                return redirect('index')
    else:
        form = AthleteForm(initial={
            'first_name': athlete.first_name,
            'last_name': athlete.last_name,
            'middle_name': athlete.middle_name,
            'birth_date': athlete.birth_date,
            'sex': athlete.sex,
            'sport': athlete.sport,
            'rank': athlete.rank,
            'city': athlete.city,
            'team': athlete.team,
        })

    return render(request, 'add_form.html', {'form': form, 'is_edit': True})


def delete_form(request, athlete_id):
    athlete = get_object_or_404(Athlete, id=athlete_id)

    if request.method == "POST":
        athlete.delete()
        messages.success(request, 'Запись удалена.')
        return redirect('index')

    return render(request, 'delete_form.html', {'athlete': athlete})
