import requests
import json
import pdb
import pprint


from event import TickEvent

requests.packages.urllib3.disable_warnings()


class StreamingForexPrices(object):
    def __init__(
        self, domain, access_token,
        account_id, instruments, events_queue
    ):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.instruments = instruments
        self.events_queue = events_queue

    def connect_to_stream(self):
        try:
            s = requests.Session()
            url = "https://" + self.domain + "/v1/prices"
            headers = {'Authorization': 'Bearer ' + self.access_token}
            params = {'instruments': self.instruments, 'accountId': self.account_id}
            req = requests.Request('GET', url, headers=headers, params=params)
            pre = req.prepare()
            resp = s.send(pre, stream=True, verify=False)
            return resp
        except Exception as e:
            s.close()
            print("Caught exception when connecting to stream\n" + str(e))

    def stream_to_queue(self):
        response = self.connect_to_stream()
        if response.status_code != 200:
            return
        for line in response.iter_lines(1):
            if line:
                try:
                    msg = json.loads(line.decode())
                except Exception as e:
                    print("Caught exception when converting message into json\n" + str(e))
                    return
                if "instrument" in msg or "tick" in msg:
                    instrument = msg["tick"]["instrument"]
                    time = msg["tick"]["time"]
                    bid = msg["tick"]["bid"]
                    ask = msg["tick"]["ask"]
                    spread = round(msg["tick"]["ask"] - msg["tick"]["bid"], 10)
                    msg['tick']['spread'] = spread
                    #print(msg)
                    #pdb.set_trace()
                    tev = TickEvent(instrument, time, bid, ask, spread)
                    self.events_queue.put(tev)
