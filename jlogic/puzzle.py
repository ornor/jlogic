from typing import Any, Callable

__ALL__ = ['Field', 'Restriction', 'Group', 'Puzzle',
           'RectangleField', 'RectanglePuzzle']


class Base(object):

    def __init__(self):
        pass


# =============================================================================


class Field(Base):

    def __init__(self, value:Any):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)


# =============================================================================


class Restriction(Base):

    def __init__(self, fn:Callable[[Any], bool]):
        super().__init__()
        self.test_fn = fn

    def __call__(self, value:Any) -> bool:
        return self.test_fn(value)


# =============================================================================


class Group(Base):

    def __init__(self, fields:list[Field],
                       restrictions:list[Restriction]=None):
        super().__init__()
        self.fields = fields if fields is not None else []
        self.restrictions = restrictions if restrictions is not None else []

    def add_restriction(self, restriction:Restriction):
        self.restrictions.append(restriction)

    def __str__(self):
        return str(self.fields)


# =============================================================================


class Puzzle(Base):

    def __init__(self):
        super().__init__()
        self.fields = []
        self.solution_fields = []
        self.groups = []

    def add_field(self, field:Field):
        self.fields.append(field)

    def add_solution_field(self, field:Field):
        self.solution_fields.append(field)

    def add_group(self, group:Group):
        self.groups.append(group)

    def load_data(self, data:str):
        # to be implemented by subclass
        pass

        self.init_data()

    def init_data(self):
        self.set_fields()
        self.set_groups()

    def set_fields(self):
        # to be implemented by subclass
        pass

    def set_groups(self):
        # to be implemented by subclass
        pass



# =============================================================================


class RectangleField(Field):

    def __init__(self, value:Any):
        super().__init__(value)
        # neighbouring fields
        self.N  = None
        self.NE = None
        self.E  = None
        self.SE = None
        self.S  = None
        self.SW = None
        self.W  = None
        self.NW = None


class RectanglePuzzle(Puzzle):

    def __init__(self):
        super().__init__()
        self.width = 0
        self.height = 0

        self.row_values = []
        self.row_index_W = []
        self.row_index_E = []
        self.col_index_N = []
        self.col_index_S = []
        self.row_solution = []

    def get_field(self, i_row:int, i_col:int):
        if i_row * self.width + i_col >= len(self.fields):
            raise IndexError('row index "{}" out of range'.format(i_row))
        if i_col >= self.width:
            raise IndexError('col index "{}" out of range'.format(i_col))
        return self.fields[i_row * self.width + i_col]
