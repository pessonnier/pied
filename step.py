import pigpio
import time
from collections import deque

# brochage BMC voir https://fr.pinout.xyz/pinout/pin12_gpio18#
# correspondent aux sorties 1,2,3,4 du L298N
outs= [18, 17, 27, 22]

halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

# les colonnes correspondent aux pins 1,3,4,6 du moteur
step_seq = [
  [1,1,0,0],
  [0,1,1,0],
  [0,0,1,1],
  [1,0,0,1]
]

step_seq_1 = [
  [1,0,0,0],
  [0,1,0,0],
  [0,0,1,0],
  [0,0,0,1]
]

periode = 2/10000

pi = pigpio.pi()

for pin in outs:
    pi.set_mode(pin, pigpio.OUTPUT)

def step1(seq = step_seq, periode = periode):
    for step in seq:
        for pin, state in zip(outs, step):
            pi.write(pin, state)
        time.sleep(periode)

def step2(seq = step_seq, periode = periode, plibre = 0):
    for step in seq:
        for pin, state in zip(outs, step):
            pi.write(pin, state)
        time.sleep(periode)
        for pin in outs:
            pi.write(pin, 0)
        time.sleep(plibre)


def stepn(n, step_fun=step1, seq = step_seq, periode = periode):
    for i in range(n):
        step_fun(seq = seq, periode = periode)
    for pin in outs:
        pi.write(pin, 0)

class pasapas:
  def __init__(o, pigpio = pi, outs = outs, periode_tension = periode, periode_libre = 0, step_seq = step_seq):
    o.pi = pi
    o.seq = deque(step_seq)
    o.outs = outs
  
  def avance(o, dir = 1):
    o.date_appel = time.time()
    o.seq.rotate(dir)
    step()
    
  def recule(o):
    o.date_appel = time.time()
    o.seq.rotate(-1)
    step()
    
  def step(o):
    for pin, state in zip(o.outs, o.seq[0]):
      o.pi.write(pin, state)
    duree_code = time.time() - o.date_appel
    time.sleep(o.periode_tension - duree_code)
    date_pause = time.time()
    if o.periode_libre > 0:
      for pin in o.outs:
        o.pi.write(pin, 0)
      duree_code = time.time() - date_pause
      time.sleep(o.periode_libre - duree_code)
    
import time
start = time. time()
stepn(1000, seq = step_seq, periode = 2/10000)
end = time. time()
print(end - start)
