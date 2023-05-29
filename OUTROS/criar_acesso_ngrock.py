# -*- coding: utf-8 -*- 

import sys
import time
import traceback
import requests
from requests.exceptions import ConnectionError
from django.conf import settings


try:
    from sh import sudo, nohup, killall
    from io import StringIO
except:
    pass


class Ngrok:
    as_root = False if sys.platform == 'darwin' else True
    sudo_ = "%s/scripts/sudo.sh" % getattr(settings, "ROOT_PATH", '/usr/local/sgp')
    ngrok_ = "%s/doc/ngrok/ngrok_%s" % (getattr(settings, "ROOT_PATH", '/usr/local/sgp'), \
        'osx' if sys.platform == 'darwin' else 'linux')
    timeout = 60
    
    @staticmethod
    def get_public_url(**kwargs):
        timeout = kwargs.get('timeout', Ngrok.timeout)
        
        j = 0
        while j < timeout:
            try:
                response = requests.get('http://127.0.0.1:4040/api/tunnels')

                if response.status_code == 200:
                    return response.json()['tunnels'][0]['public_url']
            except ConnectionError:
                pass
            except:
                if kwargs.get('debug', None):
                    traceback.print_exc()

            time.sleep(1)
            j += 1

    @staticmethod
    def start(protocol="http", port="8000", **kwargs):
        public_url = Ngrok.get_public_url(timeout=2.5, 
                                          debug=kwargs.get('debug', None))
        authtoken = kwargs.get('authtoken', settings.NGROK_AUTHTOKEN)

        if not public_url:
            try:
                if Ngrok.as_root:
                    sudo(Ngrok.sudo_, 'chmod', "+x", Ngrok.ngrok_)
                    sudo(Ngrok.sudo_, Ngrok.ngrok_, "config", "add-authtoken", authtoken)
                    sudo(Ngrok.sudo_, Ngrok.ngrok_, protocol, port, _bg=True)
                else:
                    nohup(Ngrok.ngrok_, "config", "add-authtoken", authtoken)
                    nohup(Ngrok.ngrok_, protocol, port, _bg=True)

                public_url = Ngrok.get_public_url()
            except:
                if kwargs.get('debug', None):
                    traceback.print_exc()

        return public_url

    @staticmethod
    def stop(**kwargs):
        try:
            if Ngrok.as_root:
                sudo(Ngrok.sudo_, 'killall', Ngrok.ngrok_)
            else:
                killall("ngrok_%s" % 'osx' if sys.platform == 'darwin' else 'linux')
        except:
            if kwargs.get('debug', None):
                    traceback.print_exc()
