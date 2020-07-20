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


print(serialize(nil))
assert(deserialize(serialize(nil)) == nil)


local roundtrip_vals = {
    true,
    false,
    0,
    -1,
    1,
    1e6,
    1.5,
    2.4e-9,
    tonumber('inf'),
    tonumber('-inf'),
    '',
    'string',
    '\n\r\0',
    '\0',
    '2',
}


for _, v in ipairs(roundtrip_vals) do
    print(serialize(v))
    assert(v == deserialize(serialize(v)))
end


print(serialize(tonumber('nan')))
assert(tostring(deserialize(serialize(tonumber('nan')))) == 'nan')


function areTablesEqual(a, b)
    assert(type(a) == 'table')
    assert(type(b) == 'table')
    for k, v in pairs(a) do
        if type(v) == 'table' then
            if not areTablesEqual(v, b[k]) then return false end
        else
            if b[k] ~= v then return false end
        end
    end
    for k, v in pairs(b) do
        if type(v) == 'table' then
            if not areTablesEqual(v, a[k]) then return false end
        else
            if a[k] ~= v then return false end
        end
    end
    return true
end


local roundtrip_tables = {
    {},
    {[2]=4},
    {a=1, b=true, c={}, d={x=8}},
    {1, 2, 3},
    {1},
    {'abc'},
    {[1]='a', [2]='b', [3]='c'},
    {'a', 'b', 'c'},
}


for _, v in ipairs(roundtrip_tables) do
    print(serialize(v))
    assert(areTablesEqual(v, deserialize(serialize(v))))
end

print('ALL OK')

print(serialize({true, false, 'Position is negative'}))
