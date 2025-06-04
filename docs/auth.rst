.. _auth:

################################
Authentication and authorisation
################################

DQSEGDB servers can be operated in a number of authorisation modes
depending on the access controls required.

The supported modes are detailed below.

.. _noauth:

=======
No auth
=======

DQSEGDB servers can be operated without requiring any
authorisation credentials.

.. _scitokens:

=========
SciTokens
=========

DQSEGDB servers may be operated with support for
`SciTokens <https://scitokens.org>`__, an implementation of
JSON Web Tokens designed for distributed scientific computing.

When using the :doc:`query functions <api>`, the following keyword arguments
can be used with all functions to control the use of SciTokens:

``token``
    **Default**: `None`

    A bearer token (:external+scitokens:class:`~scitokens.scitokens.SciToken`)
    to use to authorise the request.

    Pass ``token=False`` to disable any use of SciTokens.

``token_audience``
    **Default**: ``<scheme://host>`` (the fully-qualified ``host`` URI)

    The expected value of the ``aud`` token claim, which should match
    the fully-qualified URL of the GWDataFind host.

``token_scope``
    **Default**: ``"dqsegdb.read"``

    The expected value of ``scope`` token claim.
    At the time of writing, only ``"dqsegdb.read"`` is supported.

.. seealso::

    For full details on token arguments and how they are parsed, see
    :external+igwn-auth-utils:py:class:`igwn_auth_utils.Session`.
