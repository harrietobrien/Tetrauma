from color_schemes import ColorSchemes

"""
User can redefine Tetromino color settings 
--> decided to create classes for each piece AOT type aliases
--> allows addition of getter/setter functions for styling

[1] I -->   #36B6D3 (SCHEME 1 - pacific blue)
[2] J -->   #2667FF (SCHEME 1 - ultramarine blue)
[3] L -->   #F8A312 (SCHEME 1 - orange web)
[4] O -->   #FEE440 (SCHEME 1 - minion yellow)
[5] S -->   #40C9A2 (SCHEME 1 - caribbean green)
[6] T -->   #3423A6 (SCHEME 1 - blue pantone)
[7] Z -->   #EF233C (SCHEME 1 - imperial red)
"""


class Tetromino(object):
    colors = None

    def __init__(self, defaultNumber=0):
        self.tetrisStructs = self.updateData()
        scheme = ColorSchemes(selection=defaultNumber).getSchemeDict()
        Tetromino.colors = scheme
        self.pieces = self.getPieces()
        # print('currentScheme\t', self.pieceColors)
        # print('Tetromino.colors\t', Tetromino.colors)
        # print('self.pieces\t', len(self.pieces))

    @staticmethod
    def updateData() -> list:
        """
        :rtype: list(objects)
        :return: list of piece instances
        """
        tetros = list()

        class Ipiece:
            def __init__(self):
                self.hue: str = None
                self.tint: str = None
                self.shade: str = None

            def setColor(self, newColor):
                self.hue = newColor
                self.tint: str = \
                    Tetromino.colors[self.hue]
                self.shade: str = \
                    Tetromino.colors[self.hue]

            def getCellColors(self) -> tuple:
                return self.hue, self.tint, self.shade

            @staticmethod
            def getPiece() -> list[list[bool]]:
                return [[True for _ in range(4)]]

            @staticmethod
            def getPieceType() -> str:
                return "I"

            def __eq__(self, other):
                if isinstance(other, Ipiece):
                    return True
                elif isinstance(other, str):
                    if other == 'I':
                        return True
                elif isinstance(other, list):
                    return other == self.getPiece()
                else:
                    print('NotImplemented')

        ip = Ipiece()
        tetros.append(ip)

        class Jpiece:
            def __init__(self):
                self.hue: str = None
                self.tint: str = None
                self.shade: str = None

            def setColor(self, newColor):
                self.hue = newColor
                self.tint: str = \
                    Tetromino.colors.getTint(self.hue)
                self.shade: str = \
                    Tetromino.colors.getShade(self.hue)

            def getCellColors(self) -> tuple:
                return self.hue, self.tint, self.shade

            @staticmethod
            def getPiece() -> list[list[bool]]:
                return [[True, False, False],
                        [True, True, True]]

            @staticmethod
            def getPieceType() -> str:
                return "J"

            def __eq__(self, other):
                if isinstance(other, Jpiece):
                    return True
                elif isinstance(other, str):
                    if other == 'J':
                        return True
                elif isinstance(other, list):
                    return other == self.getPiece()
                else:
                    print('NotImplemented')

        jp = Jpiece()
        tetros.append(jp)

        class Lpiece:
            def __init__(self):
                self.hue: str = None
                self.tint: str = None
                self.shade: str = None

            def setColor(self, newColor):
                self.hue = newColor
                self.tint: str = \
                    Tetromino.colors.getTint(self.hue)
                self.shade: str = \
                    Tetromino.colors.getShade(self.hue)

            def getCellColors(self) -> tuple:
                return self.hue, self.tint, self.shade

            @staticmethod
            def getPiece() -> list[list[bool]]:
                return [[False, False, True],
                        [True, True, True]]

            @staticmethod
            def getPieceType() -> str:
                return "L"

            def __eq__(self, other):
                if isinstance(other, Lpiece):
                    return True
                elif isinstance(other, str):
                    if other == 'L':
                        return True
                elif isinstance(other, list):
                    return other == self.getPiece()
                else:
                    print('NotImplemented')

        lp = Lpiece()
        tetros.append(lp)

        class Opiece:
            def __init__(self):
                self.hue: str = None
                self.tint: str = None
                self.shade: str = None

            def setColor(self, newColor):
                self.hue = newColor
                self.tint: str = \
                    Tetromino.colors.getTint(self.hue)
                self.shade: str = \
                    Tetromino.colors.getShade(self.hue)

            def getCellColors(self) -> tuple:
                return self.hue, self.tint, self.shade

            @staticmethod
            def getPiece() -> list[list[bool]]:
                return [[True, True],
                        [True, True]]

            @staticmethod
            def getPieceType() -> str:
                return "O"

            def __eq__(self, other):
                if isinstance(other, Opiece):
                    return True
                elif isinstance(other, str):
                    if other == 'O':
                        return True
                elif isinstance(other, list):
                    return other == self.getPiece()
                else:
                    print('NotImplemented')

        op = Opiece()
        tetros.append(op)

        class Spiece:
            def __init__(self):
                self.hue: str = None
                self.tint: str = None
                self.shade: str = None

            def setColor(self, newColor):
                self.hue = newColor
                self.tint: str = \
                    Tetromino.colors.getTint(self.hue)
                self.shade: str = \
                    Tetromino.colors.getShade(self.hue)

            def getCellColors(self) -> tuple:
                return self.hue, self.tint, self.shade

            @staticmethod
            def getPiece() -> list[list[bool]]:
                return [[False, True, True],
                        [True, True, False]]

            @staticmethod
            def getPieceType() -> str:
                return "S"

            def __eq__(self, other):
                if isinstance(other, Opiece):
                    return True
                elif isinstance(other, str):
                    if other == 'S':
                        return True
                elif isinstance(other, list):
                    return other == self.getPiece()
                else:
                    print('NotImplemented')

        sp = Spiece()
        tetros.append(sp)

        class Tpiece:
            def __init__(self):
                self.hue: str = None
                self.tint: str = None
                self.shade: str = None

            def setColor(self, newColor):
                self.hue = newColor
                self.tint: str = \
                    Tetromino.colors.getTint(self.hue)
                self.shade: str = \
                    Tetromino.colors.getShade(self.hue)

            def getCellColors(self) -> tuple:
                return self.hue, self.tint, self.shade

            @staticmethod
            def getPiece() -> list[list[bool]]:
                return [[False, True, False],
                        [True, True, True]]

            @staticmethod
            def getPieceType() -> str:
                return "T"

            def __eq__(self, other):
                if isinstance(other, Tpiece):
                    return True
                elif isinstance(other, str):
                    if other == 'T':
                        return True
                elif isinstance(other, list):
                    return other == self.getPiece()
                else:
                    print('NotImplemented')

        tp = Tpiece()
        tetros.append(tp)

        class Zpiece:
            def __init__(self):
                self.hue: str = None
                self.tint: str = None
                self.shade: str = None

            def setColor(self, newColor):
                self.hue = newColor
                self.tint: str = \
                    Tetromino.colors.getTint(self.hue)
                self.shade: str = \
                    Tetromino.colors.getShade(self.hue)

            def getCellColors(self) -> tuple:
                return self.hue, self.tint, self.shade

            @staticmethod
            def getPiece() -> list[list[bool]]:
                return [[True, True, False],
                        [False, True, True]]

            @staticmethod
            def getPieceType() -> str:
                return "Z"

            def __eq__(self, other):
                if isinstance(other, Zpiece):
                    return True
                elif isinstance(other, str):
                    if other == 'Z':
                        return True
                elif isinstance(other, list):
                    return other == self.getPiece()
                else:
                    print('NotImplemented')

        zp = Zpiece()
        tetros.append(zp)

        return tetros

    def getPieces(self):
        return [struct.getPiece() for struct in self.tetrisStructs]

    def getColors(self):
        return [struct.color for struct in self.tetrisStructs]

    def getStructs(self):
        return self.tetrisStructs

    def __str__(self):
        print("Is every piece type represented?")
        for struct in self.tetrisStructs:
            print("--" + str(type(struct)))


test = Tetromino()
# print(test.tetrisStructs)
# test.__str__()
