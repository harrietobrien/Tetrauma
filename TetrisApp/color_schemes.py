"""
Colors Class
--> five default schemes are class attributes
   • • • each a list of seven hues
--> takes new schemes and checks validity
"""
from defaults import defaults


class ColorSchemes:
    defaults = defaults

    def __init__(self, selection=0, newScheme=None, title="NEW SCHEME"):
        self.selection = selection
        if newScheme and self.isScheme(newScheme):
            self.addScheme(title, newScheme)
            self.selection = title
        else:
            assert(not newScheme)
            self.currentScheme = defaults[self.selection]

    def getScheme(self):
        return self.getSchemeDict(self.selection)

    @staticmethod
    def isScheme(scheme):
        # confirm every hue = hex str
        if isinstance(scheme, list) or \
                isinstance(scheme, tuple) \
                and len(scheme) == 7:
            return True

    @staticmethod
    def addScheme(schemeName, schemeList):
        if schemeList:
            defaults[schemeName] = schemeList

    @staticmethod
    def hexToRGB(hueHex):
        hh = hueHex.lstrip('#')
        return tuple(int(hh[i:i + 2], 16)
                     for i in (0, 2, 4))

    @staticmethod
    def RGBToHex(RGBTuple):
        RGBList = list(map(lambda i: int(i + 0.5), RGBTuple))
        r = RGBList[0]
        g = RGBList[1]
        b = RGBList[2]
        toJoin = ['#', '{:02x}{:02x}{:02x}'.format(r, g, b)]
        return ''.join(toJoin)

    def getTint(self, hueHex, stepPercent=10):
        # convert to hex to RGB
        stepPercent /= 100
        RGB = self.hexToRGB(hueHex)
        # recalculate RGB; round
        newRGB = map(lambda hh: hh + ((255 - hh) * stepPercent), RGB)
        tint = self.RGBToHex(newRGB)
        return tint

    def getShade(self, hueHex, stepPercent=10):
        # convert to hex to RGB
        RGB = self.hexToRGB(hueHex)
        # recalculate RGB; round
        stepPercent = (100 - stepPercent) / 100
        newRGB = map(lambda hh: hh * stepPercent, RGB)
        # convert back to hex
        shade = self.RGBToHex(newRGB)
        return shade

    '''
    --> makes pieces instances of each piece
    '''

    def getSchemeDict(self):
        pieces = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        schemeDict = dict()
        keys = ('hue', 'tint', 'shade')
        for i in range(len(pieces)):
            piece = pieces[i]
            print(self.selection)
            print(defaults[self.selection])
            hue = defaults[self.selection][i]
            print('hue', hue)
            tint = self.getTint(hue)
            print('tint', tint)
            shade = self.getShade(hue)
            print('shade', shade)
            vals = (hue, tint, shade)
            colors = dict(zip(keys, vals))
            schemeDict[piece] = colors
        return schemeDict


# schemes = ColorSchemes()
# schemes.getSchemeDict(1)
