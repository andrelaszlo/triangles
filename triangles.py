from PIL import Image, ImageDraw


class BaseTriangle:
    def __init__(self, size):
        self.size = size

    def fill(self, triangle):
        """ Mark a triangular area of the Triangle as 'filled'. """
        raise NotImplementedError()

    def finish(self):
        """ Called when rendering is completed. """
        pass

    def boundary(self):
        """ Get the boundary triangle """
        w, h = self.size
        return (w/2, 0), (0, h), (w, h)


class ConsoleTriangle(BaseTriangle):
    def __init__(self, size):
        super().__init__(size)
        w, h = size
        self._canvas = [["." for _ in range(w)] for _ in range(h)]

    def fill(self, triangle):
        # Draw a triangle by filling line segments from top to bottom

        # left, right, bottom (pointing down)
        (ax, ay), (bx, by), (cx, cy) = triangle
    
        segment_length = bx - ax
        height = int(round(cy - ay))
        offset = ax
        dx = segment_length / height
        #print(midpoints)
        print('height', height)
        for row in range(height):
            start = int(round(offset))
            end = int(round(offset+segment_length))
            y = int(round(row+ay))
            print("y", y)
            for x in range(start, end+1):
                #print(row, x_)
                try:
                    self._canvas[y][x] = "#"
                    print("put", x, y)
                    #tri[x_][row] = 1
                except IndexError:
                    pass # whatever
            offset += dx/2
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


def subtriangles(triangle):
    """ Divides the triangle described by points into three subtriangles. """
    a, b, c = triangle
    ab, ac, bc = midpoints(triangle)
    return (a, ab, ac), (ab, b, bc), (ac, bc, c)


def render(maxdepth, triangle):
    """ Renders the Sierpinski triangle """
    w, h = triangle.size

    regions = [(0, triangle.boundary())]
    for level, region in regions:
        triangle.fill(midpoints(region))
        if level < maxdepth:
            for subtriangle in subtriangles(region):
                regions.append((level+1, subtriangle))


if __name__ == '__main__':
    import sys
    triangle_type = 'image'
    if len(sys.argv) > 1 and sys.argv[1].startswith('c'):
        triangle_type = 'console'

    if triangle_type == 'image':
        triangle = ImageTriangle((800, 600), 'triangles.png', scaling=3, background='purple')
        render(1, triangle)
        triangle.finish()
    else:
        triangle = ConsoleTriangle((80, 40))
        render(2, triangle)
        triangle.finish()
