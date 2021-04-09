import requests

userdata = {
    'emailaddress': 'x',
    'screenname': 'x',
    'countrycode': 'x',
    'firstName': 'x',
    'lastName': 'x',
    'balance': '0.0',
    'etransid': '###',
    'transid': '###',
    'datetime': '###',
    'euid': 'x',
    'uid': 'x',
}

# class Player:
#
#     id = 'yaoza',  # assigned by licensee, should be euid
#     update = False,
#     firstName = 'firstName',  # assigned
#     lastName = 'lastName',  # assigned
#     nickname = 'nickname',  # assigned
#     country = 'DE',  # assigned
#     language = 'fr',  # assigned
#     currency = 'CNY',  # assigned
#     session':{
#         'id': '111ssss3333rrrrr45555',  # assigned by licensee
#         'ip': '192.168.0.1'  # assigned
#     }
#

UA_dataStruct = {
    'uuid': 'random',  # assigned, should be uid
    'player': {
        'balance': '0.0',
        'id': 'yaoza',  # assigned by licensee, should be euid
        'update': False,
        'firstName': 'firstName',  # assigned
        'lastName': 'lastName',  # assigned
        'nickname': 'nickname',  # assigned
        'country': 'DE',  # assigned
        'language': 'fr',  # assigned
        'currency': 'CNY',  # assigned
        'session': {
            'id': '111ssss3333rrrrr45555',  # assigned by licensee
            'ip': '192.168.0.1'  # assigned
        }
    },
    'config': {
        'brand': {
            'skin': '1'
        },
        'game': {
            'category': 'roulette',
            'interface': 'view1'

        },
        'channel': {
            'wrapped': False,
            'mobile': False
        },
        'urls': {
            'cashier': 'http://www.chs.ee',  # assigned by licensee
            'responsibleGaming': 'http://www.RGam.ee',  # assigned by licensee
            'lobby': 'http://www.lobb.ee',  # assigned by licensee
            'sessionTimeout': 'http://www.sesstm.ee'  # assigned by licensee
        },
        'freeGames': False
    }
}


class Session:
    UA_payload = UA_dataStruct
    link = ''
    url = 'https://diyft4.uat1.evo-test.com/api/ecashier'
    ecID = 'diyft40000000001test123'

    def get_link(self):
        x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=self.UA_payload)
        link = 'https://diyft4.uat1.evo-test.com' + x.json()['entry']

        return link
