import click
from physalia.power_meters import EmulatedPowerMeter

POWER_METER = EmulatedPowerMeter()


def start():
    """starts recording energy consumption"""
    POWER_METER.start()
    click.secho('Started energy profiling', fg='green')


def stop():
    """stops recording energy consumption"""
    energy_consumption = POWER_METER.stop()
    click.secho(
        'Stopped energy profiling. '
        'Energy consumption: {:.6f} Joules'.format(energy_consumption),
        fg='red'
    )


def monitor_energy(func):
    """decorator to measure energy consumption during a routine"""
    def inner(*args, **kwargs):
        start()
        func(*args, **kwargs)
        stop()
    return inner
