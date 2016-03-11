import requests
import json

class StockMinion(object):

    def __init__(self, api_key = None):
        self.session = requests.Session()
        if(api_key):
            header = {'X-Starfighter-Authorization' : api_key}
            self.session.headers.update(header)

    def check_api(self):
        
        resp = self.session.get(BASE_URL + 'heartbeat')
        data = StockMinion._process_response(resp.text, resp.status_code)
        return data

    
    def check_venue(self, venue):

        resp = self.session.get(BASE_URL + 'venues/%s/heartbeat' % venue)
        data = StockMinion._process_response(resp.text, resp.status_code)    
        return data


    def get_stocks_on_venue(self, venue):

        resp = self.session.get(BASE_URL + 'venues/%s/stocks' % venue)
        data = StockMinion._process_response(resp.text, resp.status_code)
        return data
    
    
    def get_orderbook(self, venue, stock):

        resp = self.session.get(BASE_URL + 'venues/%s/stocks/%s' % (venue, stock))
        data = StockMinion._process_response(resp.text, resp.status_code)
        return data


    def place_order(self, **kwargs):

        mandatory = ['account', 'venue', 'stock', 'direction', 'orderType']
        missing_args = [x for x in mandatory if x not in kwargs]
        
        if(missing_args):
            raise ValueError("Missing '%s' arguments in function call" % (', '.join(missing_args)))
        
        # leave the dictionary packed
        request_body = kwargs
        resp = self.session.post(BASE_URL + 'venues/%s/stocks/%s/orders' % (kwargs['venue'], kwargs['stock']),
                                 data = json.dumps(request_body))
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
            print("Got a status code of %d" % code)
        else:
            pass

    @staticmethod
    def _process_response(json_obj, code):
        
        data = StockMinion._process_json(json_obj)
        StockMinion._process_status(code)
        return data

    

    
if __name__ == '__main__':

    BASE_URL = "https://api.stockfighter.io/ob/api/"
    TEST_VENUE = "TESTEX"
    TEST_STOCK    = "FOOBAR"
    TEST_ACCOUNT  = "EXB123456"

    instance = StockMinion()

    data = instance.check_api()
    print(data)

    data = instance.check_venue(TEST_VENUE)
    print(data)

    data = instance.get_stocks_on_venue(TEST_VENUE)
    print(data)

    data = instance.get_orderbook(TEST_VENUE, TEST_STOCK)
    print(data)

    data = instance.place_order(account = TEST_ACCOUNT, venue = TEST_VENUE, stock = TEST_STOCK,  direction = "buy", orderType = "market")
    print(data)
