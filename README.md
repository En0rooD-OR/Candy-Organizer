Autor: Katsu Dev

Usalo y editalo como desees

Este es un programa de consola, es decir que no cuenta con GUI.
Funciona como un especie de organizador, guarda una carpeta y copia su contenido en otra, categorizado por versiones. 
Está pensado para usarse con almacenamiento externo, como un usb o una targeta de memoria; tambien se puede usar con almacenamiento interno pero no tendria sentido.

Hay pequeños problemas con el empaquetado, por ejemplo solo guarda un zip por versión, en lugar de reemplazarlo, pero no crashea.
Tampoco puedes borrar proyectos y solo empieza a respaldar archivos luego de ejecutar run. 

Al iniciar el ejecutable se recorrerá todo el diccionario de proyectos, y verificará que los directorios configurados existan; si no, saltará una advertencia y preguntará si deseas continuar.

#### USO:

Siempre se mostrará la lista de funciones en el input de comandos.

**add:** Agrega un proyecto nuevo al diccionario.
```
Espera los args:
!Directorio de origen (str)
!Directorio de respaldo (str)
```

Se asignará por defecto la versión 1.0, y creará un directorio en el directorio de respaldo con la versión como nombre, donde se guardarán los cambios hasta que cambies la versión.
También se les asignará una id de referencia como claves en el diccionario.

**change:** Cambia los datos del proyecto en el diccionario.
```
Espera los args:
!ID del proyecto (int)
-*Directorio de origen (str)
-*Directorio de respaldo (str)
-*Versión (str)
```

Cuidado: Esto no mueve los directorios si se cambia su dirección de respaldo.
Puedes cambiar a una versión anterior sin problemas, se segurá editando el directorio de esa versión si el programa lo está monitoreando

**package:** Empaqueta los últimos cambios de la versión configurada en un archivo zip.
```
Espera los args:
!ID del proyecto (int)
```

Cuidado: Solo se empaqueta una vez por versión, si quieres generar un nuevo empaquetado debes borrar el archivo anterior por tu cuenta.

**list:** Muestra la lista de proyectos y su información

**run:** Empieza a verificar cada 5seg cambios en los proyectos configurados.

Se guardarán reportes de cada actualización y cada error en la carpeta de Logs. La carpeta Data.json contiene los diccionarios de cada proyecto.

Si algo sale mal, considere agregar las carpetas "Logs" y "Data".

#### Dependencias:
```
os, time, json, shutil
``

Actualizaré esto de vez en cuando; solo hice un binario para linux, pero de nuevo, pueden hacer con esto lo que deseen.

# jensaki152@gmail.com
# Paypal: mitsuprojects3@gmail.com
