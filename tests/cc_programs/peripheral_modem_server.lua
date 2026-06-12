side = 'back'
m = peripheral.wrap(side)
channel = 5
m.close(channel)
m.open(channel)
while true do
    local event, evside, evchannel, reply, msg, dist = os.pullEvent('modem_message')
    if eside == side or evchannel == channel then
        print('reply:', reply, 'msg:', msg, 'dist:', dist)
        if msg == 'stop' then break end
        m.transmit(reply, channel, msg)
    end
end
m.close(channel)
