local _py = {
    cc_url = '__cc_url__',
    oc_host = '__oc_host__',
    oc_port = __oc_port__,
    proto_version = 5,
    event_sub = {},
    tasks = {},
    filters = {},
    coparams = {},
    modules = {},
    mcache = {},
}

if type(getfenv) == 'function' then
    _py.genv = getfenv()
elseif type(_ENV) == 'table' then
    _py.genv = _ENV
elseif type(_G) == 'table' then
    _py.genv = _G  -- TODO: necessary?
else
    error('E001: Can\'t get environment')
end
-- TODO: rename temp to _pytemp
_py.genv.temp = {}

if type(loadstring) == 'function' then
    -- 5.1: prefer loadstring
    function _py.loadstring(source)
        local r, err = loadstring(source)
        if r ~= nil then setfenv(r, _py.genv) end
        return r, err
    end
else
    -- 5.2+: load can deal with strings as well
    function _py.loadstring(source)
        return load(source, nil, nil, _py.genv)
    end
end

if type(require) == 'function' then
    function _py.try_import(module, fn_name, save_as)
        local r, m = pcall(function() return require(module) end)
        if (not r
            or type(m) ~= 'table'
            or type(m[fn_name]) ~= 'function') then return false end
        if save_as == nil then
            _py._impfn = m[fn_name]
        else
            _py[save_as] = m[fn_name]
        end
        return true
    end
else
    function _py.try_import() return false end
end

function _py.loadmethod(code)
    -- R:module.method  (needs require(module))
    -- M:module.method
    -- E:code  (eval)
    -- code  (eval without cache)
    if _py.mcache[code] ~= nil then return _py.mcache[code] end

    local mod, modname
    while true do
        local _, _, rmod, mcode = string.find(code, '^R:(%a%w*):(.*)$')
        if rmod == nil then break end
        if _py.modules[rmod] == nil then
            local r, v = pcall(require, rmod)
            if not r then return nil, 'module not found' end
            _py.modules[rmod] = v
        end
        mod, code = _py.modules[rmod], mcode
    end
    do
        local _, _, rmod, mcode = string.find(code, '^G:(%a%w*):(.*)$')
        if rmod ~= nil then
            mod, code = _py.genv[rmod], mcode
            if mod == nil then return nil, 'module not found' end
        end
    end

    local fn
    do
        local _, _, meth = string.find(code, '^M:(%a%w*)$')
        if meth ~= nil then
            fn = mod[meth]
            if fn == nil then return nil, 'method not found' end
        else
            local err
            fn, err = _py.loadstring(code)
            if not fn then return nil, err end
        end
    end
    _py.mcache[code] = fn
    return fn
end

if type(os) == 'table' and type(os.pullEvent) == 'function' then
    _py.pullEvent = os.pullEvent  -- computercraft
elseif _py.try_import('event', 'pull') then
    _py.pullEvent = _py._impfn  -- opencomputers
else
    error('E002: Can\'t detect pullEvent method')
end

if type(arg) == 'table' then
    _py.argv = arg  -- TODO: remove?
else
    _py.argv = {...}
end

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
            return '[' .. tostring(v) .. ']'
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
    end
    _py.serialize = function(v) return s_rec(v, {}) end
end

function _py.create_stream(s, idx)
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

function _py.deserialize(stream)
    local tok = stream.fixed(1)
    if tok == 'N' then
        return nil
    elseif tok == 'F' then
        return false
    elseif tok == 'T' then
        return true
    elseif tok == '[' then
        return tonumber(stream.tostop(']'))
    elseif tok == '<' then
        local slen = tonumber(stream.tostop('>'))
        return stream.fixed(slen)
    elseif tok == 'E' then
        -- same as string (<), but intended for evaluation
        local slen = tonumber(stream.tostop('>'))
        local fn = assert(_py.loadstring(stream.fixed(slen)))
        return fn()
    elseif tok == '{' then
        local r = {}
        while true do
            tok = stream.fixed(1)
            if tok == ':' then
                local key = _py.deserialize(stream)
                r[key] = _py.deserialize(stream)
            else break end
        end
        return r
    else
        error('Unknown token ' .. tok)
    end
end

function _py.drop_task(task_id)
    _py.tasks[task_id] = nil
    _py.filters[task_id] = nil
    _py.coparams[task_id] = nil
end

-- nil-safe
if type(table.maxn) == 'function' then
    function _py.safe_unpack(a)
        return table.unpack(a, 1, table.maxn(a))
    end
else
    function _py.safe_unpack(a)
        local maxn = #a
        -- TODO: better solution?
        for k in pairs(a) do
            if type(k) == 'number' and k > maxn then maxn = k end
        end
        return table.unpack(a, 1, maxn)
    end
end

if type(http) == 'table' and type(http.websocket) == 'function' then
    function _py.start_connection()
        local ws = http.websocket(_py.cc_url)
        if not ws then
            error('Unable to connect to server ' .. _py.cc_url)
        end
        _py.ws = {
            send = function(m) return ws.send(m, true) end,
            close = function() ws.close() end,
        }
    end
