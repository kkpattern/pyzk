"""
Distribution related classes and function.
"""
import sys


def output_sorted(distribution, reverse=True, stream=sys.stdout):
    """
    Given a C{dict} in which the key is the item and value is the count of
    the item, output the distribution in sorted format.

    @type distribution: C{dict}
    @param distribution: The distribution of items.

    @type reverse: C{bool}
    @param reverse: If True the value will be reverse sorted.

    @param stream: A file-like object into which the output is wrote.
    """
    for value in sorted(distribution, reverse=reverse):
        for i in range(distribution[value]):
            stream.write("{0}\n".format(value))


def output_unique(distribution, reverse=True, stream=sys.stdout):
    """
    Given a C{dict} in which the key is the item and value is the count of
    the item, output the distribution in unique format.

    @type distribution: C{dict}
    @param distribution: The distribution of items.

    @type reverse: C{bool}
    @param reverse: If True the value will be reverse unique.

    @param stream: A file-like object into which the output is wrote.
    """
    for value in sorted(distribution, reverse=reverse):
        stream.write("{0} {1}\n".format(value, distribution[value]))


class Distribution(object):
    """
    Manage data distribution, output the distribution in sorted or unique
    format.
    """
    def __init__(self):
        self._distribution = {}

    def __str__(self):
        """
        Present the distribution in str.
        """
        return str(self._distribution)

    def __iter__(self):
        """
        Iterate the values.
        """
        for value in self._distribution:
            yield value

    def __getitem__(self, value):
        """
        Get the count of value.
        """
        return self._distribution[value]

    def __setitem__(self, value, count):
        """
        Set the count of value.
        """
        self._distribution[value] = count

    def add(self, value, count):
        """
        Add value.

        @param value: The value to add.

        @param count: How many values to add.
        """
        try:
            self._distribution[value] += count
        except KeyError:
            self._distribution[value] = count

    def output_sorted(self, reverse=True, stream=sys.stdout):
        """
        Output the data distribution in sorted format.
        
        @type reverse: C{bool}
        @param reverse: If True the value will be reverse sorted.

        @param stream: A file-like object into which the output is wrote.
        """
        output_sorted(self._distribution, reverse, stream)

    def output_unique(self, reverse=False, stream=sys.stdout):
        """
        Output the data distribution in unique format.

        @type reverse: C{bool}
        @param reverse: If True the value will be reverse sorted.

        @param stream: A file-like object into which the output is wrote.
        """
        output_unique(self._distribution, reverse, stream)
