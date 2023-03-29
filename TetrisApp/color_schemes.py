"""
Colors Class
--> five default schemes are class attributes
   • • • each a list of seven hues
--> takes new schemes and checks validity
"""


class ColorSchemes(object):
    defaults = dict()
    defaults[1] = (
        '#EF233C',  # imperial red
        '#F8A312',  # orange web
        '#FEE440',  # minion yellow
        '#40C9A2',  # caribbean green
        '#36B6D3',  # pacific blue
        '#2667FF',  # ultramarine blue
        '#3423A6'  # blue pantone
    )
    defaults[2] = (
        '#F45866',  # fiery rose
        '#F79D84',  # vivid tangerine
        '#F8C162',  # maximum yellow red
        '#D7F171',  # mindaro
        '#A9FOD1',  # magic mint
        '#8AC4FF',  # maya blue
        '#ADBDFF'  # maximum blue purple
    )
    defaults[3] = (
        '#D72483',  # barbie pink
        '#FF595E',  # red salsa
        '#FF9E1F',  # orange peel
        '#FFCA3A',  # sun glow
        '#E0FF4F',  # arctic lime
        '#59CD90',  # emerald
        '#3185FC'  # azure
    )
    defaults[4] = (
        '#D81159',  # ruby
        '#FC440F',  # coquelicot
        '#FF9F1C',  # orange peel
        '#C6F91F',  # electric lime
        '#2EC4B6',  # tiffany blue
        '#008BF8',  # bleu de france
        '#623CEA'  # majorelle Blue
    )
    defaults[5] = (
        '#CC0085',  # medium violet red
        '#EA638C',  # blush
        '#F79D84',  # vivid tangerine
        '#EFCA08',  # yellow munsell
        '#6CC551',  # mantis
        '#41B1C8',  # pacific blue
        '#5E2BFF'  # han purple
    )

    def __init__(self, n=7, newScheme=1, title="NEW SCHEME"):
        self.currentScheme = ColorSchemes.defaults[1]
        self.n = n  # number of pieces
        if self.isScheme(newScheme):
            self.addScheme(title, newScheme)
        else:
            if newScheme is None:
                # get random scheme
                self.currentScheme = ColorSchemes.defaults[1]
        # self.length = len(self.scheme)

    def isScheme(self, scheme):
        # confirm every hue = hex str
        if isinstance(scheme, list) or \
                isinstance(scheme, tuple) \
                and len(scheme) == self.n:
            return True

    @staticmethod
    def addScheme(schemeName, schemeList):
        if schemeList:
            ColorSchemes.defaults[schemeName] = schemeList

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
        toJoin = ['#', '{:X}{:X}{:X}'.format(r, g, b)]
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
    def getSchemeDict(self, currScheme):
        pieces = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        schemeDict = dict()
        keys = ('hue', 'tint', 'shade')
        for i in range(len(pieces)):
            piece = pieces[i]
            hue = ColorSchemes.defaults[currScheme][i]
            print('hue', hue)
            tint = self.getTint(hue)
            print('tint', tint)
            shade = self.getShade(hue)
            print('shade', shade)
            vals = (hue, tint, shade)
            colors = dict(zip(keys, vals))
            schemeDict[piece] = colors
        return schemeDict

    '''
    colors = dict()
    for i in range(len(dir(ColorSchemes))):
        currScheme = dir(ColorSchemes)[i]
        if not currScheme.startswith('__') and not \
                callable(getattr(ColorSchemes, currScheme)):
            pass
    '''


schemes = ColorSchemes()
schemes.getSchemeDict(1)

