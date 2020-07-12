from cc import colors, textutils


assert textutils.slowWrite('write ') is None
assert textutils.slowWrite('write ', 5) is None
assert textutils.slowPrint('print') is None
assert textutils.slowPrint('print', 5) is None

assert textutils.formatTime(0) == '0:00 AM'
assert textutils.formatTime(0, True) == '0:00'

table = [
    colors.red,
    ['Planet', 'Distance', 'Mass'],
    colors.gray,
    ['Mercury', '0.387', '0.055'],
    colors.lightGray,
    ['Venus', '0.723', '0.815'],
    colors.green,
    ['Earth', '1.000', '1.000'],
    colors.red,
    ['Mars', '1.524', '0.107'],
    colors.orange,
    ['Jupiter', '5.203', '318'],
    colors.yellow,
    ['Saturn', '9.537', '95'],
    colors.cyan,
    ['Uranus', '19.191', '14.5'],
    colors.blue,
    ['Neptune', '30.069', '17'],
    colors.white,
]

assert textutils.tabulate(*table) is None

lines = textutils.pagedPrint('''
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Suspendisse feugiat diam et velit aliquam, nec porttitor eros facilisis.
Nulla facilisi.
Sed eget dui vel tellus aliquam fermentum.
Aliquam sed lorem congue, dignissim nulla in, porta diam.
Aliquam erat volutpat.
'''.strip())
assert isinstance(lines, int)
assert lines > 0

assert textutils.pagedTabulate(*table[:-1], *table[2:-1], *table[2:]) is None

assert textutils.complete('co', ['command', 'row', 'column']) == [
    'mmand', 'lumn']

print('Test finished successfully')
