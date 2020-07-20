local genv = getfenv()
local temp = {}
local event_sub = {}
genv.temp = temp
local url = 'http://127.0.0.1:4343/'
local tasks = {}
local filters = {}
local ycounts = {}
local coparams = {}

ws = http.websocket(url..'ws/')
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

local deserialize
do
    local function d_rec(s, idx)
        local tok = s:sub(idx, idx)
        idx = idx + 1
        if tok == 'N' then
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
                key, idx = d_rec(s, idx)
                value, idx = d_rec(s, idx)
                r[key] = value
            end
            return r, idx
        else
            error('Unknown token ' .. tok, 0)
        end
    end
    deserialize = function(s)
        local r = d_rec(s, 1)
        return r
    end
end

function ws_send(data)
    ws.send(serialize(data), true)
end

ws_send{
    action='run',
    computer=os.getComputerID(),
    args={...},
}

while true do
    local event, p1, p2, p3, p4, p5 = os.pullEvent()

    if event == 'websocket_message' then
        msg = deserialize(p2)
        if msg.action == 'task' then
            local fn, err = loadstring(msg.code)
            if fn == nil then
                ws_send{
                    action='task_result',
                    task_id=msg.task_id,
                    result={false, err},
                    yields=0,
                }
            else
                setfenv(fn, genv)
                if msg.immediate then
                    ws_send{
                        action='task_result',
                        task_id=msg.task_id,
                        result={fn(table.unpack(msg.params or {}))},
                        yields=0,
                    }
                else
                    tasks[msg.task_id] = coroutine.create(fn)
                    ycounts[msg.task_id] = 0
                    coparams[msg.task_id] = msg.params or {}
                end
            end
        elseif msg.action == 'drop' then
            for _, task_id in ipairs(msg.task_ids) do
                tasks[task_id] = nil
                filters[task_id] = nil
                ycounts[task_id] = nil
                coparams[task_id] = nil
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
        ws_send{
            action='event',
            event=event,
            params={p1, p2, p3, p4, p5},
        }
    end

    local del_tasks = {}
    for task_id in pairs(tasks) do
        if filters[task_id] == nil or filters[task_id] == event then
            local r
            if coparams[task_id] ~= nil then
                r = {coroutine.resume(tasks[task_id], table.unpack(coparams[task_id]))}
                coparams[task_id] = nil
            else
                r = {coroutine.resume(tasks[task_id], event, p1, p2, p3, p4, p5)}
            end
            if coroutine.status(tasks[task_id]) == 'dead' then
                ws_send{
                    action='task_result',
                    task_id=task_id,
                    result=r,
                    yields=ycounts[task_id],
                }
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
        coparams[task_id] = nil
    end
end

ws.close()
