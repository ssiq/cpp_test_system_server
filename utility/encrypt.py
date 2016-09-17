'''
Basic module to provide keyczar based encryption/decryption.

Deficiencies include:
    * no key rotation
    * no key expiration

Author: kvamlnk
'''

# __metaclass__ = type

import os

from keyczar import keyczar
from keyczar import keyczart
from keyczar.errors import KeyczarError
import base64
from Crypto.Cipher import AES
from Crypto import Random
import json

# Note that the names used in these format strings
# should be used in your code
#
# FMT_CREATE = 'create --location=%(loc)s --purpose=crypt'
# FMT_ADDKEY = 'addkey --location=%(loc)s --status=primary'
#


# def _require_dir(loc):
#     '''Make sure that loc is a directory.
#     If it does not exist, create it.
#     '''
#     if os.path.exists(loc):
#         if not os.path.isdir(loc):
#             raise ValueError('%s must be a directory' % loc)
#     else:
#         # should we verify that containing dir is 0700?
#         os.makedirs(loc, 0755)
#
#
# def _tool(fmt, **kwds):
#     '''Package the call to keyczart.main
#     which is awkwardly setup for command-line use without
#     organizing the underlying logic for direct function calls.
#     '''
#     return keyczart.main((fmt % kwds).split())
#
#
# def _initialize(loc, **kwds):
#     '''Initialize a location
#     create it
#     add a primary key
#     '''
#     _require_dir(loc)
#     steps = [FMT_CREATE, FMT_ADDKEY]
#     for step in steps:
#         _tool(step, loc=loc, **kwds)
#
#
# class Crypter(object):
#     '''Simplify use of keyczar.Crypter class
#     '''
#     location = 'stdkeyset'
#
#     @staticmethod
#     def _read(loc):
#         return keyczar.Crypter.Read(loc)
#
#     def __init__(self, loc=None):
#         if loc is None:
#             loc = self.location
#         try:
#             self.crypt = self._read(loc)
#         except KeyczarError:
#             _initialize(loc)
#             self.crypt = self._read(loc)
#
#         print self.crypt
#
#     def encrypt(self, s):
#         return self.crypt.Encrypt(s)
#
#     def decrypt(self, s):
#         return self.crypt.Decrypt(s)

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s)-1:])]


class Crypter(object):
    def _pad_key(self, key):
        return "{: <32}".format(key).encode("utf-8")

    def __init__(self, loc=None, key=None):
        import os
        if key is not None:
            self.key = self._pad_key(key)
        else:
            loc = os.path.join(loc, '1')
            print loc
            with open(loc, 'r') as f:
                self.key = self._pad_key(json.loads(f.read())['aesKeyString'])
                print self.key

    def encrypt(self, raw):
        raw = pad(raw)
        # print AES.block_size
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


if __name__ == '__main__':
    crypter = Crypter('../keys')
    input = 'Library Reference (keep this under your pillow)'
    print len(input), input
    c = crypter.encrypt( input)
    crypter = Crypter('../keys')
    print len(c), c
    plain = crypter.decrypt( c)
    assert plain == input, ' in<%s>\nout<%s>' % (input, plain)