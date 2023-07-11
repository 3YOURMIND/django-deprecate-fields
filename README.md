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
`return_instead` argument, see below for more info).

Lastly, after the changes above have been deployed, `field1` can then safely be removed in the model (plus another
`makemigrations` run)

## Modifying the returned value

`deprecate_field` has an optional `return_instead` parameter which accepts
either a static value or a one-argument callable, when the deprecated field is
accessed, the value that is returned will depend on the argument passed to the
`return_instead` parameter.

### Static values

Returning a static value on deprecated field access is pretty simple, all
you have to do is pass a Python literal, variable, constant, etc. as argument
to the `return_instead` parameter like so:

```python
from django.db import models
from django_deprecate_fields import deprecate_field

class MyModel(models.Model):
    field1 = deprecate_field(models.CharField(), return_instead="Foo")
    field2 = models.CharField()
```

Now every time `MyModel.field1` is accessed `"foo"` will be returned.

### Dynamic values

The `return_instead` parameter also accepts callables with one argument.

This argument will always be the model instance on which the field is being
accessed, this allows you to use other Model instance attributes to alias
or even extrapolate the result of accessing the deprecated field.

Here's an example of a simple callable that will return either "foo" or "bar"
when the deprecated field is accessed, depending on luck:

```python
import random

from django.db import models
from django_deprecate_fields import deprecate_field


def my_func(_):
    # note that we don't need to extrapolate the return value based on the
    # model instance so we simply "discard" it using the _ convention
    return random.choice(["foo", "bar"])


class MyModel(models.Model):
    field1 = deprecate_field(models.CharField(), return_instead=my_func)
    field2 = models.CharField()
```

Here's an example of a callable that uses the Model instance argument which
will simply alias field1 to field2.

```python
from django.db import models
from django_deprecate_fields import deprecate_field


def my_func(obj):
    return obj.field2


class MyModel(models.Model):
    field1 = deprecate_field(models.CharField(), return_instead=my_func)
    field2 = models.CharField()
```

You can even use model methods, this is the recommended way to do it or
"best practice":

```python
from django.db import models
from django_deprecate_fields import deprecate_field



class MyModel(models.Model):

    def my_method(self):
        return self.field2

    field1 = deprecate_field(models.CharField(), return_instead=my_method)
    field2 = models.CharField()
```

These are all very simple examples but you can presumably extrapolate values
from various different fields, allowing you to refactor old code the way you
want without breaking API for your clients.

## Contributing

First of all, thank you very much for contributing to this project. Please base
your work on the `master` branch and target `master` in your pull request.

## License

`django-deprecate-fields` is released under the [Apache 2.0 License](./LICENSE).
