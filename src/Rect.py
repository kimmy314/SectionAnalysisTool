from Shape import Shape
from RectangleAnalysis import RectangleAnalysis as RA
__author__ = Kim Nguyen, kbnguyen@ncsu.edu
class Rect(Shape):
    ''' rectangle shape '''
    def __init__(self, section):
        super(Rect, self).__init__(section);

    def draw(self, canvas, inToPix, origin):
        ''' draws a rectangle on the canvas based on the section '''
        if (not isinstance(self.section, RA)):
            raise ValueError('Invalid rectangle');

        xo, yo = origin;
        xcg, ycg = self.section.xcg, self.section.ycg;
        label = self.section.name
        c = self.section.corners();
        x0, y0 = self.inLocToPix(inToPix, xo, yo, c[0][0], c[0][1]);
        x1, y1 = self.inLocToPix(inToPix, xo, yo, c[1][0], c[1][1]);
        x2, y2 = self.inLocToPix(inToPix, xo, yo, c[2][0], c[2][1]);
        x3, y3 = self.inLocToPix(inToPix, xo, yo, c[3][0], c[3][1]);

        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill ='white')

        xt, yt = self.inLocToPix(inToPix, xo, yo, xcg, ycg);
        canvas.create_text(xt, yt, text = label, fill = 'blue');