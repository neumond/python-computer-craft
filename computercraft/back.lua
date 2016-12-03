local genv = getfenv()
local temp = {}
genv.temp = temp
local url = 'http://127.0.0.1:4343/'
local args = {...}
local tasks = {}

-- https://www.lua.org/pil/11.4.html
local Queue = {}
function Queue.new()
    return {head = 0, tail = 0}
end
function Queue.push(q, value)
    q[q.head] = value
    q.head = q.head + 1
end
function Queue.pop(q)
    if q.tail >= q.head then return nil end
    local value = q[q.tail]
    q[q.tail] = nil
    q.tail = q.tail + 1
    return value
end
function Queue.length(q)
    return q.head - q.tail
end
local output = Queue.new()

local function is_special_task(task_id)
    return (task_id == '_fetch' or task_id == '_send')
end

local function string_split(text)
    local pos = string.find(text, ';')
    return string.sub(text, 1, pos - 1), string.sub(text, pos + 1)
end

local function inner_resume(task_id, ...)
    local r = {coroutine.resume(tasks[task_id].co, ...)}
    if coroutine.status(tasks[task_id].co) == 'dead' then
        if not is_special_task(task_id) then
            Queue.push(output, {task_id=task_id, result=r})
        end
        tasks[task_id] = nil
        return true
    end
    if r[1] then tasks[task_id].exp = r[2] end
    return false
end

local function make_task(task_id, f, ...)
    tasks[task_id] = {co=coroutine.create(f)}
    return inner_resume(task_id, ...)
end

local function resume_task(task_id, event, ...)
    local exp = tasks[task_id].exp
    if exp ~= nil and event ~= exp then return false end
    return inner_resume(task_id, event, ...)
end

local function event_queue(task_id, event)
    while true do
        local estruct = {os.pullEvent(event)}
        Queue.push(output, {task_id=task_id, result=estruct})
    end
end

local function fetch_fn()
    local r = http.post(url..'start/'..os.getComputerID()..'/'..args[1]..'/')
    if (r == nil or r.getResponseCode() ~= 200) then
        print('Failed to start program '..args[1])
        return
    end
    while true do
        r = http.post(url..'gettask/'..os.getComputerID()..'/', answer)
        if (r == nil or r.getResponseCode() ~= 200) then
            print('Connection broken')
            return
        end
        local cmd = r.readAll()
        if cmd == 'END' then
            break
        elseif cmd ~= 'NOOP' then
            local cmd, text = string_split(cmd)
            if cmd == 'TASK' then
                local task_id, text = string_split(text)
                local f = loadstring(text)
                setfenv(f, genv)
                make_task(task_id, f)
            elseif cmd == 'STARTQUEUE' then
                local task_id, text = string_split(text)
                make_task(task_id, event_queue, task_id, text)
            elseif cmd == 'STOPQUEUE' then
                tasks[text] = nil
            end
        end
    end
end

local function send_fn()
    while true do
        local r = Queue.pop(output)
        if r == nil then break end
        local answer = textutils.serializeJSON(r.result)
        http.post(url..'taskresult/'..os.getComputerID()..'/'..r.task_id..'/', answer)
    end
end

if make_task('_fetch', fetch_fn) then return end

while true do
    local event, p1, p2, p3, p4, p5 = os.pullEvent()
    if resume_task('_fetch', event, p1, p2, p3, p4, p5) then break end

    -- Use of http API in user code is explicitly disallowed
    if event ~= 'http_success' and event ~= 'http_failure' then
        local local_task_ids = {}
        for task_id in pairs(tasks) do
            local_task_ids[task_id] = true
        end
        for task_id in pairs(local_task_ids) do
            if not is_special_task(task_id) then
                resume_task(task_id, event, p1, p2, p3, p4, p5)
            end
        end
    end

    if tasks['_send'] ~= nil then
        resume_task('_send', event, p1, p2, p3, p4, p5)
    else
        if Queue.length(output) > 0 then make_task('_send', send_fn) end
    end
end
