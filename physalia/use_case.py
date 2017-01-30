from energy_profiler import monitor_energy


class AndroidUseCase(object):
    """Implementation an Android use case

    Attributes:
        prepare     method to run before interaction
        interact    method with Android interaction
    """
    def __init__(self, prepare, run):
        self.prepare = prepare
        self.run = run

    def run(self):
        self.prepare()
        monitor_energy(self.run)()
