# Django - Deprecate Field

[![PyPi](https://img.shields.io/pypi/v/django-deprecate-fields.svg?branch=master)](https://pypi.python.org/pypi/django-deprecate-fields/)
[![License](https://img.shields.io/github/license/3yourmind/django-deprecate-fields.svg)](./LICENSE)
[![Contributing](https://img.shields.io/badge/PR-welcome-green.svg)](https://github.com/3YOURMIND/django-deprecate-fields/pulls)
[![3yourminD-Careers](https://img.shields.io/badge/3YOURMIND-Hiring-brightgreen.svg)](https://www.3yourmind.com/career)
[![Stars](https://img.shields.io/github/stars/3YOURMIND/django-deprecate-fields.svg?style=social&label=Stars)](https://github.com/3YOURMIND/django-deprecate-fields/stargazers)

## Installation

```
pip install django-deprecate-fields
```

## Usage

Assume the simple following model:
```python
from django.db import models

class MyModel(models.Model):
    field1 = models.CharField()
    field2 = models.CharField()
```

In order to remove `field1`, it should first be marked as deprecated:
```python
from django.db import models
from django_deprecate_fields import deprecate_field

class MyModel(models.Model):
    field1 = deprecate_field(models.CharField())
    field2 = models.CharField()
```

Secondly, `makemigrations` should be called, which will change the field to be nullable. Any lingering references to it
in your code will return `None` (or optionally any value or callable passed to `deprecate_field` as the
`return_instead` argument)

Lastly, after the changes above have been deployed, `field1` can then safely be removed in the model (plus another
`makemigrations` run)

### Custom django commands

If you need the actual field to be returned when a django command other than `makemigrations`, `migrate` or `showmigrations` is run, you can use the
`commands_requiring_concrete_class` parameter.

For instance if you generate migrations with `pgmakemigrations` instead of `makemigrations`, you can create the field
this way
```python
    deprecate_field(models.CharField(), commands_requiring_concrete_class={"pgmakemigrations"})
```

## Contributing

First of all, thank you very much for contributing to this project. Please base
your work on the `master` branch and target `master` in your pull request.

## License

`django-deprecate-fields` is released under the [Apache 2.0 License](./LICENSE).
