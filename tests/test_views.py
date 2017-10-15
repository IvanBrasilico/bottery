from bottery.views import pong, locate_next, \
    process_parameters, access_api_rules


def test_pong():
    assert pong('any_string') == 'pong'
    assert pong(1) == 'pong'
    assert pong(None) == 'pong'


rules = {'book': {'list': '/list',
                 'show': '/show/',
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

def test_access_api_rules():
    pass
    