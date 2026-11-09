// AJAX-поиск
let token = document.querySelector('input[name=csrfmiddlewaretoken]');
let csrf = token ? token.outerHTML : '';
let timer = null;
document.getElementById('search_input').addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
        let q = document.getElementById('search_input').value;

        // пустой запрос — просто перезагружаем страницу, вернётся исходный список
        if (q.trim() === '') {
            window.location = '/?source=db';
            return;
        }

        fetch('/search/?q=' + encodeURIComponent(q))
            .then(response => response.json())
            .then(data => {
                let tbody = document.getElementById('athletes_body');
                tbody.innerHTML = '';
                if (data.athletes.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="8">Ничего не найдено.</td></tr>';
                }
                for (let a of data.athletes) {
                    tbody.innerHTML += '<tr>'
                        + '<td>' + a.full_name + '</td>'
                        + '<td>' + a.birth_date + '</td>'
                        + '<td>' + a.sex + '</td>'
                        + '<td>' + a.sport + '</td>'
                        + '<td>' + a.rank + '</td>'
                        + '<td>' + a.city + '</td>'
                        + '<td>' + a.country + '</td>'
                        + '<td>' + a.team + '</td>'
                        + '<td><a href="/edit/' + a.id + '/">Редактировать</a> '
                        + '<form method="post" action="/delete/' + a.id + '/" style="display:inline;">'
                        + csrf
                        + '<button type="submit" onclick="return confirm(\'Удалить запись?\');">Удалить</button></form></td>'
                        + '</tr>';
                }
            });
    }, 300);
});
