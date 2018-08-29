# -*- coding: utf-8 -*-


'''
created on 2018-01-16

@author: zzz
'''


from ctypes import *


class Gts(object):

    def __init__(self):
        self.dll = windll.LoadLibrary('gts.dll')

    def open(self, actid):
        self.dll.GT_Open.argtypes = [c_short, c_short, c_short]
        self.dll.GT_Open.restype = c_short
        return self.dll.GT_Open(actid, 0, 1)

    def close(self, actid):
        self.dll.GT_Open.argtypes = None
        self.dll.GT_Close.restype = c_short
        return self.dll.GT_Close(actid)

    def load_params(self, actid, params):
        pass

    def get_version(self):
        self.dll.GT_GetVersion.argtypes = [c_short, POINTER(c_char)]
        self.dll.GT_GetVersion.restype = c_short

        buffer = create_string_buffer(200)
        pbuffer = addressof(buffer)

        p = cast(pbuffer, POINTER(c_char))

        ret = self.dll.GT_GetVersion(0, p)

        print(sizeof(buffer), repr(buffer.value))
        return ret

    def get_dll_version(self):
        self.dll.GT_GetDllVersion.argtypes = [POINTER(c_char)]
        self.dll.GT_GetDllVersion.restype = c_short

        buffer = create_string_buffer(200)
        pbuffer = addressof(buffer)

        p = cast(pbuffer, POINTER(c_char))

        ret = self.dll.GT_GetDllVersion(p)

        print(sizeof(buffer), repr(buffer.value))
        return ret


if __name__ == '__main__':
    #g = Gts()
    #print(g.close(0))
    #print(g.get_dll_version())
    #print (g.open(1))
    pass