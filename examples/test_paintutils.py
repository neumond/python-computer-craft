from cc import import_file, fs, os, term, colors, paintutils

_lib = import_file('_lib.py', __file__)


pixels = '''
0000000030030033333333330000000003000000000000000
0333300000000033333333300000000000333333000000330
0803000000803033333333000000000000880330300003000
0800800030330333333333000300883000888880000033000
3333000000003333333333300080038880000080000888003
33333ddd3333333333333333300000333330000000000d033
333dddddd3333333333333333333333333333333333ddd333
3333ccdd333333333333344444444333333333333dddddd33
333cc33d3333333333334444444444333333333335d3cc33d
5ddc33333333333333344444444444433333333333333cd55
dddc555d3333333333344444444444433333333333d5dc5dd
d5dd5dd4bbbbbbbbb999b00b00300b3bb9999bbbb4ddddddd
ddd55444bb999993bbb33390b030bb9999bbbbbbb444ddddd
55dd44bbbbbbbbbbbbb9bb3003003bbb339bbbbbbbb44444d
dd444bbbbbbbbbbb99933bbb0030b999bbbbbbbbbbbbbbb44
444bbbbbbbbbbbbbbb9bbb33b309933bbbbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbbbbbb9bbbb3bbbb99bbbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbbbbbbbb399399bbbbbbbbbbbbbbbbbbbbb
'''.strip()


assert _lib.get_class_table(paintutils) == _lib.get_object_table('paintutils')

with fs.open('img.nfp', 'w') as f:
    f.write(pixels)

int_pixels = paintutils.loadImage('img.nfp')
assert len(int_pixels) > 0
assert len(int_pixels[0]) > 0
assert paintutils.parseImage(pixels) == int_pixels

assert paintutils.drawImage(int_pixels, 1, 1) is None

os.sleep(2)

term.setTextColor(colors.white)
term.setBackgroundColor(colors.black)
term.clear()
term.setBackgroundColor(colors.green)

by = 3
bx = 3

assert paintutils.drawPixel(bx, by) is None
assert paintutils.drawPixel(bx + 1, by, colors.red) is None

bx += 5

assert paintutils.drawLine(bx, by, bx + 3, by + 3) is None
assert paintutils.drawLine(bx + 3, by, bx, by + 3, colors.red) is None

bx += 5
assert paintutils.drawBox(bx, by, bx + 3, by + 3) is None
bx += 5
assert paintutils.drawBox(bx, by, bx + 3, by + 3, colors.red) is None

bx += 5
assert paintutils.drawFilledBox(bx, by, bx + 3, by + 3) is None
bx += 5
assert paintutils.drawFilledBox(bx, by, bx + 3, by + 3, colors.red) is None

term.setCursorPos(1, by + 6)

os.sleep(2)

print('Test finished successfully')
