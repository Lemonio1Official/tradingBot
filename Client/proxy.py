from env import PROXY
import requests as requests_

proxies = None
class requests:
    Response = requests_.Response

if PROXY:
    proxy_url = f'http://{PROXY}'

    proxies = {
        'http': proxy_url,
        'https': proxy_url,
    }

    requests.get = lambda url, params = None, data = None, headers = None: requests_.get(url, data=data, params=params, headers=headers, proxies=proxies)
    requests.post = lambda url, params = None, data = None, headers = None: requests_.post(url, data=data, params=params, headers=headers, proxies=proxies)
    requests.put = lambda url, params = None, data = None, headers = None: requests_.put(url, data=data, params=params, headers=headers, proxies=proxies)
    requests.delete = lambda url, params = None, data = None, headers = None: requests_.delete(url, data=data, params=params, headers=headers, proxies=proxies)

