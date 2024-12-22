import warnings

import shapely.wkt
from geometron.plot import plot_point, plot_line, symbols
from shapely.geometry import Point, LineString, shape, mapping


class TopoObject:
    def __init__(self, wkt, id='', kind='', show_label=True, **kwargs):
        if 'name' in kwargs.keys():
            warnings.warn('the name attribute is deprecated, use id instead...')
            id = kwargs['name']
        self._id = ''
        self.id = id
        self._kind = ''
        self.kind = kind
        self._show_label = True
        self.show_label=show_label
        self._geometry = None
        self.__geo_interface__ = {}
        self.geometry = shapely.wkt.loads(wkt)

    @property
    def show_label(self):
        return self._show_label

    @show_label.setter
    def show_label(self, val):
        assert isinstance(val, bool)
        self._show_label = val

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        assert isinstance(val, str)
        self._id = val

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, val):
        assert isinstance(val, str)
        self._kind = val.lower()

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, val):
        # assert isinstance(val, shapely.geometry.?)  # TODO: check that geometry is a valid shapely geometry
        self._geometry = val
        self.to_geo()

    def to_geo(self):
        self.__geo_interface__ = {'type': 'Feature',
                                  'properties': {'id': self.id, 'label': self.id if self.show_label else '',
                                                 'kind': self.kind, 'class': str(self.__class__).split('.')[-1][:-2]},
                                  'geometry': mapping(self.geometry)}


class TopoPoint(TopoObject):
    def __init__(self, wkt='POINT (0. 0.)', **kwargs):
        if isinstance(wkt, Point):
            wkt = wkt.wkt
        super().__init__(wkt, **kwargs)
        assert isinstance(self.geometry, Point)
        if self.kind in symbols.keys():
            self.symbol = symbols[self.kind]
        else:
            self.symbol = '.'

    def plot(self, ax=None):
        plot_point(self.geometry, ax=ax, label=self.id, kind=self.kind)


class TopoLine(TopoObject):
    def __init__(self, wkt, **kwargs):
        if isinstance(wkt, LineString):
            wkt = wkt.wkt
        super().__init__(wkt, **kwargs)
        assert isinstance(self.geometry, LineString)

    def plot(self, ax=None):
        plot_line(ax=ax, obj=shape(self.geometry), label=self.id, kind=self.kind)

