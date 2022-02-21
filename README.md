# AerioInformes
## Version 2.0.2

Una aplicación para generar los informes de meteorología aeronáutica del DMSA.

## Modo de uso

Solo descarge el archivo comprimido que se le proporciona, descomprima en donde así lo prefiera.
Una vez descomprimido encontrará un archivo ejecutable para su sistema operativo. Ejecute dicho archivo
y se abrirá una ventana para seleccionar y editar las opciones que desee.

### Requisitos de los archivos de MS Office Word

Los archivos de MS Office deben respetar cierto formato debido al espacio limitado con el que se cuenta.
En el caso del documento de la `Tendencia de Aeropuertos`, cada aeropuerto debe tener su comentario, 
además del comentario general, ya que se asume que siempre se encontrará y procure que sea lo más corto 
posible. Si recibe un archivo incompleto y no cuenta con los datos para poder generar alguno de los 
comentarios, agregue el texto que desee, se recomienda: **No hay datos para este aeropuerto**.

También, asegúrese de que los documentos disponibles de `Dispersión de Ceniza` cuenten con al menos una
imagen.

**Nota:** Ahora puede agregar todos los archivos de MS Word o .docx juntos. Cuando presione el
botón `Agregar .docx` se le abrirá una ventana de diálogo donde podrá navegar hasta la ruta donde se 
encuentran los archivos. **Por esta razón se recomienda siempre tener todos los archivos de la ceniza 
volcánica y la tendencia de aeropuertos en la misma carpeta,** ya que además, en esta versión esta es la 
única manera de adjuntar estos archivos. Tenga cuidado de no adjuntar más archivos de la cuenta, o de 
adjuntar dos archivos para el mismo volcán, ya que las imágenes extraidas desde uno de los archivos serán 
sobreescritas por el otro.

### Agregar otro usuario

Si su nombre no aparece en las opciones de selección de usuario, puede usar la opción de `Otro usuario`. 
Agregue su nombre y usuario del IMN en los espacios correspondientes (**no es necesario que escriba la 
dirección de correo completa, por ejemplo, para el usuario `Diego Garro` solo debe escribir `dgarro`. El   
programa completará el resto**).

### Creación del informe

Una vez que haya concluido con la selección y edición de las opciones presione el botón `Crear Informe`,
el programa empezará a procesar los datos (talvez parezca que no responde pero realmente está trabajando),
si hay algún problema aparecerá una ventana emergente informándole, seleccione qué hacer o dé click en aceptar para corregir cualquier falta de información y vuelva a intentarlo.

Cuando el proceso de creación del informe concluya sin problemas se le informará también con una ventana
emergente, haga click en aceptar y su informe estará listo.

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

Una vez finalizado el proceso de creación del informe de manera exitosa, se le presentará una ventana 
emergente informándole. En tal caso puede cerrar el programa pulsando el botón `Salir` o la `X` en la 
esquina superior derecha o izquierda según su sistema operatvo.


Informe de cualquier mal funcionamiento a:

Diego Garro Molina
dgarro@imn.ac.cr