elseif _py.try_import('internet', 'socket', 'oc_connect') then
    function _py.start_connection()
        local s = _py.oc_connect(_py.oc_host, _py.oc_port)
        if not s or s.socket.finishConnect() == nil then
            error('Unable to connect to server ' .. _py.oc_host .. ':' .. _py.oc_port)
        end
        local bit32 = require('bit32')
        local buf = ''
        _py.ws = {
            send = function(frame)
                local z = #frame
                s.socket.write(string.char(
                    bit32.band(bit32.rshift(z, 16), 255),
                    bit32.band(bit32.rshift(z, 8), 255),
                    bit32.band(z, 255)
                ))
                s.socket.write(frame)
            end,
            close = function() s.socket.close() end,
            read_pending = function(frame_callback)
                local inc = s.socket.read()
                if inc == nil then
                    return true, 'Connection with server has been closed'
                end
                buf = buf .. inc
                while #buf >= 3 do
                    local frame_size = (
                        bit32.lshift(string.byte(buf, 1), 16)
                        + bit32.lshift(string.byte(buf, 2), 8)
                        + string.byte(buf, 3))
                    if #buf < frame_size + 3 then break end
                    if frame_callback(string.sub(buf, 4, 3 + frame_size)) then
                        return true, nil
                    end
                    buf = string.sub(buf, 4 + frame_size)
                end
                return false
            end,
        }
    end
else
    error('E003: Can\'t detect connection method')
end

function _py.ws_send(action, ...)
    local m = action
    for _, v in ipairs({...}) do
        m = m .. _py.serialize(v)
    end
    _py.ws.send(m)
end

function _py.exec_python_directive(dstring)
    local msg = _py.create_stream(dstring)
    local action = msg.fixed(1)

    if action == 'T' or action == 'I' then  -- new task
        local task_id = _py.deserialize(msg)
        local code = _py.deserialize(msg)
        local params = _py.deserialize(msg)

        local fn, err = _py.loadmethod(code)
        if fn == nil then
            -- couldn't compile
            _py.ws_send('T', task_id, _py.serialize{false, err})
        else
            if action == 'I' then
                _py.ws_send('T', task_id, _py.serialize{fn(_py.safe_unpack(params))})
            else
                _py.tasks[task_id] = coroutine.create(fn)
                _py.coparams[task_id] = params
            end
        end
    elseif action == 'D' then  -- drop tasks
        while not msg.isend() do
            _py.drop_task(_py.deserialize(msg))
        end
    elseif action == 'S' or action == 'U' then  -- (un)subscribe to event
        local event = _py.deserialize(msg)
        if action == 'S' then
            _py.event_sub[event] = true
        else
            _py.event_sub[event] = nil
        end
    elseif action == 'C' then  -- close session
        local err = _py.deserialize(msg)
        if err ~= nil then
            io.stderr:write(err .. '\n')
        end
        return true
    end
end

function _py.resume_coros(event, p1, p2, p3, p4, p5)
    local del_tasks = {}
    for task_id in pairs(_py.tasks) do
        if _py.filters[task_id] == nil or _py.filters[task_id] == event then
            local r
            if _py.coparams[task_id] ~= nil then
                r = {coroutine.resume(
                    _py.tasks[task_id],
                    _py.safe_unpack(_py.coparams[task_id]))}
                _py.coparams[task_id] = nil
            else
                r = {coroutine.resume(
                    _py.tasks[task_id],
                    event, p1, p2, p3, p4, p5)}
            end
            if coroutine.status(_py.tasks[task_id]) == 'dead' then
                _py.ws_send('T', task_id, _py.serialize(r))
                del_tasks[task_id] = true
            else
                if r[1] == true then
                    _py.filters[task_id] = r[2]
                else
                    _py.filters[task_id] = nil
                end
            end
        end
    end
    for task_id in pairs(del_tasks) do _py.drop_task(task_id) end
end

if type(fs) == 'table' and type(fs.combine) == 'function' then
    function _py.start_program(name)
        local path = fs.combine(shell.dir(), name)
        if not fs.exists(path) then return nil end
        if fs.isDir(path) then return nil end
        local f = fs.open(path, 'r')
        local code = f.readAll()
        f.close()
        return path, code
    end
else
    function _py.start_program(name)
        local filesystem = require('filesystem')
        local shell = require('shell')
        local path = filesystem.concat(shell.getWorkingDirectory(), name)
        if not filesystem.exists(path) then return nil end
        if filesystem.isDirectory(path) then return nil end
        local f = io.open(path, 'rb')
        local code = f:read('*a')
        f:close()
        return path, code
    end
end

_py.start_connection()
do
    local path, code = nil, nil
    if _py.argv[1] ~= nil then
        path, code = _py.start_program(_py.argv[1])
        if path == nil then error('Program not found') end
    end
    _py.ws_send('0', _py.proto_version, _py.argv, path, code)
end
while true do
    local event, p1, p2, p3, p4, p5 = _py.pullEvent()
    if event == 'websocket_message' then
        -- TODO: filter by address
        if _py.exec_python_directive(p2) then break end
    elseif event == 'websocket_closed' then
        -- TODO: filter by address
        error('Connection with server has been closed')
    elseif event == 'internet_ready' then
        -- TODO: filter by address
        local must_exit, err = _py.ws.read_pending(_py.exec_python_directive)
        if must_exit then
            if err == nil then break else error(err) end
        end
    elseif _py.event_sub[event] == true then
        _py.ws_send('E', event, {p1, p2, p3, p4, p5})
    end
    _py.resume_coros(event, p1, p2, p3, p4, p5)
end
_py.ws.close()
