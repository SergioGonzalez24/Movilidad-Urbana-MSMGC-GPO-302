from subprocess import call
import threading


def launcher_1():
    call(["python", "./Entregables/EjecutableMesa/launcher_1.py"])


def launcher_2():
    call(["python", "./Entregables/EjecutableMesa/launcher_2.py"])


if __name__ == '__main__':
    t1 = threading.Thread(target=launcher_1)
    t2 = threading.Thread(target=launcher_2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
