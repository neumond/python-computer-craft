from cc import gps


print('It must be impossible to gps locate on basic computer')
print('for this test to complete')

assert gps.locate() is None

input('Attach wireless modem to computer [enter]')

assert gps.locate() is None
assert gps.locate(debug=True) is None
assert gps.locate(timeout=5, debug=True) is None

print('Test finished successfully')
