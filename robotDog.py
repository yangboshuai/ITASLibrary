from robot.api import TestSuite

suite = TestSuite('Login')
suite.resource.imports.library('ITASLibrary')

test = suite.tests.create('LoginTest', tags=['smoke'])
print type(test)
test.keywords.create('SetBaseUrl', args=[ 'http://192.168.168.151:8080'], type='setup')
loginResp=test.keywords.create('login', args=[ 'REGSUP201504','1234a*'])
print type(loginResp)




result = suite.run(critical='smoke', output='skynet.xml')

