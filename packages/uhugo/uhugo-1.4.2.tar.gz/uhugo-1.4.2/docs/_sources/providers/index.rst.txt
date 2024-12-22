Providers
=========

.. versionadded:: 0.0.3

Providers are cloud hosted services that host your static website. uHugo comes with three providers - Netlify, Cloudflare and Vercel.

Every provider has their own configuration files.

1. Netlify - ``netlify.toml``
2. Cloudflare - ``config.[toml|yaml]``
3. Vercel - ``vercel.json``

.. note:: For Cloudflare, the configurations must be put in Hugo's ``config.[toml|yaml]`` file.

Supported Providers
-------------------

Let's look at the providers in detail.

.. toctree::
    :maxdepth: 2
 
    cloudflare
    netlify
    vercel
