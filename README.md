# Autor: Katsu Dev

Usalo y editalo como desees

Este es un programa de consola, es decir que no cuenta con GUI.
Funciona como un especie de organizador, guarda una carpeta y copia su contenido en otra, categorizado por versiones. 
Está pensado para usarse con almacenamiento externo, como un usb o una targeta de memoria; tambien se puede usar con almacenamiento interno pero no tendria sentido.

Hay pequeños problemas con el empaquetado por ejemplo, solo guarda un zip por versión, en lugar de reemplazarlo, pero no crashea.
Tampoco puedes borrar proyectos y solo empieza a respaldar archivos luego de ejecutar run. 

Al iniciar el ejecutable se recorrerá todo el diccionario de proyectos, y verificará que los directorios configurados existan; si no, saltará una advertencia y preguntará si deseas continuar.

#### 0.0.2:

**Historial de cambios:**

- *Archivo de configuración añadido:* Puedes cambiar comportamientos del programa cambiando los valores en el archivo `Config.json`:
```
format: Tipo de empaquetado. (str, 'zip' por defecto.)
delAfterPacked: Borrar despues de empaquetar. (bool, 'true' por defecto.)
every: Tiempo de cada actualización del backup. (int/float, '5' por defecto.)
startOnExecute: Iniciar automáticamente despues de ejecutar el programa. (bool, 'false' por defecto.)
```

- *Nuevos logs agregados:* Entre ellos, logs de inicio y finalización del programa, excepciones en `main()` y `run()`.

- *Más excepciones.*

- *Excepción de salida en main:* Ctr+c`.

- *Alternativas al escribir comandos:*
```
- list/ls
- package/pkg
- change/ch
```

- *Función 'check' agregada.*

- *Función 'help' agregada.*

#### USO:

Puede consultar las funciones con el comando 'help'.

**add:** Agrega un proyecto nuevo al diccionario.
```
Espera los args:
!Directorio de origen (str)
!Directorio de respaldo (str)
```
Se asignará por defecto la versión 1.0, y creará un directorio en el directorio de respaldo con la versión como nombre al actualizar, donde se guardarán los cambios hasta que cambies la versión.
También se les asignará una id de referencia como claves en el diccionario.

**change:** Cambia los datos del proyecto en el diccionario.
```
Espera los args:
!ID del proyecto (int)
-*Directorio de origen (str)
-*Directorio de respaldo (str)
-*Versión (str)
```
*Cuidado:* Esto no mueve los directorios si se cambia su dirección de respaldo.
Puedes cambiar a una versión anterior sin problemas, se segurá editando el directorio de esa versión si el programa lo está monitoreando.

**package:** Empaqueta todos los archivos en el directorio del backup.
```
Espera los args:
!ID del proyecto (int)
```
Se empaquetarán con el formato configurado en el archivo `Config.json`, y si está configurado tambien se borrarán los demás directorios dejando solo el archivo configurado.

**list:** Muestra la lista de proyectos y su información.

**check:** Verifica si los directorios configurados existen.

**run:** Empieza a verificar cada 5seg cambios en los proyectos configurados.
Si está configurado en el archivo `Config.json`, se iniciará automáticamente al ejecutar el programa.

Se guardarán reportes de cada actualización y cada error en la carpeta de Logs. La carpeta Data.json contiene los diccionarios de cada proyecto.

Actualizaré esto de vez en cuando; solo hice un binario para linux, pero de nuevo, pueden hacer con esto lo que deseen.

## jensaki152@gmail.com
## Paypal: mitsuprojects3@gmail.com

