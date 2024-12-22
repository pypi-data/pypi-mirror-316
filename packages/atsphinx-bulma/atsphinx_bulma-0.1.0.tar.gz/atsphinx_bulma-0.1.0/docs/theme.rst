===========
Using theme
===========

Overview
========

This provides theme to display contents designed by Bulma.

Requirements
============

This does not have extra requirements.
You can use soon after install atsphinx-bulma.

Usage
=====

.. code-block:: python
   :caption: conf.py

   html_theme = "bulma-basic"

Options
=======

* **bulma_version** : Version of bulma to fetch from CDN. Default is ``'1.0.2'``.
* **bulmaswatch** : Theme name of `bulmaswatch <https://jenil.github.io/bulmaswatch/>`_ if it is set no-blank string. Default is ``''``.
* **color_mode** : Using color mode. Set ``'light'``, ``'dark'`` , ``''``.
* **sidebar_position**: Which sidebar renders on content. Set ``'left'`` or ``'right'``.
* **navbar_icons** : Configurations for icons on navbar (top of page).
* **show_theme_credit** : Please set ``False`` if you don't want to render credit of this extension.
