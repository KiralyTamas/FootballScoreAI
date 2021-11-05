import http.client
import json
import logging
from json import JSONDecodeError


class EndpointCaller:
    def __init__(self, api_key, host_url, is_rapid_api=False):
        self.api_key = api_key
        self.host_url = host_url
        self.headers = {
            'x-rapidapi-host': self.host_url,
            'x-rapidapi-key': self.api_key
            }
        self.connection = http.client.HTTPSConnection(self.host_url)
        self.is_rapid_api = is_rapid_api
        self.logger = logging.getLogger(__name__)

    def call(self, endpoint):
        if self.is_rapid_api:
            endpoint = "/v2" + endpoint
        self.logger.info("Calling: {}".format(endpoint))
        try:
            self.connection.request("GET", endpoint, headers=self.headers)
            response = self.connection.getresponse()
            byte_data = response.read()
            return json.loads(byte_data.decode("utf-8"))
        except TimeoutError:
            self.logger.error("Timeout error")
            return {}
        except JSONDecodeError:
            self.logger.error("JSON decoding error")
            return {}
        except Exception:
            self.logger.error("Unknown error")
            return {}
