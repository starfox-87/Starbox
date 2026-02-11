# MITM Module Framework

class MITMModule:
    def __init__(self):
        pass

    def execute(self, request):
        """Override this method in derived classes to implement functionality."""
        return request


class LoggerModule(MITMModule):
    def execute(self, request):
        print(f"Logging request: {request}")
        return super().execute(request)


class ModifierModule(MITMModule):
    def __init__(self, modify_func):
        super().__init__()
        self.modify_func = modify_func

    def execute(self, request):
        modified_request = self.modify_func(request)
        return super().execute(modified_request)


class MITM:
    def __init__(self):
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)
        return self  # Allows chainability

    def process(self, request):
        for module in self.modules:
            request = module.execute(request)
        return request


# Example usage
if __name__ == '__main__':
    mitm = MITM()
    mitm.add_module(LoggerModule()).add_module(ModifierModule(lambda req: req + " [modified]"))
    final_request = mitm.process("GET /")
    print(f"Final request: {final_request}")
