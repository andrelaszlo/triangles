from PIL import Image, ImageDraw


class BaseTriangle:
    def __init__(self, size):
        self.size = size

    def fill(self, triangle):
        raise NotImplementedError()

    def finish(self):
        pass

    def boundary(self):
        """ Get the boundary triangle """
        w, h = self.size
        return (w/2, 0), (0, h), (w, h)


class ConsoleTriangle(BaseTriangle):
    def __init__(self, size):
        super().__init__(size)
        self._canvas = [["." for _ in range(self.size[0])]
                        for _ in range(self.size[1])]

    def fill(self, triangle):
        # Draw a triangle by filling line segments from top to bottom

        # left, right, bottom (pointing down)
        (ax, ay), (bx, by), (cx, cy) = midpoints
    
        segment_length = bx - ax
        height = int(round(cy - ay))
        offset = 0
        dx = segment_length / height
        #print(midpoints)
        for row in range(height):
            start = int(round(offset))
            end = int(round(offset+segment_length))
            y_ = int(round(row+ay))
            for x in range(start, end+1):
                #print(row, x_)
                try:
                    tri[x][y_] = "#"
                    #tri[x_][row] = 1
                except IndexError:
                    pass # whatever
            print(offset, segment_length)
            offset += dx
            segment_length -= dx

    def finish(self):
        print("\n".join("".join(row) for row in self._canvas))


class ImageTriangle(BaseTriangle):
    def __init__(self, size, filename,
                 foreground='black', background='white', scaling=2):
        self._original_size = size
        size = tuple([x*scaling for x in size])
        super().__init__(size)

        self._foreground = foreground
        self._background = background

        self._im = Image.new("RGB", size, self._foreground)
        self._draw = ImageDraw.Draw(self._im)
        self._filename = filename

        self._draw_boundary()

    def _draw_boundary(self):
        self._draw.polygon(self.boundary(), fill=self._background)

    def fill(self, triangle):
        self._draw.polygon(triangle, fill=self._foreground)

    def finish(self):
        self._im = self._im.resize(self._original_size, resample=Image.LANCZOS)
        self._im.save(self._filename)


def midpoints(points):
    """ Left, right and bottom corner of the inscribed triangle. """
    (ax, ay), (bx, by), (cx, cy) = points
    ab = bx + ((ax - bx) / 2), ay + ((by - ay) / 2)
    ac = ax + ((cx - ax) / 2), ay + ((cy - ay) / 2)
    bc = bx + ((cx - bx) / 2), by
    return ab, ac, bc


def subtriangles(points, midpoints):
    a, b, c = points
    ab, ac, bc = midpoints
    return (a, ab, ac), (ab, b, bc), (ac, bc, c)


def generate(maxdepth, triangle, boundary=None, depth=0):
    if depth == maxdepth:
        return

    w, h = triangle.size

    if boundary is None:
        boundary = triangle.boundary()

    triangle.fill(midpoints(boundary))

    for subtriangle in subtriangles(boundary, midpoints(boundary)):
        generate(maxdepth, triangle, subtriangle, depth+1)


if __name__ == '__main__':
    triangle = ImageTriangle((800, 600), 'triangles.png', scaling=3, background='purple')
    generate(7, triangle)
    triangle.finish()
