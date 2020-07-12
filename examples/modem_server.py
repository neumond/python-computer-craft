from cc import peripheral


side = 'back'
m = peripheral.wrap(side)
listen_channel = 5
for msg in m.receive(listen_channel):
    print(repr(msg))
    if msg.content == 'stop':
        break
    else:
        m.transmit(msg.reply_channel, listen_channel, msg.content)
