Netlify Provider
================

.. versionadded:: 1.0.0

The ``netlify`` provider allows you to deploy your static site to `Netlify`_.

uHugo automatically detects the ``netlify`` provider if you have a ``netlify.toml`` file in your project and searches for ``HUGO_VERSION`` key in the ``[context.production.environment]`` section.
If found, uHugo will update it to the latest version of Hugo. It also, updates the preview builds to the latest version of Hugo in the ``[context.deploy-preview.environment]`` section.

.. _netlify: https://www.netlify.com/
