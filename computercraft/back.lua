local genv = getfenv()
local temp = {}
local event_sub = {}
genv.temp = temp
local url = 'http://127.0.0.1:4343/'
local tasks = {}

ws = http.websocket(url..'ws/')
if ws == false then
    error('unable to connect to server '..url..'ws/')
end
ws.send(textutils.serializeJSON{
    action='run',
    computer=os.getComputerID(),
    args={...},
})

while true do
    local event, p1, p2, p3, p4, p5 = os.pullEvent()

    if event == 'websocket_message' then
        msg = textutils.unserializeJSON(p2)
        if msg.action == 'task' then
            local fn, err = loadstring(msg.code)
            if fn == nil then
                ws.send(textutils.serializeJSON{
                    action='task_result',
                    task_id=msg.task_id,
                    result={false, err},
                })
            else
                setfenv(fn, genv)
                if msg.immediate then
                    ws.send(textutils.serializeJSON{
                        action='task_result',
                        task_id=msg.task_id,
                        result={fn()},
                    })
                else
                    tasks[msg.task_id] = coroutine.create(fn)
                end
            end
        elseif msg.action == 'sub' then
            event_sub[msg.event] = true
        elseif msg.action == 'unsub' then
            event_sub[msg.event] = nil
        elseif msg.action == 'close' then
            if msg.error ~= nil then
                print(msg.error)
            end
            break
        else
            print(msg)
        end
    elseif event_sub[event] == true then
        ws.send(textutils.serializeJSON{
            action='event',
            event=event,
            params={p1, p2, p3, p4, p5},
        })
    end

    local del_tasks = {}
    for task_id in pairs(tasks) do
        local r = {coroutine.resume(tasks[task_id], event, p1, p2, p3, p4, p5)}
        if coroutine.status(tasks[task_id]) == 'dead' then
            ws.send(textutils.serializeJSON{
                action='task_result',
                task_id=task_id,
                result=r,
            })
            del_tasks[task_id] = true
        end
    end
    for task_id in pairs(del_tasks) do
        tasks[task_id] = nil
    end
end

ws.close()
