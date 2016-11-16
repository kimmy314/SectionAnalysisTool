from Shape import Shape
from PolygonAnalysis import PolygonAnalysis as PA
__author__ = 'RA029440 - Kim_Nguyen@haci.honda.com'
class Poly(Shape):
    ''' polygon shape '''
    def __init__(self, section):
        super(Poly, self).__init__(section);

    def draw(self, canvas, inToPix, origin):
        ''' draws a polygon based on the section '''
        if (not isinstance(self.section, PA)):
            raise ValueError('Invalid Polygon');

        xo = origin[0];
        yo = origin[1];
        xcg = self.section.xcg;
        ycg = self.section.ycg;
        coords = self.section.coords;
        label = self.section.name;
        points = [];
        for i in range(int(len(coords) / 2)):
            x, y = self.section.getXY(i);
            xp, yp = self.inLocToPix(inToPix, xo, yo, x, y);
            points.append(xp);
            points.append(yp);

        canvas.create_polygon(points, fill ='white')

        xt, yt = self.inLocToPix(inToPix, xo, yo, xcg, ycg);
        canvas.create_text(xt, yt, text = label, fill = 'blue');