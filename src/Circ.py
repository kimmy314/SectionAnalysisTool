from Shape import Shape
from CircSegAnalysis import CircSegAnalysis as CSA
__author__ = 'Kim Nguyen'
class Circ(Shape):
    ''' Circle shape '''
    def __init__(self, section):
        super(Circ, self).__init__(section);

    def draw(self, canvas, inToPix, origin):
        ''' draws a circle based on the section details '''
        if (not isinstance(self.section, CSA)):
            raise ValueError('Invalid Circle');

        x = self.section.x;
        y = self.section.y;
        dim1 = self.section.dim1;
        dim2 = self.section.dim2;
        orient = self.section._orientD;
        alpha = self.section._alphaD;
        xo = origin[0];
        yo = origin[1];
        xcg = self.section.xcg;
        ycg = self.section.ycg;
        label = self.section.name;
        x0, y0 = self.inLocToPix(inToPix, xo, yo, x - dim1, y + dim1);
        x1, y1 = self.inLocToPix(inToPix, xo, yo, x + dim1, y - dim1);
        x2, y2 = self.inLocToPix(inToPix, xo, yo, x - dim2, y + dim2);
        x3, y3 = self.inLocToPix(inToPix, xo, yo, x + dim2, y - dim2);
        if (alpha != 360):
            canvas.create_arc(x0, y0, x1, y1,
                              start = int(orient + 360 - alpha / 2),
                              extent = int(alpha),
                              fill ='white',
                              outline = 'grey');
            canvas.create_arc(x2, y2, x3, y3,
                              start = int(orient + 360 - alpha / 2),
                              extent = int(alpha),
                              fill ='grey',
                              outline = 'grey');
        else:
            canvas.create_oval(x0, y0, x1, y1,
                               fill ='white',
                               outline = 'grey');
            canvas.create_oval(x2, y2, x3, y3,
                               fill ='grey',
                               outline = 'grey');
                              
        xt, yt = self.inLocToPix(inToPix, xo, yo, xcg, ycg);
        canvas.create_text(xt, yt, text = label, fill = 'blue');