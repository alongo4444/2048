class Tile:
    def __init__(self, value, i, j):
        self.value = value
        self.i = i
        self.j = j

    def getColor(self):
        return {
            0: '#FFF3D6',
            2: '#FFDC85',
            4: '#FBBE4B',
            8: '#FC7522',
            16: '#FD4D21',
            32: '#FF3333',
            64: '#D00000',
            128: '#ff2d34',
            256: '#9d0208',
            512: '#ab1f2d',
            1024:'#e1235c',
            2048: '#f98b8b'
        }[self.value]
