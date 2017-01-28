import click
from physalia.power_meters.emulated_power_meter import EmulatedPowerMeter

power_meter = EmulatedPowerMeter()


def start():
    """starts recording energy consumption"""
    power_meter.start()
    click.secho('Started energy profiling', fg='green')


def stop():
    """stops recording energy consumption"""
    energy_consumption = power_meter.stop()
    click.secho(
        'Stopped energy profiling. '
        'Energy consumption: {:.6f} Joules'.format(energy_consumption),
        fg='red'
    )


def monitor_energy(func):
    def inner(*args, **kwargs):
        start()
        func(*args, **kwargs)
        stop()
    return inner
