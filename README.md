# Convertir datos de salud de Apple de XML a CSV

Un sencillo script para convertir el archivo export.xml de Apple Health en un csv fácil de usar.



## Como ejecutarlo 

### 1. Verifique que tiene Python 3 y Pandas instalados en su máquina o entorno

`python --version` debería devolver _Python 3.x.x_ donde x es cualquier número. 

Si tiene Python 2.x.x, actualice a Python 3 aquí: https://www.python.org/downloads/ (o especifique la versión de Python de su entorno)

`python3 -c «import pandas»` debería devolver en blanco desde la línea de comandos

Si obtiene un _**ModuleNotFoundError: No module named 'pandas'**_ error, instale pandas e inténtelo de nuevo:

`pip3 install pandas`

### 2. Exporte sus datos de Apple Health

| Health Home | ➡️ | Export Data |
|--|--|--|
|<img style=«float: left;» src=«img/health_home.jpg» width=300>|||<img style=«float: left;» src=«img/export_data_button.jpg» width = 300 >||

Sus datos serán preparados, y entonces usted puede transferir el archivo export.zip a su máquina.

### 3. Descomprima el archivo, que debería contener:

* apple_health_export
* export.xml (Este es el archivo con los datos que desea convertir)

* export_cda.xml


### 4. Coloque el archivo «apple_health_xml_convert.py» de este repositorio en la carpeta junto a los archivos y ejecute el script

`python3 apple_health_xml_convert.py`



La exportación se escribirá con el formato

* **apple_health_export_YYYY-MM-DD.csv**



En Excel, la salida debería ser algo parecido a esto:

<img style=«float: left;» src=«img/example_output.jpg»>

Nota: Este script elimina los prefijos de datos de Apple Health: `HKQuantityTypeIdentifier`, `HKCategoryTypeIdentifier` y `HKCharacteristicTypeIdentifier` para mejorar la legibilidad. No dude en comentar esas líneas en el código con un `#` si desea mantenerlas en la salida CSV.
