local genv = getfenv()
local temp = {}
local event_sub = {}
genv.temp = temp
local url = 'http://127.0.0.1:4343/'
local tasks = {}
local filters = {}
local ycounts = {}

ws = http.websocket(url..'ws/')
if ws == false then
    error('unable to connect to server '..url..'ws/')
end
ws.send(textutils.serializeJSON{
    action='run',
    computer=os.getComputerID(),
    args={...},
})

function nullify_array(a, size)
    local r = {}
    for k=1,size do
        if a[k] == nil then
            r[k] = textutils.json_null
        else
            r[k] = a[k]
        end
    end
    return r
end

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
                    yields=0,
                })
            else
                setfenv(fn, genv)
                if msg.immediate then
                    ws.send(textutils.serializeJSON{
                        action='task_result',
                        task_id=msg.task_id,
                        result={fn()},
                        yields=0,
                    })
                else
                    tasks[msg.task_id] = coroutine.create(fn)
                    ycounts[msg.task_id] = 0
                end
            end
        elseif msg.action == 'drop' then
            for _, task_id in ipairs(msg.task_ids) do
                tasks[task_id] = nil
                filters[task_id] = nil
                ycounts[task_id] = nil
            end
        elseif msg.action == 'sub' then
            event_sub[msg.event] = true
        elseif msg.action == 'unsub' then
            event_sub[msg.event] = nil
        elseif msg.action == 'close' then
            if msg.error ~= nil then
                io.stderr:write(msg.error)
            end
            break
        end
    elseif event_sub[event] == true then
        ws.send(textutils.serializeJSON{
            action='event',
            event=event,
            params=nullify_array({p1, p2, p3, p4, p5}, 5),
        })
    end

    local del_tasks = {}
    for task_id in pairs(tasks) do
        if filters[task_id] == nil or filters[task_id] == event then
            local r = {coroutine.resume(tasks[task_id], event, p1, p2, p3, p4, p5)}
            if coroutine.status(tasks[task_id]) == 'dead' then
                ws.send(textutils.serializeJSON{
                    action='task_result',
                    task_id=task_id,
                    result=r,
                    yields=ycounts[task_id],
                })
                del_tasks[task_id] = true
            else
                if r[1] == true then
                    filters[task_id] = r[2]
                else
                    filters[task_id] = nil
                end
                ycounts[task_id] = ycounts[task_id] + 1
            end
        end
    end
    for task_id in pairs(del_tasks) do
        tasks[task_id] = nil
        filters[task_id] = nil
        ycounts[task_id] = nil
    end
end

ws.close()
