# Autor: Katsu Dev [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/katsu-def/Candy-Organizer)

Usalo y editalo como desees

Este es un programa de consola, es decir que no cuenta con GUI. diseñado para ser simple y ligero.
Funciona como un especie de organizador, guarda una carpeta y copia su contenido en otra, categorizado por versiones. 
Está pensado para usarse con almacenamiento externo, como un usb o una targeta de memoria.

Al iniciar el ejecutable se recorrerá todo el diccionario de proyectos, y verificará que los directorios configurados existan; si no, saltará una advertencia y preguntará si deseas continuar.

#### 0.0.3:

**Historial de cambios:**

- *Cambios en change/ch:* Ahora mueve los archivos al cambiar la ruta de backup.

- *Cambios en package/pkg:* Ahora se podrá empaquetar los backups múltiples veces, sin embargo se empaquetará todo, incluyendo otros backups.

- *Cambios en Data.json:* Se añadió el parámetro `pkgCount`, donde se guardarán registros de cuantas veces el backup se ha empaquetado.

- *Cambios al leer la configuración:* Ahora al leer `Config.json` se verificará que el archivo exista, caso contrario se generará un archivo nuevo.
**Cuidado:** Esto generará las configuraciones por defecto.

- *Cambios en la lectura de comandos:* Ahora no importará si dejas un espacio al final de cada comando, se leerá igual.

- *Advertencia al no poder leer el archivo de configuración removida.* 

- *Cambios menores de estética y escritura del código*

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

**change/ch:** Cambia los datos del proyecto en el diccionario.
```
Espera los args:
!ID del proyecto (int)
-*Directorio de origen (str)
-*Directorio de respaldo (str)
-*Versión (str)
```
Puedes cambiar a una versión anterior sin problemas, se segurá editando el directorio de esa versión si el programa lo está monitoreando.

**package/pkg:** Empaqueta todos los archivos en el directorio del backup.
```
Espera los args:
!ID del proyecto (int)
```
Se empaquetarán con el formato configurado en el archivo `Config.json`, y si está configurado se limpiarán los demás directorios, dejando solo el empaquetado.

**list/ls:** Muestra la lista de proyectos y su información.

**check:** Verifica si los directorios configurados existen.

**run:** Verifica cambios en el directorio de origen y actualiza el backup.
Si está configurado en el archivo `Config.json`, se iniciará automáticamente al ejecutar el programa; de igual manera dependiendo de la configuración, la frecuencia de monitoreo cambiará.

#### CONFIGURACIÓN:
```
format: Tipo de empaquetado. (str, 'zip' por defecto.)
delAfterPacked: Borrar después de empaquetar. (bool, 'true' por defecto.)
every: frecuencia de actualización actualización del backup. (int/float, '5' por defecto.)
startOnExecute: Iniciar automáticamente al ejecutar el programa. (bool, 'false' por defecto.)
```

Se guardarán reportes de cada actualización y cada error en la carpeta de Logs. El archivo Data.json contiene los diccionarios de cada proyecto.

Actualizaré esto de vez en cuando; solo hice un binario para linux, pero de nuevo, pueden hacer con esto lo que deseen.

## jensaki152@gmail.com
## Paypal: mitsuprojects3@gmail.com

