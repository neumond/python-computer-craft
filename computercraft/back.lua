local genv = getfenv()
local temp = {}
local event_sub = {}
genv.temp = temp
local url = 'http://127.0.0.1:4343/'
local proto_version = 3
local tasks = {}
local filters = {}
local ycounts = {}
local coparams = {}

local ws = http.websocket(url..'ws/')
if ws == false then
    error('Unable to connect to server '..url..'ws/')
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

function create_stream(s, idx)
    if idx == nil then idx = 1 end
    return {
        getidx=function() return idx end,
        isend=function() return idx > #s end,
        fixed=function(n)
            local r = s:sub(idx, idx + n - 1)
            if #r ~= n then error('Unexpected end of stream') end
            idx = idx + n
            return r
        end,
        tostop=function(sym)
            local newidx = s:find(sym, idx, true)
            if newidx == nil then error('Unexpected end of stream') end
            local r = s:sub(idx, newidx - 1)
            idx = newidx + 1
            return r
        end,
    }
end

function deserialize(stream)
    local tok = stream.fixed(1)
    if tok == 'N' then
        return nil
    elseif tok == 'F' then
        return false
    elseif tok == 'T' then
        return true
    elseif tok == '\[' then
        return tonumber(stream.tostop('\]'))
    elseif tok == '<' then
        local slen = tonumber(stream.tostop('>'))
        return stream.fixed(slen)
    elseif tok == 'E' then
        -- same as string (<), but intended for evaluation
        local slen = tonumber(stream.tostop('>'))
        local fn = assert(loadstring(stream.fixed(slen)))
        setfenv(fn, genv)
        return fn()
    elseif tok == '{' then
        local r = {}
        while true do
            tok = stream.fixed(1)
            if tok == ':' then
                local key = deserialize(stream)
                r[key] = deserialize(stream)
            else break end
        end
        return r
    else
        error('Unknown token ' .. tok)
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
        local msg = create_stream(p2)
        local action = msg.fixed(1)

        if action == 'T' or action == 'I' then  -- new task
            local task_id = deserialize(msg)
            local code = deserialize(msg)
            local params = deserialize(msg)

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
            while not msg.isend() do
                drop_task(deserialize(msg))
            end
        elseif action == 'S' or action == 'U' then  -- (un)subscribe to event
            local event = deserialize(msg)
            if action == 'S' then
                event_sub[event] = true
            else
                event_sub[event] = nil
            end
        elseif action == 'C' then  -- close session
            local err = deserialize(msg)
            if err ~= nil then
                io.stderr:write(err .. '\n')
            end
            break
        end
    elseif event == 'websocket_closed' then
        error('Connection with server has been closed')
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
