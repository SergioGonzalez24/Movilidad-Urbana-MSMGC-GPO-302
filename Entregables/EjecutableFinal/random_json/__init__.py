import random
import math

##-----------------------------------------------------------------------

class Generator(object):

    def __init__ (self):
        random.seed()

    def byte (self):
        return random.randint(0,0xff)

    def integer (self,signed):
        i = random.randint(0,0xffffffff)
        if signed:
            i = 0x7fffffff - i
        return i

    def _small_float (self, pos = True, maxval = None):
        go = True
        while go:
            n = self.integer(not pos)
            d = self.integer(False)
            d = 1 if d is 0 else d
            ret = float(d)/float(n)
            if maxval is None or abs(ret) < maxval:
                go = False
        return ret

    def float(self):
        base = self._small_float(pos = True, maxval = 40)
        exp = self._small_float(pos = True, maxval = 40)
        return math.pow(base,exp)

    def string(self, n = None):
        if not n:
            n = random.randint(0,200)
        s = ''.join([ chr(self.byte()) for i in range(n) ])
        return s.encode('base64').strip()

    def array (self, n, d):
        if not n:
            n = random.randint(0, 10)
        return [ self.json(d+1) for i in range(n) ]

    def obj (self, n, d=0):
        if not n:
            n = random.randint(0, 8)
        return dict([ (self.string(10),self.json(d+1)) for i in range(n) ])

    def json(self, d=0):
        b = random.randint(0,7)
        ret = None

        # Don't go more than 4 levels deep. Cut if off by
        # not allowing recursive structures at level 5.
        if d > 4 and b > 5:
            b = b % 5

        if False: pass
        elif b is 0: ret = False
        elif b is 1: ret = True
        elif b is 2: ret = None
        elif b is 3: ret = self.integer(True)
        elif b is 4: ret = self.float()
        elif b is 5: ret = self.string()
        elif b is 6: ret = self.array(None, d)
        elif b is 7: ret = self.obj(None,d)
        return ret

##-----------------------------------------------------------------------

def json ():
    g = Generator()
    return g.json()

def obj(n = None):
    g = Generator()
    return g.obj(n)

##-----------------------------------------------------------------------

if __name__ == "__main__":
    print obj(10)

