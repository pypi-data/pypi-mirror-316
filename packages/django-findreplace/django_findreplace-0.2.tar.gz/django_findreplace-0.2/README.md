# Django Find Replace

A [Django](https://www.djangoproject.com/) management command which will replace all instances of
a string throughout a database with another - useful for bulk content changes.

## Installation

Using [pip](https://pip.pypa.io/):

```console
$ pip install django-findreplace
```

Edit your Django project's settings module, and add the application to ``INSTALLED_APPS``:

```python
INSTALLED_APPS = [
    # ...
    "findreplace",
    # ...
]
```

## Usage

To replace all instances of *foo* with *bar*:

```console
$ ./manage.py findreplace foo bar
```

To use this command without being asked for confirmation:

```console
$ ./manage.py findreplace --noinput foo bar
```
