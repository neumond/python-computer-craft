from cc import os


timer_id = os.startTimer(2)
for e in os.captureEvent('timer'):
    if e[0] == timer_id:
        print('Timer reached')
        break
