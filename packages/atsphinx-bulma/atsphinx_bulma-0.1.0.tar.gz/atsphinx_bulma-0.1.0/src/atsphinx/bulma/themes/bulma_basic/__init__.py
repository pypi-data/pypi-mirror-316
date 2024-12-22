"""Entrypoint of theme."""

from pathlib import Path

from sphinx.application import Sphinx

here = Path(__file__).parent


def setup(app: Sphinx):  # noqa: D103
    app.add_html_theme("bulma-basic", str(here))
    app.setup_extension("atsphinx.bulma")
