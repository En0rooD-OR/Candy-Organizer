#!/usr/bin/env python3

import os, time, json, shutil

ver: str = "0.0.1"

DATA_FILE: str = "Data/Data.json"
LOG_DIR: str = "Logs"

print(f"Candy Organizer v{ver} - 21/03/26 \nAutor: Kātsu Dev. jensaki52@gmail.com")


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
            except json.JSONDecodeError:
                return {}
            
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

        print(f"\nVerificación completa. {errors} errores.\n")
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
        print(f"ID {k}: {v["src"]} (v{v["version"]})")

# ALL: Monitorea cuando un proyecto se actualiza

def run(data):
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

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nMonitoreo detenido.")
    
    except Exception as e:
        print(f"Error fatal: {e}")
        log(e)

# ALL: Empaquetar en un zip

def package(data):
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
        shutil.make_archive(name, "zip", path)
        shutil.move(f"{name}.zip", path)
        #shutil.rmtree(os.path.join(v["backup"], v["version"]))

        log(f"Proyecto empaquetado: {name}")
        print("Empaquetado listo.")
    
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

# CLI

def main():
    data: dict = load()

    if not data:
        print("No hay proyectos configurados.")

    if check(data) > 0:
        op: str = input("¿Deseas continuar? (s/n): ").lower()
        if op != "s":
            return

    while True:
        cmd: str = input("\nIngresa un comando (add/change/package/list/run/exit): ").lower()

        if cmd == "add":
            add(data)
        elif cmd == "list":
            list_projects(data)
        elif cmd == "run":
            run(data)
        elif cmd == "package":
            package(data)
        elif cmd == "change":
            change(data)
        elif cmd == "exit":
            break
        else:
            print("Comando no reconocido.")


if __name__ == "__main__":
    main()
