# Pythonized ComputerCraft API

First, you need to start a server:

```bash
cd your_folder_with_programs
python -m computercraft.server
```

Current directory is the place for your amazing programs.
Server tracks files inside this directory and reloads if necessary.
You don't (always) have to restart server if you change your programs.

Create simple program named `hello.py`:

```python
async def program(api):
    await api.print('Hello world!')
```

In minecraft, open up any computer and type:

```bash
wget http://127.0.0.1:8080/ py
py hello
```

`py` is short Lua program that interacts with the server.
Argument is the name of program without `.py`.
In everything else it works exactly like native program on Lua.
`api` object contains almost everything *as is* in ComputerCraft documentation:

```python
async def program(api):
    await api.disk.eject('right')
    await api.print(await api.os.getComputerLabel())
    # ...
```

Using python coroutines allows launching commands in parallel, effectively replacing `parallel` API:

```python
async def program(api):
    # Since os.sleep is mostly waiting for events, it doesn't block execution of parallel threads
    # and this snippet takes approximately 2 seconds to complete.
    await asyncio.gather(api.os.sleep(2), api.os.sleep(2))
```

TODO:
- use current dir for programs
