import re
from jlogic.puzzle import RectanglePuzzle, RectangleField

__ALL__ = ['Battleships']


class Battleships(RectanglePuzzle):
    """
    Battleships is a puzzle game class that inherits from RectanglePuzzle.

    It represents a Battleships puzzle grid and provides methods to load and
    validate puzzle data, as well as set up the puzzle fields, groups and
    restrictions.
    """

    VALUE_EMPTY  = '.'
    VALUE_HIT    = 'x'
    VALUE_NO_HIT = '-'

    def __init__(self, data:str=None):
        """
        Initializes the instance of the class.

        Args:
            data (str, optional): A string containing data to initialize the
                instance. Defaults to None.
        """
        super().__init__()
        if data is not None:
            self.load_data(data)

    def _parse_value(self, value:str) -> str:
        """
        Parses and validates a given value for the Battleships puzzle.

        This method checks if the provided value is one of the allowed values
        for the puzzle, which are:
        - VALUE_EMPTY ('.')
        - VALUE_HIT ('x')
        - VALUE_NO_HIT ('-')

        If the value is valid, it returns the value. Otherwise, it raises a
        ValueError indicating that the value is not valid.

        Parameters:
        value (str): The value to be parsed and validated.

        Returns:
        str: The validated value.

        Raises:
        ValueError: If the value is not one of the allowed values.
        """
        if value not in (self.VALUE_EMPTY, self.VALUE_HIT, self.VALUE_NO_HIT):
            raise ValueError('value "{}" is not valid'.format(value))
        return value

    def _parse_index(self, index_value:str) -> int:
        """
        Parses the given index value and converts it to an integer.

        Args:
            index_value (str): The index value to be parsed.

        Returns:
            int: The parsed integer value of the index.

        Raises:
            ValueError: If the index value cannot be converted to an integer.
        """
        try:
            index_value = int(index_value)
        except Exception as _:
            raise ValueError('index value "{}" is not valid'.format(
                    index_value))
        return index_value

    def load_data(self, data: str):
        """
        Loads multiline data string into puzzle.

        Args:
            data (str): Multiline string containing the puzzle data.

        Raises:
            ValueError: If any row data or row solution length does not match
                        the expected width, or if the number of rows does not
                        match the expected height.

        Example:
            data = '''
              1133102414
            3 ..x.....x.    --x----xx-
            1 ..........    --x-------
            1 ..........    --x-------
            2 .......x..    ----x--x--
            1 ..........    -------x--
            2 ..........    -x-------x
            2 ..........    -------x-x
            3 x..x......    x--x-----x
            3 ......x...    ---x--x--x
            2 ..........    ---x--x---
            '''
            load_data(data)
        """
        data = data.strip('\n')
        for irow, row in enumerate(data.split('\n')):
            if irow == 0:
                col_index = row.strip()
                self.width = len(col_index)
                self.height = len(col_index)
                self.col_index_N = [self._parse_index(i) for i in col_index]
            else:
                row_split = re.split(r"\s+", row.strip())
                if len(row_split) < 1:
                    raise ValueError('row "{}" is not valid'.format(row.strip))
                row_index = row_split[0]
                row_data = row_split[1]
                row_solution = row_split[2] if len(row_split) > 2 else None
                self.row_index_W.append(self._parse_index(row_index))
                if len(row_data) != self.width:
                    raise ValueError('length of row "{}" is not {}'.format(
                            row_data, self.width))
                else:
                    self.row_values.append([
                            self._parse_value(v) for v in row_data])
                if (row_solution is not None
                        and len(row_solution) != self.width):
                    raise ValueError(
                        'length of row solution "{}" is not {}'.format(
                            row_solution, self.width))
                elif row_solution is not None:
                    self.row_solution.append([
                            self._parse_value(v) for v in row_solution])

        if len(self.row_values) != self.height:
            raise ValueError('length of row values "{}" is not {}'.format(
                    self.row_values, self.height))
        if len(self.row_index_W) != self.height:
            raise ValueError('length of left row data "{}" is not {}'.format(
                    self.row_index_W, self.height))
        if (len(self.row_solution) > 0
                and len(self.row_solution) != self.height):
            raise ValueError('length of row solution "{}" is not {}'.format(
                    self.row_solution, self.height))

        self.init_data()

    def set_fields(self):
        """
        Initializes and sets the fields for the game board.

        This method iterates over the rows and values in `self.row_values`,
        creating a `RectangleField` for each value and adding it to the board.

        Attributes:
            self.row_values (list): A list of lists containing the values for each row.
        """
        for row in self.row_values:
            for val in row:
                self.add_field(RectangleField(val))

    def set_groups(self):
        # set rows
        pass

        # set cols
        pass

    def set_restrictions(self):
        pass
