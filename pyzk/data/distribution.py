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


def output_unique(distribution, reverse=True,
                  stream=sys.stdout, separator=' '):
    """
    Given a C{dict} in which the key is the item and value is the count of
    the item, output the distribution in unique format.

    @type distribution: C{dict}
    @param distribution: The distribution of items.

    @type reverse: C{bool}
    @param reverse: If True the value will be reverse unique.

    @param stream: A file-like object into which the output is wrote.

    @type separator: C{str}
    @param separator: The separator to use.
    """
    for value in sorted(distribution, reverse=reverse):
        stream.write(
            "{0}{1}{2}\n".format(value, separator, distribution[value]))


def export_sorted(distribution, reverse=True):
    """
    Export distribution in sorted format in a C{list}.

    @param distribution: A C{dict}-like object.

    @type reverse: C{bool}
    @param reverse: If True the value will be reverse sorted.
    """
    result = []
    for value in sorted(distribution, reverse=reverse):
        for i in range(distribution[value]):
            result.append(value)
    return result


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
            self[value] += count
        except KeyError:
            self[value] = count

    def load(self, stream=sys.stdin, value_parser=str, count_parser=int,
             separator=None):
        """
        Load data from a file-like object. The format of the input should be:
          value count
          or
          value

        @param stream: A file-like object.

        @type value_parser: C{callable}
        @param value_parser: Parse the value from str.

        @type count_parser: C{callable}
        @param count_parser: Parse the count from str.

        @type separator: C{str}
        @param separator: The separator used in input stream.
        """
        for line_number, line in enumerate(stream, start=1):
            striped_line = line.strip()
            if striped_line:
              data = striped_line.split(separator)
              if len(data) > 2:
                  raise ValueError('Bad input at line {0}: "{1}"'.format(
                      line_number, striped_line))
              else:
                  try:
                      value = value_parser(data[0])
                  except ValueError:
                      raise ValueError('Bad input at line {0}: "{1}"'.format(
                          line_number, striped_line))
                  try:
                      count = count_parser(data[1])
                  except IndexError:
                      count = 1
                  except ValueError:
                      raise ValueError('Bad input at line {0}: "{1}"'.format(
                          line_number, striped_line))
                  self.add(value, count)

    def export(self):
        """
        Export the distribution in a C{dict}.
        """
        return dict(self._distribution)

    def export_sorted(self):
        """
        Export distribution in sorted format in a C{list}.
        """
        return export_sorted(self._distribution)

    def output_sorted(self, reverse=True, stream=sys.stdout):
        """
        Output the data distribution in sorted format.
        
        @type reverse: C{bool}
        @param reverse: If True the value will be reverse sorted.

        @param stream: A file-like object into which the output is wrote.
        """
        output_sorted(self._distribution, reverse, stream)

    def output_unique(self, reverse=False, stream=sys.stdout, separator=' '):
        """
        Output the data distribution in unique format.

        @type reverse: C{bool}
        @param reverse: If True the value will be reverse sorted.

        @param stream: A file-like object into which the output is wrote.

        @type separator: C{str}
        @param separator: The separator to use.
        """
        output_unique(self._distribution, reverse, stream, separator)
