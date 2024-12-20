# django-localhost-run

## Käyttöönotto

### Järjestelmävaatimukset

* SSH-pääteohjelmisto
* Python 3.8 tai uudempi
* Django 4.2.1 tai uudempi

### Asennus

```bash
pip install django-localhost-run
```

### Django-projektiasetukset

Lisää Django-projektiasetuksiin:
```python
# projekti/asetukset.py
...
INSTALLED_APPS = [
  'localhost_run',  # ennen staticfiles-sovellusta
  ...
  'django.contrib.staticfiles', # tarvittaessa
  ...
]
```

## Käyttö

Paketti periyttää `runserver`-komennon siten, että:
- vipu `python manage.py runserver --lhr` ottaa Localhost.run-tunnelin
  käyttöön
- kun vipu on päällä:
  - avataan tunneli ennen kehityspalvelimen käynnistymistä
  - tulostetaan tunnelin julkinen https-osoite konsoliin
  - asetetaan tämä https-osoite myös `LOCALHOST_RUN`-ympäristömuuttujaan
    käynnissä olevan palvelimen sisällä
