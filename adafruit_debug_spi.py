# The MIT License (MIT)
#
# Copyright (c) 2019 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_debug_spi`
================================================================================

Wrapper library for debugging SPI.


* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Debug_SPI.git"


class DebugSPI:
    """
    Wrapper library for debugging SPI.

    This library wraps a SPI object and prints buffers before writes and after reads.

    See the SPI documentation for detailed documentation on the methods in this class.

    :param spi: An initialized SPI object to debug.
    """
    def __init__(self, spi):
        self._spi = spi

    def __enter__(self):
        """
        No-op used in Context Managers.
        """
        return self._spi.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Automatically deinitialises the hardware on context exit.
        """
        return self._spi.__exit__(exc_type, exc_val, exc_tb)

    def deinit(self):
        """
        Turn off the SPI bus.
        """
        return self._spi.deinit()

    def configure(self, *args, baudrate=10000, polarity=0, phase=0, bits=8):
        """
        Configures the SPI bus. The SPI object must be locked.

        :param int baudrate: the desired clock rate in Hertz. The actual clock rate may be higher
                             or lower due to the granularity of available clock settings. Check the
                             ``frequency`` attribute for the actual clock rate.
        :param int polarity: the base state of the clock line (0 or 1)
        :param int phase: the edge of the clock that data is captured. First (0) or second (1).
                          Rising or falling depends on clock polarity.
        :param int bits: the number of bits per word
        """
        return self._spi.configure(*args, baudrate=baudrate, polarity=polarity, phase=phase,
                                   bits=bits)

    def try_lock(self):
        """
        Attempts to grab the SPI lock. Returns True on success.

        :return: True when lock has been grabbed
        :rtype: bool
        """
        return self._spi.try_lock()

    def unlock(self):
        """
        Releases the SPI lock.
        """
        return self._spi.unlock()

    def write(self, buffer, *args, start=0, end=None):
        """
        Debug version of ``write`` that prints the buffer before sending.

        :param bytearray buffer: Write out the data in this buffer
        :param int start: Start of the slice of ``buffer`` to write out: ``buffer[start:end]``
        :param int end: End of the slice; this index is not included. Defaults to ``len(buffer)``
        """
        self._spi.write(buffer, *args, start=start, end=end)
        print("spi.write:", [hex(i) for i in buffer])

    def readinto(self, buffer, *args, start=0, end=None, write_value=0):
        """
        Debug version of ``read_into`` that prints the buffer before reading.

        :param bytearray buffer: Read data into this buffer
        :param int start: Start of the slice of ``buffer`` to read into: ``buffer[start:end]``
        :param int end: End of the slice; this index is not included. Defaults to ``len(buffer)``
        :param int write_value: Value to write while reading. (Usually ignored.)
        """
        self._spi.readinto(buffer, *args, start=start, end=end, write_value=write_value)
        print("spi.readinto:", [hex(i) for i in buffer])

    def write_readinto(self, buffer_out, buffer_in, *args, out_start=0, out_end=None, in_start=0,
                       in_end=None):
        """
        Debug version of ``write_readinto`` that prints the ``buffer_out`` before writing and the
        ``buffer_in`` after reading.

        :param bytearray buffer_out: Write out the data in this buffer
        :param bytearray buffer_in: Read data into this buffer
        :param int out_start: Start of the slice of buffer_out to write out:
                              ``buffer_out[out_start:out_end]``
        :param int out_end: End of the slice; this index is not included. Defaults to
                            ``len(buffer_out)``
        :param int in_start: Start of the slice of ``buffer_in`` to read into:
                             ``buffer_in[in_start:in_end]``
        :param int in_end: End of the slice; this index is not included. Defaults to
                           ``len(buffer_in)``
        """
        print("spi.write_readinto.buffer_out:", [hex(i) for i in buffer_out[out_start:out_end]])
        self._spi.write_readinto(buffer_out, buffer_in, *args, out_start=out_start, out_end=out_end,
                                 in_start=in_start, in_end=in_end)
        print("spi.write_readinto.buffer_in:", [hex(i) for i in buffer_in[in_start:in_end]])

    def frequency(self):
        """
        The actual SPI bus frequency. This may not match the frequency requested due to internal
        limitations.
        """
        return self._spi.frequency
