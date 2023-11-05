from cc import import_file, os


_lib = import_file('_lib.py', __file__)


with _lib.assert_takes_time(1.5, 3):
    timer_id = os.startTimer(2)
    for e in os.captureEvent('timer'):
        if e[0] == timer_id:
            print('Timer reached')
            break


timer_id = os.startTimer(20)
assert isinstance(timer_id, int)
assert os.cancelTimer(timer_id) is None
assert os.cancelTimer(timer_id) is None

alarm_id = os.setAlarm(0.0)
assert isinstance(alarm_id, int)
assert os.cancelAlarm(alarm_id) is None
assert os.cancelAlarm(alarm_id) is None

with _lib.assert_takes_time(1.5, 3):
    assert os.sleep(2) is None

assert (os.version()).startswith('CraftOS ')
assert isinstance(os.getComputerID(), int)

assert os.setComputerLabel(None) is None
assert os.getComputerLabel() is None
assert os.setComputerLabel('altair') is None
assert os.getComputerLabel() == 'altair'
assert os.setComputerLabel(None) is None
assert os.getComputerLabel() is None

assert isinstance(os.epoch(), int)
assert isinstance(os.day(), int)
assert isinstance(os.time(), (int, float))
assert isinstance(os.clock(), (int, float))

assert os.run({}, '/rom/programs/fun/hello.lua') is True

print('Test finished successfully')
