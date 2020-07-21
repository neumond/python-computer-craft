local genv = getfenv()
local temp = {}
local event_sub = {}
genv.temp = temp
local url = 'http://127.0.0.1:4343/'
local proto_version = 2
local tasks = {}
local filters = {}
local ycounts = {}
local coparams = {}

local ws = http.websocket(url..'ws/')
if ws == false then
    error('unable to connect to server '..url..'ws/')
end

local serialize
do
    local function s_rec(v, tracking)
        local t = type(v)
        if v == nil then
            return 'N'
        elseif v == false then
            return 'F'
        elseif v == true then
            return 'T'
        elseif t == 'number' then
            return '\[' .. tostring(v) .. '\]'
        elseif t == 'string' then
            return string.format('<%u>', #v) .. v
        elseif t == 'table' then
            if tracking[v] ~= nil then
                error('Cannot serialize table with recursive entries', 0)
            end
            tracking[v] = true
            local r = '{'
            for k, x in pairs(v) do
                r = r .. ':' .. s_rec(k, tracking) .. s_rec(x, tracking)
            end
            return r .. '}'
        else
            error('Cannot serialize type ' .. t, 0)
        end
        local tp = type(t)
    end
    serialize = function(v) return s_rec(v, {}) end
end

function deserialize(s, idx)
    if idx == nil then idx = 1 end
    local tok = s:sub(idx, idx)
    idx = idx + 1
    if tok == '' then
        error('Unexpected end of message', 0)
    elseif tok == 'N' then
        return nil, idx
    elseif tok == 'F' then
        return false, idx
    elseif tok == 'T' then
        return true, idx
    elseif tok == '\[' then
        local newidx = s:find('\]', idx, true)
        return tonumber(s:sub(idx, newidx - 1)), newidx + 1
    elseif tok == '<' then
        local newidx = s:find('>', idx, true)
        local slen = tonumber(s:sub(idx, newidx - 1))
        if slen == 0 then
            return '', newidx + 1
        end
        return s:sub(newidx + 1, newidx + slen), newidx + slen + 1
    elseif tok == '{' then
        local r = {}
        while true do
            tok = s:sub(idx, idx)
            idx = idx + 1
            if tok == '}' then break end
            local key, value
            key, idx = deserialize(s, idx)
            value, idx = deserialize(s, idx)
            r[key] = value
        end
        return r, idx
    else
        error('Unknown token ' .. tok, 0)
    end
end

function drop_task(task_id)
    tasks[task_id] = nil
    filters[task_id] = nil
    ycounts[task_id] = nil
    coparams[task_id] = nil
end

function ws_send(action, ...)
    local m = action
    for _, v in ipairs(arg) do
        m = m .. serialize(v)
    end
    ws.send(m, true)
end

function safe_unpack(a)
    -- nil-safe
    return table.unpack(a, 1, table.maxn(a))
end

ws_send('0', proto_version, os.getComputerID(), arg)

while true do
    local event, p1, p2, p3, p4, p5 = os.pullEvent()

    if event == 'websocket_message' then
        local msg = p2
        local action = msg:sub(1, 1)
        local idx = 2

        if action == 'T' or action == 'I' then  -- new task
            -- task_id, code, params
            local task_id, code, params
            task_id, idx = deserialize(msg, idx)
            code, idx = deserialize(msg, idx)
            params, idx = deserialize(msg, idx)

            local fn, err = loadstring(code)
            if fn == nil then
                -- couldn't compile
                ws_send('T', task_id, serialize{false, err}, 0)
            else
                setfenv(fn, genv)
                if action == 'I' then
                    ws_send('T', task_id, serialize{fn(safe_unpack(params))}, 0)
                else
                    tasks[task_id] = coroutine.create(fn)
                    ycounts[task_id] = 0
                    coparams[task_id] = params
                end
            end
        elseif action == 'D' then  -- drop tasks
            while idx <= #msg do
                local task_id
                task_id, idx = deserialize(msg, idx)
                drop_task(task_id)
            end
        elseif action == 'S' or action == 'U' then  -- (un)subscribe to event
            local event
            event, idx = deserialize(msg, idx)
            if action == 'S' then
                event_sub[event] = true
            else
                event_sub[event] = nil
            end
        elseif action == 'C' then  -- close session
            local err
            err, idx = deserialize(msg, idx)
            if err ~= nil then
                io.stderr:write(err .. '\n')
            end
            break
        end
    elseif event_sub[event] == true then
        ws_send('E', event, {p1, p2, p3, p4, p5})
    end

    local del_tasks = {}
    for task_id in pairs(tasks) do
        if filters[task_id] == nil or filters[task_id] == event then
            local r
            if coparams[task_id] ~= nil then
                r = {coroutine.resume(tasks[task_id], safe_unpack(coparams[task_id]))}
                coparams[task_id] = nil
            else
                r = {coroutine.resume(tasks[task_id], event, p1, p2, p3, p4, p5)}
            end
            ycounts[task_id] = ycounts[task_id] + 1
            if coroutine.status(tasks[task_id]) == 'dead' then
                ws_send('T', task_id, serialize(r), ycounts[task_id])
                del_tasks[task_id] = true
            else
                if r[1] == true then
                    filters[task_id] = r[2]
                else
                    filters[task_id] = nil
                end
            end
        end
    end
    for task_id in pairs(del_tasks) do drop_task(task_id) end
end

ws.close()
