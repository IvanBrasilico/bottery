from unittest import mock
from bottery.views import pong, locate_next, \
    process_parameters, access_api_rules


def test_pong():
    assert pong('any_string') == 'pong'
    assert pong(1) == 'pong'
    assert pong(None) == 'pong'


rules = {'book': {'list': '/list',
                  'view': '/view/',
                  'filter': '/filter',
                  '_message': 'Enter command: '
                 }
        }
params = {'filter:2': [{'name': 'author', 'required': True},
                       {'name': 'name', 'required': True},
                       {'name': 'publisher', 'required': False}
                      ]
         }

def test_locate_next():
    assert locate_next('book', rules) == (rules['book'], 1)
    assert locate_next('book list', rules) == ('/list', 2)
    assert locate_next('book not_exist_com', rules) == ({}, 2)

def test_process_parameters():
    assert process_parameters('filter', 2, params) == (['author', 'name', 'publisher'], 2)

@mock.patch('bottery.views.urlopen')
def test_call_api(urlopen):
    urlopen.return_value.read.return_value = '{"mocked": "mocked"}'
    message = type('Message', (object,), {'text': 'book'})
    resp, hook = access_api_rules(message, rules)
    assert hook is True
    assert resp.find('Enter command:') == 0
    message.text = 'book view'
    assert access_api_rules(message, rules) == ('Enter parameters: ', True)
    message.text = 'book view corcunda'
    assert access_api_rules(message, rules) == ('mocked: mocked \n ', False)

