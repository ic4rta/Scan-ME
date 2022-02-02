import os
import socket
import multiprocessing
import subprocess
from colorama import Fore, init

def mi_ip():
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(("8.8.8.8", 80))
    res = ip.getsockname()[0]
    ip.close()
    return res

def ping(emp, res):
    DEVNULL = open(os.devnull, 'w')
    while True:
        ip = emp.get()
        if ip is None:
            break
        try:
            subprocess.check_call(['ping', '-c1', ip], stdout=DEVNULL)
            res.put(ip)
        except:
            pass

def scan(max = 255):
    lista_ip = list()
    ip_comp = mi_ip().split('.')
    base_ip = ip_comp[0] + '.' + ip_comp[1] + '.' + ip_comp[2] + '.'
    iniciar = multiprocessing.Queue()
    res = multiprocessing.Queue()
    pool = [multiprocessing.Process(target=ping, args=(iniciar, res)) for i in range(max)]

    for i in pool:
        i.start()
    for i in range(1, 255):
        iniciar.put(base_ip + '{0}'.format(i))
    for i in pool:
        iniciar.put(None)
    for i in pool:
        i.join()

    while not res.empty():
        ip = res.get()
        lista_ip.append(ip)

    return lista_ip

def ports(host, puerto_final):
    puertos_abiertos = list()
    try:
        ip = socket.gethostbyname(host)
    except ValueError:
        return
    try:
        for puertos in range(1, puerto_final):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            res = s.connect_ex((ip, puertos))
            if res == 0:
                puertos_abiertos.append(puertos)

    except socket.gaierror:
        print("No se pudo encontrar el nombre del host")
    except socket.error:
        print("No se pudo conectar al servidor")
    
    return puertos_abiertos

def menu():
    print(Fore.GREEN + " ___   ___    __    _  _       __  __  ____ ")
    print(Fore.CYAN + "/ __) / __)  /__\  ( \( ) ___ (  \/  )( ___)")
    print(Fore.YELLOW + "\__ \( (__  /(__)\  )  ( (___) )    (  )__)") 
    print(Fore.MAGENTA + "(___/ \___)(__)(__)(_)\_)     (_/\/\_)(____)")
    print(Fore.WHITE + "\n\n1) Mostrar IP de los host conectados")
    print("2) Buscar puertos abiertos de un host")
    print("3) Salir")
def main():
    while True:
        menu()
        try:
            opc = int(input("Ingrese una opcion: "))
            os.system('clear')
            if opc in range(3):
                if opc == 1:
                    print("\nEscaneando...")
                    lst = scan()
                    os.system("clear")
                    print(f"\nSu IP: {mi_ip()}")
                    print("Todos los host de su red")
                    print("\n", lst)
                
                elif opc == 2:
                    host = input("Ingres el host: ")
                    puerto_final = int(input("Ingrese el puerto: "))
                    lst2 = ports(host, puerto_final)
                    print("\nEscaneando...")
                    os.system("clear")
                    print(f"Puertos abiertos de: {host}")
                    print(lst2)
            elif opc == 3:
                break
            else:
                print("No es una opcion correcta")
        except ValueError:
            print("Ingresa un numero")

if __name__ == '__main__':
    main()
