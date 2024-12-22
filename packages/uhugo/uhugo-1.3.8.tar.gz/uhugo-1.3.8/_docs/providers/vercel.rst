Vercel Provider
===============

.. versionadded:: 1.0.0

The ``vercel`` provider allows you to deploy your static site to `Vercel`_.

uHugo automatically detects the ``vercel`` provider if you have a ``vercel.json`` file in your project and searches for ``HUGO_VERSION`` key in the ``env`` section.
If found, uHugo will update it to the latest version of Hugo.

.. _Vercel: https://vercel.com/
