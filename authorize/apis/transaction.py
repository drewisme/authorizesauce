from decimal import Decimal
import urllib

from authorize.exceptions import AuthorizeConnectionError, \
    AuthorizeResponseError


PROD_URL = 'https://secure.authorize.net/gateway/transact.dll'
TEST_URL = 'https://test.authorize.net/gateway/transact.dll'
RESPONSE_FIELDS = {
    0: 'response_code',
    2: 'response_reason_code',
    3: 'response_reason_text',
    4: 'authorization_code',
    5: 'avs_response',
    6: 'transaction_id',
    9: 'amount',
    11: 'transaction_type',
    38: 'cvv_response',
}

def parse_response(response):
    response = response.split(';')
    fields = {}
    for index, name in RESPONSE_FIELDS.items():
        fields[name] = response[index]
    return fields

class TransactionAPI(object):
    def __init__(self, login_id, transaction_key, debug=True, test=False):
        self.url = TEST_URL if debug else PROD_URL
        self.base_params = {
            'x_login': login_id,
            'x_tran_key': transaction_key,
            'x_version': '3.1',
            'x_test_request': 'TRUE' if test else 'FALSE',
            'x_delim_data': 'TRUE',
            'x_delim_char': ';',
        }

    def _make_call(self, params):
        params = urllib.urlencode(params)
        url = '{0}?{1}'.format(self.url, params)
        try:
            response = urllib.urlopen(url).read()
        except IOError as e:
            raise AuthorizeConnectionError(e)
        fields = parse_response(response)
        if fields['response_code'] != '1':
            e = AuthorizeResponseError(fields['response_reason_text'])
            e.full_response = fields
            raise e
        return fields

    def _add_params(self, params, credit_card=None, address=None):
        if credit_card:
            params.update({
                'x_card_num': credit_card.card_number,
                'x_exp_date': credit_card.expiration.strftime('%m-%Y'),
                'x_card_code': credit_card.cvv,
                'x_first_name': credit_card.first_name,
                'x_last_name': credit_card.last_name,
            })
        if address:
            params.update({
                'x_address': address.street,
                'x_city': address.city,
                'x_state': address.state,
                'x_zip': address.zip_code,
                'x_country': address.country,
            })
        for key, value in params.items():
            if value is None:
                del params[key]
        return params

    def auth(self, amount, credit_card, address=None):
        amount = Decimal(str(amount)).quantize(Decimal('0.01'))
        params = self.base_params.copy()
        params = self._add_params(params, credit_card, address)
        params['x_type'] = 'AUTH_ONLY'
        params['x_amount'] = str(amount)
        return self._make_call(params)

    def capture(self, amount, credit_card, address=None):
        amount = Decimal(str(amount)).quantize(Decimal('0.01'))
        params = self.base_params.copy()
        params = self._add_params(params, credit_card, address)
        params['x_type'] = 'AUTH_CAPTURE'
        params['x_amount'] = str(amount)
        return self._make_call(params)

    def settle(self, transaction_id, amount=None):
        # Amount is not required -- if provided, settles for a lower amount
        # than the original auth; if not, settles the full amount authed.
        params = self.base_params.copy()
        params['x_type'] = 'PRIOR_AUTH_CAPTURE'
        params['x_trans_id'] = transaction_id
        if amount:
            amount = Decimal(str(amount)).quantize(Decimal('0.01'))
            params['x_amount'] = str(amount)
        return self._make_call(params)

    def credit(self, card_num, transaction_id=None, amount=None):
        # Card num must be the full card number for unlinked credits. Card
        # number can be the last four digits when transaction_id is provided.
        # If transaction_id is provided, will attempt to refund the given
        # transaction (refund amount cannot be greater, and cannot refund a
        # transaction greater than 120 days old).
        # If transaction_id is not provided, will attempt to create a credit
        # to the card unlinked to any previous transaction. NOTE: Your
        # Authorize.net account must be enabled for "expanded credits
        # capability" (ECC) to do this.
        # If transaction_id is provided, amount is optional. If provided,
        # credits the account for a lower amount than the original charge. If
        # not, credits the account for the full amount of the original charge.
        params = self.base_params.copy()
        params['x_type'] = 'CREDIT'
        params['x_trans_id'] = transaction_id
        params['x_card_num'] = card_num
        if amount:
            amount = Decimal(str(amount)).quantize(Decimal('0.01'))
            params['x_amount'] = str(amount)
        return self._make_call(params)

    def void(self, transaction_id):
        params = self.base_params.copy()
        params['x_type'] = 'VOID'
        params['x_trans_id'] = transaction_id
        return self._make_call(params)
