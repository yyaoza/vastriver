import requests
import xml.etree.ElementTree as ET

# from flask import request

userdataStruct = {
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

UA_dataStruct = {
    'uuid': 'random',  # assigned, should be uid
    'transaction': {
        'etransid': '###',
        'transid': '###',
        'datetime': '###',
    },
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
            'cashier': 'http://www.RGam.ee',  # assigned by licensee
            'responsibleGaming': 'http://www.RGam.ee',  # assigned by licensee
            'lobby': 'http://www.lobb.ee',  # assigned by licensee
            'sessionTimeout': 'http://www.sesstm.ee'  # assigned by licensee
        },
        'freeGames': False
    }
}


class Session:
    UA_payload = UA_dataStruct
    userdata = userdataStruct
    link = ''
    # url = 'https://diyft4.uat1.evo-test.com/api/ecashier'
    url = 'https://diyft4.uat1.evo-test.com/'
    cashier_payload = {
        'cCode': 'xxx',
        'euID': 'yaoza',
        'ecID': 'diyft40000000001test123',
        'eTransID': 'fake_eTransID',
        'output': '1'
    }

    def __init__(self, hostname):
        self.UA_payload['config']['urls']['cashier'] = hostname
        self.get_user_info()

    def casino_cmd(self, cmd, amount=0):
        if cmd == 'GUI':
            self.cashier_payload.update({'cCode': cmd})
        else:
            self.cashier_payload.update({'cCode': cmd,
                                         'amount': amount,
                                         })

        x = requests.get(self.url + 'api/ecashier', params=self.cashier_payload)
        return ET.fromstring(x.text)

    def set_lang_game(self, form):
        self.UA_payload['player']['language'] = form.language.data
        self.UA_payload['config']['game']['category'] = form.game.data

    def get_user_info(self):
        gui = self.casino_cmd('GUI')
        self.UA_payload['player']['firstName'] = gui[1].text
        self.UA_payload['player']['lastName'] = gui[2].text
        self.UA_payload['player']['nickname'] = gui[3].text
        self.UA_payload['player']['country'] = gui[4].text
        self.UA_payload['player']['update'] = False
        self.UA_payload['uuid'] = gui[5].text
        self.UA_payload['player']['id'] = gui[6].text
        rwa = self.casino_cmd('RWA')
        self.UA_payload['player']['balance'] = rwa[3].text

    def update_user_info(self, form):
        self.UA_payload['player']['firstName'] = form.firstName.data
        self.UA_payload['player']['lastName'] = form.lastName.data
        self.UA_payload['player']['nickname'] = form.nickName.data
        self.UA_payload['player']['country'] = form.country.data
        self.UA_payload['player']['language'] = form.language.data
        self.UA_payload['player']['update'] = True
        self.UA_payload['config']['game']['category'] = form.game.data
        print("*Writing payload", self.UA_payload, sep="---->")
        self.get_link()

    def ft_add(self, amount):
        ecr = self.casino_cmd('ECR', amount)
        self.UA_payload['player']['balance'] = ecr[0].text
        self.UA_payload['transaction']['etransid'] = ecr[1].text
        self.UA_payload['transaction']['transid'] = ecr[2].text
        self.UA_payload['transaction']['datetime'] = ecr[3].text
        self.userdata.update({
            'balance': ecr[0].text,
            'etransid': ecr[1].text,
            'transid': ecr[2].text,
            'datetime': ecr[3].text
        })

    def ft_subtract(self, amount):
        ecr = self.casino_cmd('EDB', amount)
        self.UA_payload['player']['balance'] = ecr[0].text
        self.UA_payload['transaction']['etransid'] = ecr[1].text
        self.UA_payload['transaction']['transid'] = ecr[2].text
        self.UA_payload['transaction']['datetime'] = ecr[3].text
        self.userdata.update({
            'balance': ecr[0].text,
            'etransid': ecr[1].text,
            'transid': ecr[2].text,
            'datetime': ecr[3].text
        })

    def get_link(self):
        x = requests.post(self.url + 'ua/v1/diyft40000000001/test123', json=self.UA_payload)
        link = 'https://diyft4.uat1.evo-test.com' + x.json()['entry']
        print(link)
        return link
