"""Logic to asynchronously profile energy using Monsoon.

This is based on the original code by Google, which is
licensed under the Apache License, Version 2.0 .
"""

import sys
import time
from threading import Event, Thread
from physalia.third_party.monsoon import MonsoonData

# pylint: disable=protected-access

PLEASE_STOP = Event()

class MonsoonReader(Thread):
    """`Thread` subclass to asynchronously control monsoon measurements."""
    # pylint: disable=too-many-instance-attributes

    def __init__(self, monsoon, sample_hz, sample_offset=0, live=False):
        super(MonsoonReader, self).__init__()
        self._please_stop = Event()
        self.monsoon = monsoon
        self.sample_hz = sample_hz
        self.sample_offset = sample_offset
        self.live = live
        self.data = None
        self.error_flag = False
        #monsoon cache data
        self._monsoon_native_hz = None
        self._monsoon_voltage = None
        self._monsoon_status = None

    def prepare(self):
        """Prepare monsoon to start measuring."""
        sys.stdout.flush()
        self.monsoon.mon._FlushInput() # make sure old failures are gone
        self._monsoon_voltage = self.monsoon.mon.GetVoltage()
        self.monsoon.log.info(
            "Taking samples at %dhz, voltage %.2fv.",
            self.sample_hz, self._monsoon_voltage)
        # Make sure state is normal
        self.monsoon.mon.StopDataCollection()
        self._monsoon_status = self.monsoon.mon.GetStatus()
        self._monsoon_native_hz = self._monsoon_status["sampleRate"] * 1000

    def run(self):
        """Start measuring."""
        self._take_samples(
            self.monsoon,
            self.sample_hz,
            self.sample_offset,
            self.live
        )
    def stop(self):
        """Stop measuring.

        Measurements are stored in `self.data`."""
        self._please_stop.set()
        self.join()

    def _take_samples(self, monsoon, sample_hz, sample_offset=0, live=False):
        # pylint: disable=broad-except
        # pylint: disable=too-many-locals
        # We want to keep this code similar to the original from Google.
        # Although some smells were fixed, these would be too much.
        """Take samples of the current value supplied by monsoon.

        This is the actual measurement for power consumption. This function
        blocks until the number of samples requested has been fulfilled.

        Args:
            monsoon: A physalia.third_party.monsoon.Monsoon object.
            hz: Number of points to take for every second.
            offset: The number of initial data points to discard in MonsoonData
                calculations. sample_num is extended by offset to compensate.
            live: Print each sample in console as measurement goes on.

        Returns:
            A MonsoonData object representing the data obtained in this
            sampling. None if sampling is unsuccessful.
        """
        # Collect and average samples as specified
        monsoon.mon.StartDataCollection()

        # In case sample_hz doesn't divide self._monsoon_native_hz exactly, use this
        # invariant: 'offset' = (consumed samples) * sample_hz -
        # (emitted samples) * self._monsoon_native_hz
        # This is the error accumulator in a variation of Bresenham's
        # algorithm.
        emitted = offset = 0
        collected = []
        # past n samples for rolling average
        current_values = []
        timestamps = []

        try:
            last_flush = time.time()
            while not self._please_stop.is_set():
                # The number of raw samples to consume before emitting the next
                # output
                need = int((self._monsoon_native_hz - offset + sample_hz - 1) / sample_hz)
                if need > len(collected) and not self._please_stop.is_set():
                    # still need more input samples
                    samples = monsoon.mon.CollectData()
                    if not samples:
                        break
                    collected.extend(samples)
                else:
                    # Have enough data, generate output samples.
                    # Adjust for consuming 'need' input samples.
                    offset += need * sample_hz
                    # maybe multiple, if sample_hz > self._monsoon_native_hz
                    while offset >= self._monsoon_native_hz:
                        # TODO(angli): Optimize "collected" operations.
                        this_sample = sum(collected[:need]) / need
                        this_time = int(time.time())
                        timestamps.append(this_time)
                        if live:
                            monsoon.log.info("%s %s", this_time, this_sample)
                            sys.stdout.flush()
                        current_values.append(this_sample)
                        offset -= self._monsoon_native_hz
                        emitted += 1  # adjust for emitting 1 output sample
                    collected = collected[need:]
                    now = time.time()
                    if now - last_flush >= 0.99 and live:  # flush every second
                        sys.stdout.flush()
                        last_flush = now
        except Exception:
            pass
        monsoon.mon.StopDataCollection()
        try:
            self.data = MonsoonData(
                current_values,
                timestamps,
                sample_hz,
                self._monsoon_voltage,
                offset=sample_offset
            )
        except Exception:
            self.data = None
            self.error_flag = True
