"""Logic to asynchronously profile energy using Monsoon.

This is based on the original code by Google.
"""
import fcntl
import logging
import os
import select
import struct
import sys
import time
import timeout_decorator
import collections
from threading import Event
from monsoon import MonsoonData

PLEASE_STOP = Event()

def take_samples(self, sample_hz, sample_offset=0, live=False):
    """Take samples of the current value supplied by monsoon.

    This is the actual measurement for power consumption. This function
    blocks until the number of samples requested has been fulfilled.

    Args:
        self: A physalia.third_party.monsoon.Monsoon object.
        hz: Number of points to take for every second.
        offset: The number of initial data points to discard in MonsoonData
            calculations. sample_num is extended by offset to compensate.
        live: Print each sample in console as measurement goes on.

    Returns:
        A MonsoonData object representing the data obtained in this
        sampling. None if sampling is unsuccessful.
    """
    sys.stdout.flush()
    voltage = self.mon.GetVoltage()
    self.log.info("Taking samples at %dhz, voltage %.2fv.",
                  sample_hz, voltage)
    # Make sure state is normal
    self.mon.StopDataCollection()
    status = self.mon.GetStatus()
    native_hz = status["sampleRate"] * 1000

    # Collect and average samples as specified
    self.mon.StartDataCollection()

    # In case sample_hz doesn't divide native_hz exactly, use this
    # invariant: 'offset' = (consumed samples) * sample_hz -
    # (emitted samples) * native_hz
    # This is the error accumulator in a variation of Bresenham's
    # algorithm.
    emitted = offset = 0
    collected = []
    # past n samples for rolling average
    history_deque = collections.deque()
    current_values = []
    timestamps = []

    try:
        last_flush = time.time()
        while not PLEASE_STOP.is_set():
            # The number of raw samples to consume before emitting the next
            # output
            need = int((native_hz - offset + sample_hz - 1) / sample_hz)
            if need > len(collected):  # still need more input samples
                samples = self.mon.CollectData()
                if not samples:
                    break
                collected.extend(samples)
            else:
                # Have enough data, generate output samples.
                # Adjust for consuming 'need' input samples.
                offset += need * sample_hz
                # maybe multiple, if sample_hz > native_hz
                while offset >= native_hz:
                    # TODO(angli): Optimize "collected" operations.
                    this_sample = sum(collected[:need]) / need
                    this_time = int(time.time())
                    timestamps.append(this_time)
                    if live:
                        self.log.info("%s %s", this_time, this_sample)
                    current_values.append(this_sample)
                    sys.stdout.flush()
                    offset -= native_hz
                    emitted += 1  # adjust for emitting 1 output sample
                collected = collected[need:]
                now = time.time()
                if now - last_flush >= 0.99:  # flush every second
                    sys.stdout.flush()
                    last_flush = now
    except Exception as e:
        pass
    self.mon.StopDataCollection()
    try:
        return MonsoonData(current_values, timestamps, sample_hz, voltage, offset=sample_offset)
    except:
        return None

def stop_taking_samples():
    PLEASE_STOP.set()