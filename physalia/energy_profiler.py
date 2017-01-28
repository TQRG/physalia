import click
from power_meters import EmulatedPowerMeter

power_meter = EmulatedPowerMeter()


def start():
    """starts recording energy consumption"""
    power_meter.start()
    click.secho('started energy profiling', fg='green')


def stop():
    """stops recording energy consumption"""
    energy_consumption = power_meter.stop()
    click.secho(
        'stopped energy profiling {}'.format(energy_consumption),
        fg='red'
    )


def monitor_energy(func):
    def inner(*args, **kwargs):
        start()
        func(*args, **kwargs)
        stop()
    return inner
