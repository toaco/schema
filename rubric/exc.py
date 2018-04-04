class ValidateError(Exception):
    def __eq__(self, ins):
        return self.args == ins.args
