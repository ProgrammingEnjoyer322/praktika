# Программа для выборки данных с Google Maps.
Для работы программы необходимы данные в формате XML.
Для этого перейдите на сайт https://overpass-turbo.eu/
И выполните следующий запрос:

way
  [landuse=vineyard]
  (39.91184298474967,15.704956054687502,40.54198241319326,16.73492431640625);
out geom;

Далее нажмите экспорт -> download необработанные данные OSM.
Загруженный файл без изменений помещаем в папку с програмой.
Запускать программу желательно с включенным VPN в среде IDLE.

В случае если не найден модуль Pil, его необходимо установить
прописав следующую команду в терминале: 
pip install Pillow
