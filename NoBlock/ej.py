"""Considerando el programa noblock.py, realizar un programa que lance dos procesos hijos que intenten encontrar el nonce para un No-Bloque con una dificultad dada. 
El hijo que lo encuentre primero debe comunicarse con el padre mediante una señal guardando el nonce en una fifo para que el padre pueda leerla. 
Hacer otra versión pero utilizando pipes."""

import os
import signal
from noblock import NoBlock, proof_of_work

fifo_arc = 'fifo'
if os.path.exists(fifo_arc):
    os.remove(fifo_arc)
os.mkfifo(fifo_arc)

def proceso_hijo(seed):
    block = NoBlock(seed=seed, nonce=0)
    new_hash = proof_of_work(block)
    with open(fifo_arc, 'w') as fifo:
        fifo.write(str(block.nonce))

    os.kill(os.getppid(), signal.SIGUSR1)

def manejar_senal(signum, frame):
    with open(fifo_arc, 'r') as fifo:
        nonce = fifo.read()
    print(f"Nonce encontrado: {nonce}")
    fifo.close()
    exit(0)

signal.signal(signal.SIGUSR1, manejar_senal)

for i in range(1,3):
    pid = os.fork()
    if pid == 0:
        seed = f'Semilla {i}'
        proceso_hijo(seed)
        exit(0)

signal.pause()

os.remove(fifo_arc)
