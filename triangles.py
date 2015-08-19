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
        self._canvas = [[" " for _ in range(w)] for _ in range(h)]
        self.fill(self.boundary(), char='#')

    def fill(self, triangle, char=' '):
        # Draw a triangle by filling line segments from top to bottom

        # left, right, bottom (pointing down)
        (ax, ay), (bx, by), (cx, cy) = triangle
    
        segment_length = max(bx - ax, cx - bx)
        height = int(round(cy - ay))
        x_offset = min(ax, bx, cx)
        dx = segment_length / height
        y_offset = min(ay, by, cy)
        row_range = range(height)
        if ax > bx:
            # Reversed rectangle
            row_range = range(height, 0, -1)
        for row in row_range:
            start = int(round(x_offset))
            end = int(round(x_offset + segment_length))
            y = int(round(row + y_offset))
            for x in range(start, end+1):
                try:
                    self._canvas[y][x] = char
                except IndexError:
                    pass  # Don't care - out of bounds
            x_offset += dx/2
            segment_length -= dx

    def finish(self):
        print("\n".join("".join(row) for row in self._canvas), end="")


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

    if maxdepth == 0:
        return

    regions = [(1, triangle.boundary())]
    for level, region in regions:
        triangle.fill(midpoints(region))
        if level < maxdepth:
            for subtriangle in subtriangles(region):
                regions.append((level+1, subtriangle))


if __name__ == '__main__':
    import sys

    triangle_type = 'image'
    iterations = 2

    if len(sys.argv) > 1 and sys.argv[1].startswith('c'):
        triangle_type = 'console'

    if len(sys.argv) > 2:
        iterations = int(sys.argv[2])
        print("iterations set to", iterations)

    if triangle_type == 'image':
        triangle = ImageTriangle((800, 600), 'triangles.png', scaling=3, background='purple')
        render(iterations, triangle)
        triangle.finish()
    else:
        import console
        term_size = console.get_terminal_size()
        triangle = ConsoleTriangle(term_size)
        render(iterations, triangle)
        triangle.finish()
        input("\r")
