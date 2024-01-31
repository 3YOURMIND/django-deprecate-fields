# Copyright 2018 3YOURMIND GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from codecs import open
from os import path

from setuptools import setup

PROJECT_DIR = path.abspath(path.dirname(__file__))

long_description = open("README.md").read()

install_requirements = ["Django>=2.1"]

setup(
    name="django-deprecate-fields",
    version="0.1.2",
    description="This package allows deprecating model fields and allows "
    "removing them in a backwards compatible manner.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/3YOURMIND/django-deprecate-fields",
    author="3YOURMIND GmbH",
    license="Apache License 2.0",
    packages=["django_deprecate_fields"],
    install_requires=install_requirements,
    keywords="django migration deprecation database backward compatibility",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
