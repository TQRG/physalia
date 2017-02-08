"""Command Line Interface for Physalia.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python cli.py "python ui_interaction.py"
"""

# pylint: disable=no-value-for-parameter
# pylint: disable=missing-docstring

import subprocess
import click
from physalia.energy_profiler import AndroidUseCase


@click.command()
@click.argument('runner')
def tool(runner):
    """Run the tool with CLI arguments."""
    def prepare():
        pass

    def run():
        subprocess.check_output(runner, shell=True)
    use_case = AndroidUseCase('login', 'com.test.app', '12', prepare, run)
    use_case.profile(verbose=True)


if __name__ == '__main__':
    tool()
