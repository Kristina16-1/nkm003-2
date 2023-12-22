from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    def out_of_ambit(self, other):
        a_1 = (self.x - other.p.x) * (other.q.x - other.p.x) + (
                self.y - other.p.y) * (other.q.y - other.p.y)
        a_2 = (self.x - other.q.x) * (other.p.x - other.q.x) + (
                self.y - other.q.y) * (other.p.y - other.q.y)
        if a_2 < 0 < a_1:
            a = self.dist(other.q)
        elif a_1 < 0 < a_2:
            a = self.dist(other.p)
        else:
            a = 2 * abs(R2Point.area(self, other.q, other.p) / other.p.dist(
            other.q))

        return a

    def in_triangle(self, li):
        p, q, r = li[0].q, li[1].q, li[2].q
        e1 = (p.x - self.x) * (q.y - p.y) - (q.x - p.x) * (p.y - self.y)
        e2 = (q.x - self.x) * (r.y - q.y) - (r.x - q.x) * (q.y - self.y)
        e3 = (r.x - self.x) * (p.y - r.y) - (p.x - r.x) * (r.y - self.y)
        e = (e1, e2, e3)
        if all(c <= 0 for c in e) or all(c >= 0 for c in e):
            return False
        else:
            return True


class Interval:
    def __init__(self, p, q):
        self.p, self.q = p, q


if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
