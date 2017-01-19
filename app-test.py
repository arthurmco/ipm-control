
import os
import app
import unittest
import tempfile

import json

#from models.Database import Database, installDatabase

class IPMTestCase(unittest.TestCase):
    __testid=-1
    
    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def do_login(self, user, pwd):
        return self.app.post('/login', data=dict(
            username=user, password=pwd), follow_redirects=True)

    def do_logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login(self):
        rv = self.do_login('tester', 'nottester')
        assert b'Logout' not in rv.data
        rv = self.do_login('nottester', 'tester')
        assert b'Logout' not in rv.data
        rv = self.do_login('tester', 'tester')
        assert b'Logout' in rv.data

    def test_user_get_without_permission(self):
        rv = self.app.get('/api/client/1')
        assert rv.status_code == 403
        
    def test_client_add(self):
        rv = self.do_login('tester', 'tester')
        assert rv.status_code == 200

        rv = self.app.get('/api/client/add?name=TestCaseRunning')
        assert rv.status_code == 200
        assert b'TestCaseRunning' in rv.data
        cobj = json.loads(rv.data)
        IPMTestCase.__testid = int(cobj['id'])

    def test_client_get(self):
        rv = self.do_login('tester', 'tester')
        assert rv.status_code == 200

        rv = self.app.get('/api/client/'+str(IPMTestCase.__testid))
        assert rv.status_code == 200

        assert b'TestCaseRunning' in rv.data

    def test_client_remove(self):
        rv = self.do_login('tester', 'tester')
        assert rv.status_code == 200

        rv = self.app.get('/api/client/'+str(IPMTestCase.__testid)+'/remove')
        assert rv.status_code == 200

        rv = self.app.get('/api/client/'+str(IPMTestCase.__testid))
        assert b'{}' in rv.data

        __testid=-1
        
        

if __name__ == '__main__':
    unittest.main()
