from PartialAnalysis import PartialAnalysis;
from colour import Color as Color
__author__ = 'Kim Nguyen'
class Shape:
    ''' shape helps draws on the canvas and colors things '''
    def __init__(self, section):
        self._section = None;
        self.section = section;

    @property
    def section(self):
        ''' section '''
        return self._section;

    @section.setter
    def section(self, value):
        ''' the section to draw if one '''
        if isinstance(value, PartialAnalysis):
                self._section = value;
        else:
            raise ValueError('Invalid section');

    def inLocToPix(self, inToPix, xo, yo, x, y):
        ''' converts an x, y coordinate in units to pixel '''
        return int(xo + x * inToPix), int(yo - y * inToPix);

    def draw(self, canvas, inToPix, origin):
        ''' draws on the canvas '''
        raise NotImplementedError( 'Should have implemented this' );

    def point(self, canvas, x, y, stress, minS, maxS):
        ''' points are used only for creating stress fields '''
        if (maxS - minS < 1):
            maxS = 1;
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # [RED, GREEN, BLUE]
        color = self.convert_to_rgb(self, stress, minS, maxS, colors);
        item = canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1,
                                fill = self.rgb_to_hex(color),
                                outline = self.rgb_to_hex(color));
        return item

    def convert_to_rgb(self, val, minval, maxval, colors):
        ''' gets rbg based on min, max and cur val '''
        max_index = len(colors)-1
        v = float(val-minval) / float(maxval-minval) * max_index
        i1, i2 = int(v), min(int(v)+1, max_index)
        (r1, g1, b1), (r2, g2, b2) = colors[i1], colors[i2]
        f = v - i1
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

    def rgb_to_hex(rgb_tuple):
        ''' converts rbg to hex based on Color '''
        color = Color(red = rgb_tuple[0]*1.0/255)
        color.green = rgb_tuple[1]*1.0/255
        color.blue = rgb_tuple[2]*1.0/255
        return color.hex