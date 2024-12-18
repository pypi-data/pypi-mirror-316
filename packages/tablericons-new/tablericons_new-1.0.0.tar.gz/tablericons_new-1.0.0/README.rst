===========
tablericons
===========

.. image:: https://img.shields.io/github/actions/workflow/status/gartmeier/tablericons/main.yml.svg?branch=main&style=for-the-badge
   :target: https://github.com/gartmeier/tablericons/actions?workflow=CI

.. image:: https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge
   :target: https://github.com/gartmeier/tablericons/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/tablericons-new.svg?style=for-the-badge
   :target: https://pypi.org/project/tablericons-new/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

Use `tablericons <https://tablericons.com/>`__ in your Django and Jinja templates.

Requirements
------------

Python 3.9 to 3.13 supported.

Django 4.2 to 5.1 supported.

Usage
-----

The ``tablericons-new`` package supports both Django templates and Jinja templates.
Follow the appropriate guide below.

Django templates
~~~~~~~~~~~~~~~~

1. Install with ``python -m pip install tablericons-new[django]``.

2. Add to your ``INSTALLED_APPS``:

   .. code-block:: python

       INSTALLED_APPS = [
           ...,
           "tablericons",
           ...,
       ]

Now your templates can load the template library with:

.. code-block:: django

    {% load tablericons %}

Alternatively, make the library available in all templates by adding it to `the builtins option <https://docs.djangoproject.com/en/stable/topics/templates/#django.template.backends.django.DjangoTemplates>`__:

.. code-block:: python

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            # ...
            "OPTIONS": {
                # ...
                "builtins": [
                    ...,
                    "tablericons.templatetags.tablericons",
                    ...,
                ],
            },
        }
    ]

The library provides these tags to render SVG icons in their corresponding styles:

* ``tablericon_outline``
* ``tablericon_filled``

The tags take these arguments:

* ``name``, positional: the name of the icon to use.
  You can see the icon names on the `tablericons.com grid <https://tablericons.com/>`__.

* ``size``, keyword: an integer that will be used for the width and height attributes of the output ``<svg>`` tag.
  Defaults to the icons’ designed sizes: ``24`` for outline and solid, ``20`` for mini, and ``16`` for micro.
  Can be ``None``, in which case no width or height attributes will be output.

* Any number of keyword arguments.
  These will be added as attributes in the output HTML.
  Underscores in attribute names will be replaced with dashes, allowing you to define e.g. ``data-`` attributes.

  Most attributes will be added to the ``<svg>`` tag containing the icon, but these attributes will be attached to the inner ``<path>`` tags instead:

  * ``stroke-linecap``
  * ``stroke-linejoin``
  * ``vector-effect``

Examples
^^^^^^^^

An outline “school” icon:

.. code-block:: django

    {% tablericon_outline "school" %}

The same icon, solid, at 40x40 pixels, and a CSS class:

.. code-block:: django

    {% tablericon_outline "school" size=40 class="mr-4" %}

That icon again, but with the paths changed to a narrower stroke width, and a "data-controller" attribute declared:

.. code-block:: django

    {% tablericon_outline "school" stroke_width=1 data_controller="academia" %}

Jinja templates
~~~~~~~~~~~~~~~

1. Install with ``python -m pip install tablericons-new[jinja]``.

2. Adjust your Jinja ``Environment`` to add the global ``tablericon_*`` functions from ``tablericons.jinja``.
   For example:

   .. code-block:: python

       from tablericons.jinja import (
           tablericon_outline,
           tablericon_filled,
       )
       from jinja2 import Environment

       env = Environment()
       env.globals.update(
           {
               "tablericon_outline": tablericon_outline,
               "tablericon_filled": tablericon_filled,
           }
       )

Now in your templates you can call those functions, which render ``<svg>`` icons corresponding to the icon styles in the set.
The functions take these arguments:

* ``name``, positional: the name of the icon to use.
  You can see the icon names on the `tablericons.com grid <https://tablericons.com/>`__.

* ``size``, keyword: an integer that will be used for the width and height attributes of the output ``<svg>`` tag.
  Defaults to the icons’ designed sizes: ``24`` for outline and solid, ``20`` for mini, and ``16`` for micro.
  Can be ``None``, in which case no width or height attributes will be output.

* Any number of keyword arguments.
  These will be added as HTML attributes to the output HTML.
  Underscores in attribute names will be replaced with dashes, allowing you to define e.g. ``data-`` attributes.

  Most attributes will be added to the ``<svg>`` tag containing the icon, but these attributes will be attached to the inner ``<path>`` tags instead:

  * ``stroke-linecap``
  * ``stroke-linejoin``
  * ``vector-effect``

Note: unlike the SVG code you can copy from `tablericons.com <https://tablericons.com/>`__, there is no default ``class``.

Examples
^^^^^^^^

An outline “egg” icon:

.. code-block:: jinja

    {{ tablericon_outline("egg") }}

The same icon, solid, at 40x40 pixels, and a CSS class:

.. code-block:: jinja

    {{ tablericon_filled("egg", size=40, class="mr-4") %}

That icon again, but with the paths changed to a narrower stroke width, and a "data-controller" attribute declared:

.. code-block:: jinja

    {{ tablericon_outline("egg", stroke_width=1, data_controller="academia") %}

Acknowledgements
----------------

This package is heavely inspired by [Adam Johnson's heroicons](https://github.com/gartmeier/heroicons). It's actually mostly copied from it so a huge thanks Adam!
