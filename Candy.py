#!/usr/bin/env python3

import os, time, json, shutil

ver: str = "0.0.2"

DATA_FILE: str = "./Data/Data.json"
LOG_DIR: str = "./Logs"
CONFIG_FILE: str = "./Config.json"

print(f"Candy Organizer v{ver} - 24/03/26 \nAutor: Kātsu Dev. jensaki52@gmail.com. Paypal: mitsuprojects3@gmail.com")


# ALL: Función de logs

def log(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    filename: str = time.strftime("%Y-%m-%d") + ".log"
    path: str = os.path.join(LOG_DIR, filename)

    with open(path, "a") as f:
        f.write(f"[{time.strftime("%H:%M:%S")}] {msg}\n")

# ALL: Leer y guardar

def load():
    try:
        if not os.path.exists(DATA_FILE):
            return {}

        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                log(e)
                return {}
            
    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

def load_config():
    try: 
        with open(CONFIG_FILE, "r") as c:
            try:
                return json.load(c)
            except json.JSONDecodeError as e:
                log(e)
                
    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

def save(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    
    except Exception as e:
            print(f"Error fatal: {e}")
            log(e)

# ALL: Analizador de proyectos

def check(data) -> int:
    try:
        print("\nVerificando proyectos...")
        errors: int = 0

        for k, v in data.items():
            if not os.path.exists(v["src"]):
                print(f"Proyecto {k} no encontrado: {v["src"]}")
                log(f"ERROR: Proyecto no encontrado {v["src"]}")
                errors += 1

            if not os.path.exists(v["backup"]):
                print(f"Backup {k} no encontrado: {v["backup"]}")
                log(f"ERROR: Backup no encontrado {v["backup"]}")
                errors += 1

        print(f"\nVerificación completa. {errors} errores.")
        return errors
    
    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

def weight(path):
    size: int = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for file in filenames:
                fp = os.path.join(dirpath, file)
                if os.path.exists(fp):
                    size += os.path.getsize(fp)
        return size

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
            "weight": weight(src)
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
        print(f"ID {k}: {v["src"]}, {v["weight"]}bytes. (v{v["version"]})")

# ALL: Monitorea cuando un proyecto se actualiza

def run(data, f_data):
    print("Monitoreando cambios... (Ctrl+C para salir)")
    try:
        while True:
            for k, v in data.items():
                if not os.path.exists(v["src"]):
                    log(f"ERROR: Ruta no encontrada {v["src"]}")
                    continue

                w = weight(v["src"])
                if w > v["weight"]:
                    dest = os.path.join(v["backup"], v["version"])
                    os.makedirs(dest, exist_ok=True)

                    shutil.copytree(v["src"], dest, dirs_exist_ok=True)

                    v["weight"] = w
                    save(data)

                    log(f"Backup creado para {v["src"]} versión {v["version"]}")
                    print(f"Backup actualizado: {v["src"]}")

            time.sleep(f_data["every"])

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
        path: str = v["backup"]

        if not os.path.exists(path):
            print("No existe este directorio.")
            return

        name: str = f"{os.path.basename(v["src"])}_backup"
        shutil.make_archive(name, f_data["format"], path)
        shutil.move(f"{name}.zip", path)

        log(f"Proyecto empaquetado: {name}")
        print("Empaquetado listo.")

        if f_data["delAfterPacked"]:
            log(f"Borrado automático")
            for d in os.listdir(v["backup"]):
                shutil.rmtree(os.path.join(v["backup"], d))
                log(f"{os.path.join(v["backup"], d)} ha sido borrado.")
                
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
            op: int = int(input(f"Escoge un parametro a editar. Editando: {os.path.abspath(data[id]["src"])}. \n - Origen(1) \n - Respaldo(2) \n - Versión(3) \n"))
            if op < 1 or op > 3:
                print("Debes elegir una de las opciones establecidas.")
            
            elif op == 1:
                newd: str = input("Nuevo directorio a respaldar: ")
                if os.path.exists(newd):
                    data[id]["src"] = newd
                    save(data)
                    print("Cambios guardados.")
                    log(f"Origen de proyecto actualizado: {os.path.abspath(data[id]["src"])} ({data[id]["src"]})")

                else:
                    print("Ruta inválida.")
                    return
            
            elif op == 2:
                newd: str = input("Nuevo directorio de respaldo: ")
                if os.path.exists(newd):
                    data[id]["backup"] = newd
                    save(data)
                    print("Cambios guardados.")
                    log(f"Respaldo de proyecto actualizado: {data[id]["backup"]} ({data[id]["src"]})")

                else:
                    print("Ruta inválida.")
                    return
            
            elif op == 3:
                newv: str = input("Cambiar versión del respaldo: ")
                data[id]["version"] = newv
                save(data)
                print("Cambios guardados")
                log(f"Versión del proyecto actualizada: {os.path.abspath(data[id]["src"])} ({data[id]["version"]})")

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
            print("No hay proyectos configurados.")

        elif not f_data: 
            print("Advertencia: No es posible cargar el archivo de configuración.")
            log("No es posible cargar 'Config.json'")

        de: int = check(data)
        if de > 0:
            op: str = input(f"Advertencia: Existen más de {de} directorios erroneos ¿Deseas continuar? (s/n): ").lower()
            if op != "s":
                return

        while True:
            cmd: str = input("\nIngresa un comando (help): ").lower()

            if cmd == "add":
                add(data)

            elif cmd == "list" or cmd == "ls":
                list_projects(data)

            elif cmd == "run" or f_data["startOnExecute"]:
                run(data, f_data)
                log("Inicio automático.")

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
