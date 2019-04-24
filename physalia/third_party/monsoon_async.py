"""Logic to asynchronously profile energy using Monsoon.

This is based on the original code by Google, which is
licensed under the Apache License, Version 2.0 .
"""

from threading import Thread
from Monsoon.sampleEngine import triggers

# pylint: disable=protected-access

class MonsoonReader(Thread):
    """`Thread` subclass to asynchronously control monsoon measurements."""
    # pylint: disable=too-many-instance-attributes

    def __init__(self, monsoon_engine):
        super(MonsoonReader, self).__init__()
        self.monsoon_engine = monsoon_engine

    def prepare(self):
        """Prepare monsoon to start measuring."""
        # Make sure state is normal
        pass

    def run(self):
        """Start measuring."""
        self.monsoon_engine.startSampling(triggers.SAMPLECOUNT_INFINITE)

    def stop(self):
        """Stop measuring."""
        self.monsoon_engine._SampleEngine__stopTriggerSet = True
        self.join()
