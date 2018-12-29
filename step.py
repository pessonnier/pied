import pigpio
import time

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

step_seq2 = [
  [1,1,0,0],
  [0,0,1,1],
  [0,1,1,0],
  [1,0,0,1]
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


import time
start = time. time()
stepn(1000, seq = step_seq, periode = 2/10000)
end = time. time()
print(end - start)
