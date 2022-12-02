from subprocess import call
import threading



def launcher_1():
    call(["python", "./Entregables/EjecutableMesa/launcher_1.py"])

def launcher_2():
    call(["python", "./Entregables/EjecutableMesa/launcher_2.py"])
        
if __name__ == '__main__':
    t1 = threading.Thread(target=launcher_1)