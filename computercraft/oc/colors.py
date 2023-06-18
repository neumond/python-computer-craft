_index = (
    'white',
    'orange',
    'magenta',
    'lightblue',
    'yellow',
    'lime',
    'pink',
    'gray',
    'silver',
    'cyan',
    'purple',
    'blue',
    'brown',
    'green',
    'red',
    'black',
)


class Colors:
    def __getitem__(self, key: int) -> str:
        return _index[key]

    def __iter__(self):
        return enumerate(_index)

    def __len__(self):
        return len(_index)


for i, v in enumerate(_index):
    setattr(Colors, v, i)
del i, v


__replace_module__ = Colors()
