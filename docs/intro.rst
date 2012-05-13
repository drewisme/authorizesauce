Introduction
============

Here you'll find an easy introduction to charging credit cards with Authorize
Sauce. We'll take you through the basics of charging, saving cards, and
creating recurring payments.

For the full scoop on interacting with the Authorize Sauce client, see the
:doc:`client` documentation.

Initialize the client
---------------------

Whatever you plan to do, your first step will be to create the
:class:`AuthorizeClient <authorize.client.AuthorizeClient>` instance using
your Authorize.net API login and transaction key::

    >>> from authorize import AuthorizeClient
    >>> client = AuthorizeClient('285tUPuS', '58JKJ4T95uee75wd')

Charge a credit card
--------------------

Using the Authorize.net client, we can now create a
:class:`CreditCard <authorize.data.CreditCard>` object and create a $100
charge with it. We'll also store a reference to the transaction just in case
we need to refund it later::

    >>> from authorize import CreditCard
    >>> cc = CreditCard('4111111111111111', '2018', '01', '911', 'Joe', 'Blow')
    >>> transaction = client.card(cc).capture(100)
    >>> # Save the uid for this charge in case we need to refund it later
    >>> transaction.uid
    '2171830830'

Oh crap, someone wants a refund. That sucks for business, but at least it's
not hard to do in Awesome Sauce::

    >>> # Reference the transaction from earlier
    >>> transaction = client.transaction('2171830830')
    >>> # Refund the earlier transaction, passing in the last four digits of the card for verification
    >>> transaction.credit('1111')
    <AuthorizeTransaction 2171830830>

Authorize a credit card
-----------------------

If you want to simply authorize a credit card for a certain amount, but don't
want to actually settle that charge until later, we make that easy too! Let's
start by authorizing a $100 payment::

    >>> cc = CreditCard('4111111111111111', '2018', '01', '911', 'Joe', 'Blow')
    >>> transaction = client.card(cc).auth(100)
    >>> # Save the uid for this auth so we can settle it at a later date
    >>> transaction.uid
    '2171830878'

So let's say we've rendered services and we're ready to settle that $100
transaction from earlier. Easy::

    >>> # Reference the transaction from earlier
    >>> transaction = client.transaction('2171830878')
    >>> transaction.settle()
    <AuthorizeTransaction 2171830878>

But what if the total your customer owed came out to be less than that
original $100 authorization? You can just as easily capture a smaller amount
than the original authorization::

    >>> # Reference the transaction from earlier
    >>> transaction = client.transaction('2171830878')
    >>> transaction.settle(50)
    <AuthorizeTransaction 2171830878>

Save a credit card
------------------

Let's say you want to save a customer's credit card to make it easier for them
to check out next time they're on your site::

    >>> saved_card = client.card(cc).save()
    >>> # Save the uid of the saved card so you can reference it later
    >>> saved_card.uid
    '7715743|6744936'

Now all you have to do is save that ``uid`` in your database, instead of
storing sensitive credit card data, and you can charge the card again later.

    >>> # Reference the saved card uid from earlier
    >>> saved_card = client.saved_card('7715743|6744936')
    >>> # Let's charge another $500 to this card for another purchase
    >>> saved_card.capture(500)
    <AuthorizeTransaction 2171830935>

If your user ever requests that you delete this card from its secure storage
on Authorize.net's servers, we can do that too::

    >>> saved_card = client.saved_card('7715743|6744936')
    >>> saved_card.delete()

Create a recurring payment
--------------------------

Next you decide you want recurring revenue, so you're going to charge your
users a monthly $20 subscription fee starting Dec 1, 2012. This is simple to
set up::

    >>> from datetime import date
    >>> card = client.card(cc)
    >>> card.recurring(20, date(2012, 12, 1), months=1)
    <AuthorizeRecurring 1396734>

Again, if you want to update the recurring payment, this is easy to do. Let's
say we need to increase the monthly rate to $25::

    >>> # Reference the recurring uid from earlier
    >>> recurring = client.recurring('1396734')
    >>> recurring.update(amount=25)

And if the user cancels their service, we can end their recurring payment::

    >>> recurring = client.recurring('1396734')
    >>> recurring.delete()

There are many other available options when setting up recurring payments,
such as trial periods and limited number of payments. For details, see the
:meth:`AuthorizeCreditCard.recurring <authorize.client.AuthorizeCreditCard.recurring>`
method documentation.
