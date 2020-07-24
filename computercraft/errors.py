class LuaException(Exception):
    @property
    def message(self):
        if len(self.args) < 1:
            return None
        return self.args[0]
