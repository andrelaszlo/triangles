WIDTH = 80
HEIGHT = 40


def midpoints(points):
    (ax, ay), (bx, by), (cx, cy) = points
    ab = bx + ((ax - bx) / 2), ay + ((by - ay) / 2)
    ac = ax + ((cx - ax) / 2), ay + ((cy - ay) / 2)
    bc = bx + ((cx - bx) / 2), by
    return ab, ac, bc


def subtriangles(points, midpoints):
    a, b, c = points
    ab, ac, bc = midpoints
    return (a, ab, ac), (ab, b, bc), (ac, bc, c)


def fill(midpoints, tri):
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



def generate(maxdepth):
    tri = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    # top, left, right
    points = ((WIDTH/2, 0), (0, HEIGHT), (WIDTH, HEIGHT))
    return generate_(maxdepth, tri, points, 0)


def generate_(maxdepth, tri, points, depth):
    if depth > maxdepth:
        return tri

    w = len(tri[0])
    h = len(tri)
    mids = midpoints(points)

    print(points)

    #print(points, mids)
    subs = subtriangles(points, mids)
    fill(mids, tri)
    a, b, c = points
    print(a, b, c)

    tri[int(a[1])][int(a[0])] = "A"
    tri[int(b[1])-1][int(b[0])-1] = "B"
    tri[int(c[1])-1][int(c[0])-1] = "C"
    return generate_(maxdepth, tri, points, depth+1)


def render(tri):
    print("\n".join("".join(row) for row in tri))

render(generate(0))
