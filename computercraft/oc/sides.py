_index = (
    'bottom',
    'top',
    'back',
    'front',
    'right',
    'left',
)


class Sides:
    down = negy = bottom = 0
    up = posy = top = 1
    north = negz = back = 2
    south = posz = forward = front = 3
    west = negx = right = 4
    east = posx = left = 5

    def __getitem__(self, key: int) -> str:
        return _index[key]

    def __iter__(self):
        return enumerate(_index)

    def __len__(self):
        return len(_index)


__replace_module__ = Sides()
