#!/usr/bin/env python3

import os, time, json, shutil

ver: str = "0.0.3"

DATA_FILE: str = "./Data/Data.json"
LOG_DIR: str = "./Logs"
CONFIG_FILE: str = "./Config.json"


print(r"  ____                _       ")
print(r" / ___|__ _ _ __   __| |_   _ ")
print(r"| |   / _` | '_ \ / _` | | | |")
print(r"| |__| (_| | | | | (_| | |_| |")
print(r" \____\__,_|_| |_|\__,_|\__, |")
print(r"                        |___/ ")

print(f"v{ver} - 01/04/26 \nAutor: Kātsu Dev. jensaki52@gmail.com. \nPaypal: mitsuprojects3@gmail.com")


# ALL: Función de logs

def log(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    filename: str = f"{time.strftime('%Y-%m-%d')}.log" # Formato del archivo
    path: str = os.path.join(LOG_DIR, filename)

    with open(path, "a") as f: # Escritura del archivo
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n") # Formato del mensaje log

# ALL: Leer y guardar

def load():
    try:
        if not os.path.exists(DATA_FILE): # Verifica si el archivo de data existe
            return {} # Devuelve un diccionario vacio 

        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f) # Devuelve el archivo data cargado
            except json.JSONDecodeError as e:
                log(e)
                return {}
            
    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

def load_config():
    try: 
        if not os.path.exists(CONFIG_FILE): 
            config: dict = { # Opciones del diccionario
                "format": "zip",
                "delAfterPacked": True,
                "every": 5,
                "startOnExecute": False
            }
            
            with open(CONFIG_FILE, "w") as cf:
                try:
                    json.dump(config, cf, indent = 4) # Genera un archivo nuevo si no existe
                    log("Nuevo archivo de configuración creado.")
                except Exception as e:
                    print(f"Error fatal: {e}")
                    log(e)
            
        with open(CONFIG_FILE, "r") as c:
            try:
                return json.load(c) # Devuelve el diccionario del archivo de configuración cargado
            except json.JSONDecodeError as e:
                log(e)
                
    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

def save(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent = 4) # Sobreescribe los datos nuevos
    
    except Exception as e:
            print(f"Error fatal: {e}")
            log(e)

# ALL: Analizador de proyectos

def check(data):
    try:
        print("\nVerificando proyectos...")
        errors: int = 0 # Variable de carpetas erroneas

        for k, v in data.items(): # Recorre data en busca de errores
            if not os.path.exists(v['src']):
                print(f"Proyecto {k} no encontrado: {v['src']}")
                log(f"Error: Proyecto no encontrado {v['src']}")
                errors += 1 # Lo añade a la lista

            if not os.path.exists(v['backup']):
                print(f"Backup {k} no encontrado: {v['backup']}")
                log(f"Error: Backup no encontrado {v['backup']}")
                errors += 1

        print(f"\nVerificación completa. {errors} errores.")
        return errors # Devuelve el número de errores
    
    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

def weight(path):
    size: int = 0
    try:
        for d, _, f in os.walk(path): # Recorre los directorios de forma recursiva 
            for file in f:
                fp = os.path.join(d, file)
                if os.path.exists(fp):
                    size += os.path.getsize(fp) # Captura el peso y lo suma
        return size # Devuelve el peso total en bytes

    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

# ALL: Añadir nuevo proyecto

def add(data):
    src: str = input("Directorio del proyecto: ")
    dst: str = input("Directorio de respaldo: ")

    try:
        if not os.path.exists(src) or not os.path.exists(dst):
            print("Ruta inválida")
            return

        new_id = str(len(data) + 1)

        data[new_id] = {
            "src": src,
            "backup": dst,
            "version": "1.0",
            "weight": weight(src),
            "pkgCount": 0
        }

        save(data)
        log(f"Proyecto añadido: {src}")
        print("Proyecto agregado.")

    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

# ALL: Listado de proyectos

def list_projects(data):
    if not data:
        print("No hay proyectos.")
        return

    for k, v in data.items():
        print(f"ID {k}: {v['src']}, {v['weight']}bytes. (v{v['version']})")

# ALL: Monitorea cuando un proyecto se actualiza

def run(data, f_data):
    print("Monitoreando cambios... (Ctrl+C para salir)")
    try:
        while True:
            for k, v in data.items():
                if not os.path.exists(v['src']):
                    log(f"Error: Ruta no encontrada {v['src']}")
                    continue

                w = weight(v['src'])
                if w > v['weight']:
                    dest = os.path.join(v['backup'], v['version'])
                    os.makedirs(dest, exist_ok=True)

                    shutil.copytree(v['src'], dest, dirs_exist_ok=True)

                    v['weight'] = w
                    save(data)

                    log(f"Backup creado para {v['src']} versión {v['version']}")
                    print(f"Backup actualizado: {v['src']}")

            time.sleep(f_data['every'])

    except KeyboardInterrupt:
        print("\nMonitoreo detenido.")
        log("Monitoreo abortado.")
    
    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

# ALL: Empaquetar en un zip

