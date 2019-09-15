import json
from wsgiref import simple_server

import falcon


class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.')


class FlightsResource(object):

    # def __init__(self):
    # self.logger = logging.getLogger('flightsapp.' + __name__)

    def on_get(self, req, resp):
        status_invalid = req.get_param(
            'statusinvalid',default='false').lower() == 'true'
        invalid_schema = req.get_param(
            'invalidschema',default='false').lower() == 'true'
        doc = [{
            "depart": "2019-04-16T22:05:15Z",
            "arrive": "2018-12-21T07:06:13Z",
            "flight": {
                "code": "7N",
                "number": "5184"
            },
            "airline": "Pegasus Airlines",
            "isDirectFlight": True,
            "flightStatus": "DELAYED",
            "aircraft": {
                "manufacturer": "Boeing",
                "model": "488-1"
            }
        }, {
            "depart": "2019-01-06T19:23:31Z",
            "arrive": "2019-01-19T04:41:48Z",
            "flight": {
                "code": "6Y",
                "number": "46"
            },
            "airline": "CEBU Pacific Air",
            "isDirectFlight": False,
            "flightStatus": "DIVERTED",
            "aircraft": {
                "manufacturer": "Airbus",
                "model": "077-8"
            }
        }, {
            "depart": "2019-06-06T16:16:52Z",
            "arrive": "2018-12-11T21:30:44Z",
            "flight": {
                "code": "5R",
                "number": "04"
            },
            "airline": "Air Caraibes",
            "isDirectFlight": True,
            "flightStatus": "SCHEDULED",
            "aircraft": {
                "manufacturer": "Boeing",
                "model": "192-0"
            }
        }]

        if status_invalid:
            doc[0]['flightStatus']="INVALID"
        if invalid_schema:
            doc[0]['flightStatus']=0
        resp.media = doc
        resp.content_type = req.accept
        resp.status = falcon.HTTP_200


app = falcon.API(middleware=[
    RequireJSON()
])

flights = FlightsResource()
app.add_route('/flights', flights)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    print("Start serving at http://127.0.0.1:8000")
    httpd.serve_forever()
