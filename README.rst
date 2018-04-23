Authorize Sauce
===============


🔥 WARNING 🔥
-------
Authorize.Net has deprecated their SOAP APIs and plans to end-of-life them at some point. This applies to the Customer and Recurring APIs in this library. The Transaction API uses AIM and is still currently supported but Authorize.Net recommends using the new API.
See https://developer.authorize.net/api/upgrade_guide/ under `API Support Status`

*Recommend moving to official Authorize.Net SDK for python:*

* https://github.com/AuthorizeNet/sdk-python
* https://github.com/AuthorizeNet/sample-code-python

Also, see the forum issue with the SOAP API:

* https://community.developer.authorize.net/t5/Integration-and-Testing/CIM-SOAP-API-returning-a-550-error-on-sandbox-and-production/m-p/62769/highlight/true#M37030

😢

----

.. image:: https://img.shields.io/travis/drewisme/authorizesauce.svg
   :target: https://travis-ci.org/drewisme/authorizesauce
.. image:: https://img.shields.io/codecov/c/github/drewisme/authorizesauce.svg
   :target: https://codecov.io/github/drewisme/authorizesauce
.. image:: https://img.shields.io/pypi/pyversions/AuthorizeSauce.svg
   :target: https://pypi.python.org/pypi/AuthorizeSauce
.. image:: https://img.shields.io/pypi/l/AuthorizeSauce.svg
   :target: https://pypi.python.org/pypi/AuthorizeSauce

The secret sauce for accessing the Authorize.net API. The Authorize APIs for
transactions, recurring payments, and saved payments are all different and
awkward to use directly. Instead, you can use Authorize Sauce, which unifies
all three Authorize.net APIs into one coherent Pythonic interface. Charge
credit cards, easily!

::

  >>> # Init the authorize client and a credit card
  >>> from authorize import AuthorizeClient, CreditCard
  >>> client = AuthorizeClient('285tUPuS', '58JKJ4T95uee75wd')
  >>> cc = CreditCard('4111111111111111', '2018', '01', '911', 'Joe', 'Blow')
  >>> card = client.card(cc)

  >>> # Charge a card
  >>> card.capture(100)
  <AuthorizeTransaction 2171829470>

  >>> # Save the card on Authorize servers for later
  >>> saved_card = card.save()
  >>> saved_card.uid
  '7713982|6743206'

  >>> # Use a saved card to auth a transaction, and settle later
  >>> saved_card = client.saved_card('7713982|6743206')
  >>> transaction = saved_card.auth(200)
  >>> transaction.settle()

Saucy Features
--------------

* Charge a credit card
* Authorize a credit card charge, and settle it or release it later
* Credit or refund to a card
* Save a credit card securely on Authorize.net's servers
* Use saved cards to charge, auth and credit
* Create recurring charges, with billing cycles, trial periods, etc.

For the full documentation, please visit us at `Read the Docs`_. Thanks to
Chewse_ for supporting the development and open-sourcing of this library.
Authorize Sauce is released under the `MIT License`_.

.. _Read the Docs: http://authorizesauce.readthedocs.io/
.. _Chewse: https://www.chewse.com/
.. _MIT License: http://www.opensource.org/licenses/mit-license
