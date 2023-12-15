

class GBTEDGE(object):
    def __init__(self, cat='GBTEDGE.cat'):
        self.cat = cat
        self.gals = {}
        lines = open(cat).readlines()
        for line in lines:
            if line[0] == '#': continue
            words = line.split()
            if words[0] == 'NAME': continue      # old style non-commented
            # NGC0001       J2000  00:07:15.84  +27:42:29.7   113571.8579  VRAD-LSR  0.0  0.01496  10.89   +0.71  4485.7      0
            self.gals[words[0]] = [words[2],words[3],words[10]]    # store ra,dec,vlsr
        print("Found %d galaxies in %s" % (len(self.gals), cat))
    def entry(self, gal):
        if gal in self.gals:
            return self.gals[gal]
        else:
            return None
   
