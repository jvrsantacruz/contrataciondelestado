# Scraping contrataciondelestado.es

La página [contrataciondelestado.es](http://www.contrataciondelestado.es) almacena información
sobre todas las adjudicaciones que realiza la administración central. El programa descarga los
contratos que se encuentran ya adjudicados a una empresa.

La información descargada incluye qué servicios son contratados por qué administración, así como la empresa que los
realiza y la cuantía total del contrato.
Estos datos resultan de gran interés, al tratarse de algo tan delicado como de la gestión de dinero
público.

## Uso

1. Crear un virtualenv: `virtualenv env --python python2`
1. Y activarlo: `. env/bin/activate`
2. Instalar requisitos: `pip install -r reqs.txt`
3. Ejecutar script: `python2 fetch.py`

Los ficheros xml guardarán en el fichero sqlite resultante.
Si la sesión se desconecta por algún motivo, es necesario volver a empezar desde el principio.


## Datos

Los datos obtenidos por el script `fetch.py` son descargados y almacenados directamente sin tratamiento, en el mismo formato en el que se encuentran en la página web.

Se trata de un fichero xml que sigue el esquema [CODICE](http://joinup.ec.europa.eu/catalogue/asset_release/codice) para licitación desarrollado por España.
Este formato es fácilmente parseable.
