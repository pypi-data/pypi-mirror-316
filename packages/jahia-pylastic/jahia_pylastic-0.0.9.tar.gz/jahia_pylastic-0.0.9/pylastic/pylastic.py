#!/usr/bin/env python3

import requests
import json
import logging

requests.packages.urllib3.disable_warnings()

class Jelastic:
    """Instanciate a connexion to Jelastic through is API
       :param hostname: the endpoint to you Jelastic cluster
       :param login: the login of your user
       :param password: the user's password
       :type hostname: string
       :type login: string
       :type password: string

       :Example:
           >>> jel = Jelastic("my.jelastic.com",
                              "myuser",
                              "mypass")
           >>> jel.signIn
    """
    def __init__(self, hostname=None,
                 login=None, password=None,
                 session=None, token=None):
        self.hostname = "https://" + hostname
        self.login = login
        self.password = password
        self.session = session
        if token and not session:
            self.token = token
            self.session = token
        else:
            self.token = token
        self.uid = None

        self.s = requests.Session()
        self.s.headers = {'User-Agent': 'pylastic/0.1'}
        self.s.verify = False

        try:
            self.logging = logging.getLogger('pylastic')
        except:
            self.logging = logging

        self.logging.debug("A new Jelastic object is instancied.")

    def isSessionValid(self):
        """Checks if the session is valid and the user is signed in"""
        url = self.hostname + "/1.0/users/authentication/rest/checksign"
        resp = self.s.get(url, params={'session': self.session})
        self.logging.debug("login: {}".format(self.login))
        if 'accessType' in json.loads(resp.text).keys():
            self.logging.debug("Invalid session, you need to sign in.")
            return True
        else:
            self.logging.debug("The session is valid, user signed in.")
            return False

    def signIn(self):
        """Signin to the Jelastic API"""
        if self.isSessionValid():
            return self.session

        url = self.hostname + "/1.0/users/authentication/rest/signin"
        resp = self.s.post(url, data={'login': self.login,
                                      'password': self.password})
        self.logging.debug("login: {}".format(self.login))
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot authenticate. Code: {}"
                               .format(str(resp.text)))
            return resp
        else:
            self.logging.debug("Authentication successful.")
            self.session = json.loads(resp.text)['session']
            self.usersAccountGetUserInfo()
            return self.session

    def signOut(self):
        """Sign out to the Jelastic API"""
        url = self.hostname + "/1.0/users/authentication/rest/signout"
        resp = self.s.post(url, data={'session': self.session})
        self.logging.debug("logout: {}".format(self.login))
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot sign out. Code: {}"
                               .format(str(resp.text)))
            return resp
        else:
            self.logging.debug("Sign out successful.")
            return True

    def getSessionAttribute(self):
        self.logging.info("\n\thostname({})\n\tlogin({})\n\tpassword({})\n\tsession({})\n\ttoken({})\n\tuid({})"
                          .format(self.hostname,
                                  self.login,
                                  self.password,
                                  self.session,
                                  self.token,
                                  self.uid))

    # Development Scripting
    def devScriptEval(self, urlpackage=None, shortdomain=None,
                      region=None, settings=None):
        url = self.hostname + "/1.0/development/scripting/rest/eval"
        payload = {'session': self.session,
                   'appid': 'appstore',
                   'script': 'InstallApp',
                   'manifest': urlpackage,
                   'settings': json.dumps(settings)
                   }
        package = requests.get(urlpackage)
        if region:
            self.logging.debug("You specified {} region".format(region))
            payload['region'] = region
        if package.text.find('type: update') >= 0:
            self.logging.debug("{} is an update package".format(urlpackage))
            envinfo = self.envControlGetEnvInfo(shortdomain)
            payload['targetAppid'] = envinfo['env']['appid']
        else:
            self.logging.debug("{} is an install package".format(urlpackage))
            payload['shortdomain'] = shortdomain
        resp = self.s.post(url, data=payload)
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            self.logging.debug(resp.text)
        return resp

    # Environment Group
    def envGroupGetGroups(self, envname):
        url = self.hostname + "/1.0/environment/group/rest/getgroups"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    # Environment Tracking
    def envControlGetCurrentActions(self):
        url = self.hostname + "/1.0/environment/tracking/rest/getcurrentactions"
        resp = self.s.post(url, data={'session': self.session})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    # Environment Control
    def SetCloudletsCountByGroup(self, envname, count, nodegroup, fixed=1):
        url = self.hostname + "/1.0/environment/control/rest/setcloudletscountbygroup"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname,
                                      'count': count,
                                      'nodeGroup': nodegroup,
                                      'flexibleCloudlets': count,
                                      'fixedCloudlets': fixed})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    def envControlGetNodeGroups(self, envname):
        url = self.hostname + "/1.0/environment/control/rest/getnodegroups"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    def envControlGetContainerNodeTags(self, envname, nodeid):
        url = self.hostname + "/1.0/environment/control/rest/getcontainernodetags"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname,
                                      'nodeId': nodeid})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    def envControlAddContainerEnvVars(self, envname, nodegroup, envvars={}):
        url = self.hostname + "/1.0/environment/control/rest/addcontainerenvvars"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname,
                                      'nodeGroup': nodegroup,
                                      'vars': json.dumps(envvars)})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    def envControlGetContainerEnvVars(self, envname, nodeid):
        url = self.hostname + "/1.0/environment/control/rest/getcontainerenvvars"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname,
                                      'nodeId': nodeid})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    def envControlGetEnvInfo(self, envname):
        url = self.hostname + "/1.0/environment/control/rest/getenvinfo"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    def envControlGetEnvs(self):
        url = self.hostname + "/1.0/environment/control/rest/getenvs"
        resp = self.s.post(url, data={'session': self.session})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    def envControlStartEnv(self, envname):
        url = self.hostname + "/1.0/environment/control/rest/startenv"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    def envControlStopEnv(self, envname):
        url = self.hostname + "/1.0/environment/control/rest/stopenv"
        resp = self.s.post(url, data={'session': self.session,
                                      'envName': envname})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)

    # System
    def sysAdminGetUsersByStatus(self, status='0'):
        """Gets all users filtered by status. Gets "ENABLED" users by default."""
        url = self.hostname + "/1.0/system/admin/rest/getusersbystatus"
        resp = self.s.get(url, params={'session': self.session,
                                       'status': status})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot retrieve list of users. Code:"
                               + str(resp.text))
        else:
            return json.loads(resp.text)

    def sysAdminSignAsUser(self, usermail, n=10):
        url = self.hostname + "/1.0/system/admin/rest/signinasuser"
        resp = self.s.get(url, params={'session': self.session,
                                       'login': usermail,
                                       'appid': 'cluster'})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot sign in as user {}: Code: {}"
                               .format(usermail, str(resp.text)))
        else:
            if 'session' not in json.loads(resp.text) and n > 0:
                print(resp.text)
                self.logging.warning("\nsession: {}\ntoken: {}"
                                     .format(self.session, self.token))
                self.logging.warning("Auth problem, retrying {} time..."
                                     .format(n))
                self.sysAdminSignAsUser(usermail, n=n-1)
            return json.loads(resp.text)['session']

    # Users
    def usersAuthGetSessions(self):
        url = self.hostname + "/1.0/users/authentication/rest/getsessions"
        resp = self.s.get(url, params={'session': self.session,
                                       'appid': 'cluster'})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot retrieve current user sessions. Code:"
                               + str(resp.text))
        else:
            return json.loads(resp.text)

    def usersAccountGetUserInfo(self):
        url = self.hostname + "/1.0/users/account/rest/getuserinfo"
        resp = self.s.get(url, params={'session': self.session,
                                       'appid': 'cluster'})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot retrieve current user info. Code:"
                               + str(resp.text))
        else:
            self.login = json.loads(resp.text)['email']
            self.uid = json.loads(resp.text)['uid']
            return json.loads(resp.text)

    def usersAccountDeleteSSHKey(self, key_id, isPrivate=False):
        url = self.hostname + "/1.0/users/account/rest/deletesshkey"
        resp = self.s.get(url, params={'session': self.session,
                                       'appid': 'cluster',
                                       'id': key_id})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot delete ssh keys. Code:"
                               + str(resp.text))
        else:
            return json.loads(resp.text)

    def usersAccountGetSSHKey(self, isPrivate=False):
        url = self.hostname + "/1.0/users/account/rest/getsshkeys"
        resp = self.s.get(url, params={'session': self.session,
                                       'appid': 'cluster'})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot get ssh keys. Code:"
                               + str(resp.text))
        else:
            return json.loads(resp.text)

    def usersAccountAddSSHKey(self, keyTitle, sshKey, isPrivate=False):
        url = self.hostname + "/1.0/users/account/rest/addsshkey"
        resp = self.s.get(url, params={'session': self.session,
                                       'appid': 'cluster',
                                       'title': keyTitle,
                                       'sshKey': sshKey})
        if json.loads(resp.text)['result'] == 6001:
            self.logging.info("This key is already there")
        elif json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot push the public key. Code:"
                               + str(resp.text))
        elif json.loads(resp.text)['result'] == 6002:
            self.logging.error("This key is already there but has a wrong value")
        else:
            return json.loads(resp.text)

    def usersAuthSigninByToken(self, n=10):
        url = self.hostname + "/1.0/users/authentication/rest/signinbytoken"
        resp = self.s.get(url, params={'token': self.token,
                                       'session': self.token,
                                       'userHeaders': 'None'})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Cannot authenticate. Code: {}"
                               .format(resp.text))
        else:
            if 'session' not in json.loads(resp.text) and n > 0:
                print(resp.text)
                self.logging.warning("Auth problem, retrying {} time..."
                                     .format(n))
                self.usersAuthSigninByToken(n=n-1)
            self.logging.info("Token authentication successful.")
            self.session = json.loads(resp.text)['session']
            self.usersAccountGetUserInfo()
            return json.loads(resp.text)

    # Administration
    def getOOMKilledProcesses(self, alerts_filter):
        url = self.hostname + "/1.0/administration/cluster/rest/getoomkilledprocesses"
        resp = self.s.get(url, params={'session': self.session,
                                       'appid': 'cluster',
                                       'search': alerts_filter})
        if json.loads(resp.text)['result'] != 0:
            self.logging.error("Something is wrong. Code: {}"
                               .format(str(resp.text)))
        else:
            return json.loads(resp.text)
