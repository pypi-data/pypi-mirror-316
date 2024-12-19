# -*- coding:utf-8 -*-
import requests
import logging
import urllib3


class Http:

    def __init__(self, timeout=60):
        urllib3.disable_warnings()
        self.timeout = timeout
        requests.session()

    def get(self, url="", params=None, headers=None):
        logging.info(f"Method=GET, URL={url}")
        logging.info(f"Headers={headers}")
        logging.info(f"Params={params}")
        resp = requests.get(url=url, params=params, headers=headers, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        logging.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def post(self, url="", data=None, params=None, headers=None):
        logging.info(f"Method=POST, Url={url}")
        logging.info(f"Headers={headers}")
        logging.info(f"Params={params}")
        logging.info(f"Data={data}")
        resp = requests.post(url=url, data=data, params=params, headers=headers, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        logging.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def put(self, url="", params=None, data=None, headers=None):
        logging.info(f"Method=PUT, Url={url}")
        logging.info(f"Headers={headers}")
        logging.info(f"Params={params}")
        logging.info(f"Data={data}")
        resp = requests.put(url=url, params=None, data=data, headers=headers, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        logging.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def delete(self, url="", params=None, data=None, headers=None):
        logging.info(f"Method=DELETE, Url={url}")
        logging.info(f"Headers={headers}")
        logging.info(f"params={params}")
        logging.info(f"Data={data}")
        resp = requests.delete(url=url, params=params, data=data, headers=headers, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        logging.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def patch(self, url, params=None, data=None, headers=None):
        logging.info(f"Method=PATCH, Url={url}")
        logging.info(f"Headers={headers}")
        logging.info(f"params={params}")
        logging.info(f"Data={data}")
        resp = requests.patch(url=url, data=data, headers=headers, timeout=self.timeout, verify=False)
        time_consuming, time_total = self.response_time(resp)
        logging.info(f"Response:status_code={resp.status_code}, text={resp.text}, time_consuming={time_consuming}, time_total={time_total}")
        return resp

    def response_time(self, response):
        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()
        return time_consuming, time_total
