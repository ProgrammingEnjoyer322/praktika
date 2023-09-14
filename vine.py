from PIL import Image
import urllib.request
import os
import math
import time
from xml.dom import minidom
 

class DownloadTile:

    #конструктор для задания объекту параметров
    def __init__(self, lat, lon, zoom=12):
        self._lat = lat #широта
        self._lon = lon #долгота
        self._zoom = zoom #зум

    
    def getXY(self):
        """
        Преобразование широты, долготы и зума в X,Y для поиска плитки
        """
        tile_size = 256

        # сдвиг влево для получения квадрата
        # то есть для зума=2 будет 4 плитки
        numTiles = 1 << self._zoom

        # поиск x
        x = (tile_size/ 2 + self._lon * tile_size / 360.0) * numTiles // tile_size

        # преобразование широты в радианы и вычисление синуса
        sin_y = math.sin(self._lat * (math.pi / 180.0))

        # поиск y
        y = ((tile_size / 2) + 0.5 * math.log((1+sin_y)/(1-sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(x), int(y)

    def downloadImage(self, **kwargs):
        """
            Загружаем и объединяем плитки в 1 изображение
            
            Args:
                tile_width:     The number of tiles wide the image should be -
                                defaults to 5
                tile_height:    The number of tiles high the image should be -
                                defaults to 5
        """

        start_x = kwargs.get('start_x', None) #левая верхняя координата для плитки x
        start_y = kwargs.get('start_y', None) #левая верхняя координата для плитки y
        tile_width = kwargs.get('tile_width', 5) #кол-во плиток по умолчанию в ширину
        tile_height = kwargs.get('tile_height', 5) #кол-во плиток по умолчанию в высоту

        if start_x == None or start_y == None :
            start_x, start_y = self.getXY()
            start_x = start_x-2
            start_y = start_y-2

        # размер изображения
        width, height = 256 * tile_width, 256 * tile_height

        #создание изображения
        map_img = Image.new('RGB', (width,height))

        for x in range(0, tile_width):
            for y in range(0, tile_height) :
                #обращение к картам GET запросом, lyrs=s означает satellite, то есть спутниковый снимок
                url = 'https://mt0.google.com/vt/lyrs=s?x='+str(start_x+x)+'&y='+str(start_y+y)+'&z='+str(self._zoom)

                current_tile = str(x)+'-'+str(y)
                data = urllib.request.urlretrieve(url, current_tile) #загрузка файла
            
                im = Image.open(current_tile)
                map_img.paste(im, (x*256, y*256))
              
                os.remove(current_tile)

        # Сохранить
        map_img.save(str(self._lat) + "_" + str(self._lon) +"_x_"+ str(start_x + x) +"_y_"+str(start_y + y)+"_zoom_"+str(self._zoom)+ ".jpeg")
        #return map_img

def main():
    dom = minidom.parse('export.osm')
    way = dom.getElementsByTagName('way')


    for elem in way:
        nd=elem.getElementsByTagName('nd')
        
        # создание объекта класса DownloadTile
        dt = DownloadTile(float(nd[0].attributes['lat'].value), float(nd[0].attributes['lon'].value), 20)
        try:
            # Получение картинки
            dt.downloadImage()
        except IOError:
            print("Не удалось создать изображение")
        else:
            print("Изображение создано")
    

if __name__ == '__main__':  main()