def package(data, f_data):
    id = input("ID del proyecto: ")
    
    try:
        if id not in data:
            print("ID inválido.")
            return
        
        v: dict = data[id]
        name: str = f"{os.path.basename(v['src'])}_backup_{v['pkgCount']}"
        path: str = v['backup']

        if not os.path.exists(path):
            print("No existe este directorio.")
            return

        fmt = f_data['format']
        shutil.make_archive(name, fmt, path)

        # Determine the actual file extension produced by make_archive
        ext_map = {
            'zip': '.zip',
            'tar': '.tar',
            'gztar': '.tar.gz',
            'bztar': '.tar.bz2',
            'xztar': '.tar.xz'
        }
        ext = ext_map.get(fmt, '.zip')
        shutil.move(f"{name}{ext}", path)

        log(f"Proyecto empaquetado: {name}")
        print("Empaquetado listo.")

        v['pkgCount'] += 1
        save(data)

        if f_data['delAfterPacked']:
            log(f"Borrado automático")
            for d in os.listdir(v['backup']):
                entry = os.path.join(v['backup'], d)
                if os.path.isdir(entry):
                    shutil.rmtree(entry)
                    log(f"{entry} ha sido borrado.")

    except NotADirectoryError:
        print("...")

    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

# ALL: Cambiar los valores de los proyectos

def change(data):
    id = input("ID del proyecto: ")

    if id in data:
        try:
            op: int = int(input(f"Escoge un parametro a editar. Editando: {os.path.abspath(data[id]['src'])}. \n - Origen(1) \n - Respaldo(2) \n - Versión(3) \n"))
            if op < 1 or op > 3:
                print("Debes elegir una de las opciones establecidas.")
            
            elif op == 1:
                newd: str = input("Nuevo directorio a respaldar: ")
                if os.path.exists(newd):
                    data[id]['src'] = newd
                    save(data)
                    print("Cambios guardados.")
                    log(f"Origen de proyecto actualizado: {os.path.abspath(data[id]['src'])} ({data[id]['src']})")

                else:
                    print("Ruta inválida.")
                    return
            
            elif op == 2:
                oldd: str = data[id]['backup']
                newd: str = input("Nuevo directorio de respaldo: ")

                if os.path.exists(newd):
                    try:
                        data[id]['backup'] = newd
                        save(data)
                        shutil.copytree(oldd, newd, dirs_exist_ok=True)
                        shutil.rmtree(oldd)

                        print("Cambios guardados.")
                        log(f"Respaldo de proyecto actualizado: {data[id]['backup']} ({data[id]['src']})")
                    except Exception as e:
                        print(f"Error fatal: {e}")

                else:
                    print("Ruta inválida.")
                    return
            
            elif op == 3:
                newv: str = input("Cambiar versión del respaldo: ")
                data[id]['version'] = newv
                save(data)
                print("Cambios guardados")
                log(f"Versión del proyecto actualizada: {os.path.abspath(data[id]['src'])} ({data[id]['version']})")

        except ValueError:
            print("Debes elegir una de las opciones establecidas.")
            return
        except Exception as e:
            print(f"Error fatal: {e}")
            log(e)
    
    else:
        print("ID inválido.")
        return

def help():
    print(f"Candy v{ver}, estos son funciones internas del programa.")
    print(f"Lista de comandos: \n - help: Muestra la lista de comandos. \n - add: Agrega un proyecto nuevo. \n - change/ch: Cambia los datos de un proyecto. \n - package/pkg: Empaqueta el backup de un proyecto. \n - list/ls: Muestra la lista de proyectos. \n - check: Recorre los directorios configurados y verifica que existan. \n - run: Empieza a monitorear los cambios entre los directorios establecidos y el directorio de backup. \n - exit: Termina el programa. \nRecuerde que puede cambiar ciertos comportamientos del programa en {os.path.join(CONFIG_FILE)}.")

# CLI

def main():
    try:    
        data: dict = load()
        f_data: dict = load_config()
        
        log("Programa iniciado.")

        if not data:
            print("\nNo hay proyectos configurados.")

        # PARCHEADO
        """elif not f_data: 
            print("Advertencia: No es posible cargar el archivo de configuración, se creará uno nuevo.")
            log("Error al cargar 'Config.json'")"""

        if f_data.get('startOnExecute', False):
            log("Inicio automático.")
            run(data, f_data)

        de: int = check(data)
        if de > 0:
            op: str = input(f"Advertencia: Existen {de} directorios erroneos ¿Deseas continuar? (s/n): ").lower()
            if op != "s":
                return

        while True:
            cmd: str = input("\nIngresa un comando (help): ").lower()
            cmd = cmd.replace(" ", "")

            if cmd == "add":
                add(data)

            elif cmd == "list" or cmd == "ls":
                list_projects(data)

            elif cmd == "run":
                run(data, f_data)

            elif cmd == "package" or cmd == "pkg":
                package(data, f_data)

            elif cmd == "change" or cmd == "ch":
                change(data)
            
            elif cmd == "check":
                check(data)
            
            elif cmd == "help":
                help()

            elif cmd == "exit":
                log("Programa finalizado.")
                break
            
            else:
                print("Comando no reconocido, use 'help' para ver la lista de comandos.")

    except KeyboardInterrupt:
        log("Programa finalizado.")

    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

if __name__ == "__main__":
    main()
