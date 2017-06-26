"""Command Line Interface for Physalia.

Example:
        `$ python cli.py --serial 12886 -V 3.8  "sleep 5"`
"""

# pylint: disable=no-value-for-parameter
# pylint: disable=missing-docstring

import sys
import subprocess
import click
from physalia.energy_profiler import AndroidUseCase
from physalia.power_meters import MonsoonPowerMeter, EmulatedPowerMeter


@click.command()
@click.option('--count', default=1, type=click.IntRange(min=1),
              help='Number of measurement repetitions.')
@click.option('--power_meter', default='monsoon', type=click.Choice(['monsoon', 'dumb']),
              help="Which power meter to use.")
@click.option('-V', '--voltage', type=click.FLOAT,
              help="Set output voltage for Monsoon.")
@click.option('-s', '--serial', default=None, type=click.INT,
              help="Monsoon's serial number.")
@click.argument('exec_expression')
def tool(count, power_meter, voltage, serial, exec_expression):
    """Measure energy consumption while running a bash expression.

    Example:
        physalia --serial 12886 -V 3.8  "sleep 5"
    """
    physalia_power_meter = None
    if power_meter == 'monsoon':
        if not (voltage and serial):
            click.secho('Error: Monsoon requires to set voltage and serial number.', fg='red')
            sys.exit(-1)
        else:
            physalia_power_meter = MonsoonPowerMeter(voltage=voltage, serial=serial)
    elif power_meter == 'dumb':
        physalia_power_meter = EmulatedPowerMeter()

    def run(_):
        subprocess.check_output(exec_expression, shell=True)
    use_case = AndroidUseCase('physalia-cli', None, 'na', 'na', run=run)

    use_case.profile(
        power_meter=physalia_power_meter,
        verbose=True,
        retry_limit=3,
        count=count
    )


if __name__ == '__main__':
    tool()
