import requests
import json

BASE_URL = "https://api.stockfighter.io/ob/api/"

class StockMinion(object):

    
    def __init__(self, api_key, account, venue, stock):
        self.session = requests.Session()
        header = {'X-Starfighter-Authorization' : api_key}
        self.session.headers.update(header)
        self.account = account
        self.venue = venue
        self.stock = stock
        
        
    def check_api(self):
        
        data = self._call_api(BASE_URL + 'heartbeat', 'get')

        return data

    
    def check_venue(self):

        venue = self.venue
        
        data = self._call_api(BASE_URL + 'venues/{0}/heartbeat'.format(venue), 'get')

        return data


    def get_stocks_on_venue(self):

        venue = self.venue
        
        data = self._call_api(BASE_URL + 'venues/{0}/stocks'.format(venue), 'get')
        
        return data
    
    
    def get_orderbook(self):

        venue = self.venue
        stock = self.stock
        
        data = self._call_api(BASE_URL + 'venues/{0}/stocks/{1}'.format(venue, stock), 'get')
        
        return data


    # using kwargs here allows me to call this function with keywords or with a dict
    def place_order(self, **kwargs):

        kwargs['account'] = self.account
        kwargs['stock'] = self.stock
        kwargs['venue'] = self.venue

        mandatory = ['account', 'venue', 'stock', 'qty', 'direction', 'orderType']
        missing_args = [x for x in mandatory if x not in kwargs]

        # raises exception with missing operands
        if(missing_args):
            raise TypeError("Missing '{0}' arguments in function call".format(', '.join(missing_args)))
        
        # leave the dictionary packed
        request_body = kwargs
        data = self._call_api(BASE_URL + 'venues/{0}/stocks/{1}/orders'.format(kwargs['venue'], kwargs['stock']),
                              'post', data=json.dumps(request_body))
        return data
        
    def get_quote(self):

        venue = self.venue
        stock = self.stock

        data = self._call_api(BASE_URL + 'venues/{0}/stocks/{1}/quote'.format(venue, stock), 'get')
        
        return data

    def get_order_status(self, id):

        venue = self.venue
        stock = self.stock
        
        data = self._call_api(BASE_URL + 'venues/{0}/stocks/{1}/orders/{2}'.format(venue, stock, id), 'get')
        
        return data

    def cancel_order(self, id):

        venue = self.venue
        stock = self.stock
        
        data = self._call_api(BASE_URL + 'venues/{0}/stocks/{1}/orders/{2}'.format(venue, stock, id), 'delete')
        
        return data

    def get_all_orders(self, stock = None):

        venue = self.venue
        account = self.account
        
        if(stock):
            data = self._call_api(BASE_URL + 'venues/{0}/accounts/{1}/stocks/{2}/orders'.format(venue, account, stock), 'get')
        else:
            data = self._call_api(BASE_URL + 'venues/{0}/accounts/{1}/orders'.format(venue, account), 'get')
        return data


    def _call_api(self, url, verb, *args, **kwargs):

        func = getattr(self.session, verb)
        resp = func(url, *args, **kwargs)

        data = StockMinion._process_response(resp.text, resp.status_code)
        return data

        
    @staticmethod
    def _process_json(json_obj):

        try:
            data = json.loads(json_obj)
        except ValueError as e:
            data = {}
            print(e)
        return data

    @staticmethod
    def _process_status(code):

        if(code != 200):
            print("Got a status code of {0}".format(code))
        else:
            pass

    @staticmethod
    def _process_response(json_obj, code):
        
        data = StockMinion._process_json(json_obj)
        StockMinion._process_status(code)
        return data

    

    
if __name__ == '__main__':

    TEST_VENUE = "TESTEX"
    TEST_STOCK    = "FOOBAR"
    TEST_ACCOUNT  = "EXB123456"

    # pick up api key from local untracked file
    with open('api.key', 'r') as secret_file:
        API_KEY = secret_file.readlines()[0].rstrip('\n')

    instance = StockMinion(API_KEY, TEST_ACCOUNT, TEST_VENUE, TEST_STOCK)

    data = instance.check_api()
    print(data)

    data = instance.check_venue()
    print(data)

    data = instance.get_stocks_on_venue()
    print(data)

    data = instance.get_orderbook()
    print(data)

    data = instance.place_order(qty = 100, direction = "buy", orderType = "limit", price = 100)
    print(data)

    order_num = data['id']
    
    data = instance.get_quote()
    print(data)
    
    data = instance.get_order_status(order_num)
    print(data)

    data = instance.cancel_order(order_num)
    print(data)

    data = instance.get_all_orders()
    print(data)

    data = instance.get_all_orders(TEST_STOCK)
    print(data)

