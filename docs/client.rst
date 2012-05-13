Authorize interface
===================

.. automodule:: authorize.client

Authorize client
----------------

.. autoclass:: authorize.client.AuthorizeClient
    :members: card, transaction, saved_card, recurring

Credit card
-----------

.. autoclass:: authorize.client.AuthorizeCreditCard
    :members: auth, capture, credit, save, recurring

Transaction
-----------

.. autoclass:: authorize.client.AuthorizeTransaction
    :members: settle, credit, void

Saved card
----------

.. autoclass:: authorize.client.AuthorizeSavedCard
    :members: auth, capture, credit, delete

Recurring charge
----------------

.. autoclass:: authorize.client.AuthorizeRecurring
    :members: update, delete
