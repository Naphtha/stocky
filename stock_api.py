import requests
import json

class Stock_Minion(object):

    def check_api():
        
        resp = requests.get(BASE_URL + 'heartbeat')
        data = _process_response(resp.text, resp.status_code)
        return data

    
    def check_venue(venue_symbol):

        resp = requests.get(BASE_URL + 'venues/%s/heartbeat' % venue_symbol)
        data = _process_response(resp.text, resp.status_code)    
        return data


    def get_stocks_on_venue(venue_symbol):

        resp = requests.get(BASE_URL + 'venues/%s/stocks' % venue_symbol)
        data = _process_response(resp.text, resp.status_code)
        return data
    
    
    def get_orderbook(venue_symbol, stock_symbol):

        resp = requests.get(BASE_URL + 'venues/%s/stocks/%s' % (venue_symbol, stock_symbol))
        data = _process_response(resp.text, resp.status_code)
        return data


    def place_order(account, venue_symbol, stock_symbol, price, qty, direction, order_type):
        resp = requests.post(BASE_URL + '')

    
    def _process_json(json_obj):

        try:
            data = json.loads(json_obj)
        except ValueError as e:
            data = {}
            print(e)

        return data

    
    def _process_status(code):

        if(code != 200):
            print("Got a status code of %d" % code)
        else:
            pass

    
    def _process_response(json_obj, code):

        data = _process_json(json_obj)
        _process_status(code)

        return data

    

    
if __name__ == '__main__':

    BASE_URL = "https://api.stockfighter.io/ob/api/"
    TEST_EXCHANGE = "TESTEX"
    TEST_STOCK    = "FOOBAR"
    TEST_ACCOUNT  = "EXB123456"

    data = check_api()
    print(data)

    data = check_venue(TEST_EXCHANGE)
    print(data)

    data = get_stocks_on_venue(TEST_EXCHANGE)
    print(data)

    data = get_orderbook(TEST_EXCHANGE, TEST_STOCK)
    print(data)
