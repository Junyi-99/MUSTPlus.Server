import requests
import json


# Get Hash
r = requests.get(url='http://mp.junyi.pw:8000/hash')
pkey = r.text
assert pkey == r'{"code": 0, "msg": "OK", "key": "-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAr7vcGPzbCVDGUdhf7sh7jpsEG7FTbSkPpkuWqjCyB8CMb0PjiTVx\nUuxOco4zC5fDt/4kE26JZsyCfVw7quEZhEbh2aGcG5kV2j4klDj9UHVYA9OQlCuE\nXXpYeF8OOWX96HlvpsRYVv7kJZ04VjrVXRT74EVpCoPlJEVR/vf0VkI6Szdfedb2\nzZlL6xms0Vc8AqbyCy9l/E5W7PhJiwaWPKuWLKFhoNwqbOx9X3tBEWRudfAOxomS\nBBblAe2Td1V1qYwsgcfBEkD+8BvtvRNFnqoB05dZZgHsRxFm2hi9K7jkQQQj0ZSm\nISErMco1P+x59LZbKnIXhcybp/DfZl34xQIDAQAB\n-----END RSA PUBLIC KEY-----\n"}'

