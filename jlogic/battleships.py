import re
from jlogic.puzzle import RectanglePuzzle, RectangleField, Group

__ALL__ = ['Battleships']


class Battleships(RectanglePuzzle):

    VALUE_EMPTY  = '.'
    VALUE_HIT    = 'x'
    VALUE_NO_HIT = '-'

    def __init__(self, data:str=None):
        super().__init__()
        if data is not None:
            self.load_data(data)

    def _parse_value(self, value:str) -> str:
        if value not in (self.VALUE_EMPTY, self.VALUE_HIT, self.VALUE_NO_HIT):
            raise ValueError('value "{}" is not valid'.format(value))
        return value

    def _parse_index(self, index_value:str) -> int:
        try:
            index_value = int(index_value)
        except Exception as _:
            raise ValueError('index value "{}" is not valid'.format(
                    index_value))
        return index_value

    def load_data(self, data: str):
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
        for row in self.row_values:
            for val in row:
                self.add_field(RectangleField(val))

    def set_groups(self):
        # add row groups
        for i_row in range(self.height):
            fields = []
            for i_col in range(self.width):
                field = self.get_field(i_row, i_col)
                fields.append(field)

            def check_sum_hit(fields:list[Field]) -> bool:
                sum_hit = sum([1 for f in fields if f.value == self.VALUE_HIT])
                return sum_hit == self.row_index_W[i_row]

            restrictions = [sum_hit]
            self.add_group(Group(fields, restrictions))

        # add column groups TODO
