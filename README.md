# AerioInformes
## Version 2.0.0

Una aplicación para generar los informes de meteorología aeronáutica del DMSA.

## Modo de uso

Solo descarge el archivo comprimido que se le proporciona, descomprima en donde así lo prefiera.
Una vez descomprimido encontrará un archivo ejecutable para su sistema operativo. Ejecute dicho archivo
y se abrirá una ventana para seleccionar y editar las opciones que desee.

**Nota importante:** Ahora puede agregar todos los archivos de MS Word o .docx juntos. Cuando presione el
botón `Agregar .docx` se le abrirá una ventana de diálogo donde podrá navegar hasta la ruta donde se encuentran
los archivos. **Por esta razón se recomienda siempre tener todos los archivos de la ceniza volcánica y la
tendencia de aeropuertos en la misma carpeta,** ya que además, en esta versión esta es la única manera de
adjuntar estos archivos. Tenga cuidado de no adjuntar más archivos de la cuenta, o de adjuntar dos archivos
para el mismo volcán, ya que las imágenes extraidas en uno serán sobreescritas por el otro.

Una vez que haya concluido con la selección y edición de las opciones presione el botón `Crear Informe`,
el programa empezará a procesar los datos (talvez parezca que no responde pero realmente está trabajando),
si hay algún problema aparecerá una ventana emergente informándole, seleccione qué hacer o dé click en aceptar
para corregir cualquier falta de información y vuelva a intentarlo.

Cuando el proceso de creación del informe concluya sin problemas se le informará también con una ventana
emergente, dé click en aceptar y su informe estará listo.

## ¿Dónde se encuentran los archivos generados?

El programa genera un árbol de carpetas si no se encuentran disponibles en el mismo directorio donde está
el archivo ejecutable. Las carpetas son `images` y `pdf`.

**`images`:** Dentro de esta carpeta encontrará dos más, `output` y `volcanoes`, para nuestro caso, la que
más interesa es `output`, ahí se encuentran las imágenes de salida del programa, las cuales conforman el
informe aeronáutico deseado. Las imágenes están numeradas, en caso de que alguna información no se haya
suministrado al programa y la imagen no se haya generado, verá que la numeración no es secuencial. Queda a
discresión del usuario verificar que se hayan generado las imágenes deseadas con la información suministrada
al programa. Dentro de `volcanoes` se enuentran otras tres: `turrialba`, `poas` y `rvieja`. Dentro de cada una
se encuentran las imágenes extraídas de los informes de ceniza volcánica, dichas imágenes no son de interés
para el usuario. **El contenido de cada una de éstas carpetas se borra cada vez que se inicia el programa.**

**`pdf`:** Dentro de esta carpeta se crea un arbol de directorios por año y mes, de manera que para cada año se
va creando una carpeta nueva, y lo mismo para cada mes. Dentro de cada carpeta del mes se irán creando los
archivos en formato .pdf que serán agregados al SGC-MET en su respectivo registro.

Cualquier mal funcionamiento favor comunicarse con:

Diego Garro Molina
dgarro@imn.ac.cr