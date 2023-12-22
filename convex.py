from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def count(self):
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p, li):
        return Point(p, li)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, li):
        self.p = p
        self.li = li
        self.cast = 0
        if any(p.out_of_ambit(c) < 1 for c in li) or p.in_triangle(li):
            self.cast += 1
            print(any(p.out_of_ambit(c) < 1 for c in li))
            print(p.in_triangle(li))
        #li-треугольник

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.li)

    def count(self):
        return self.cast


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, li):
        self.p, self.q = p, q
        self.li = li
        self.cast = 0
        if any(p.out_of_ambit(c) < 1 for c in li) or p.in_triangle(li):
            self.cast += 1
        if any(q.out_of_ambit(c) < 1 for c in li) or q.in_triangle(li):
            self.cast += 1

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.li)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r, self.li)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q, self.li)
        else:
            return self

    def count(self):
        return self.cast


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, li):
        self.points = Deq()
        self.cast = 0
        self.li = li
        self.points.push_first(b)
        if any(a.out_of_ambit(c) < 1 for c in li) or a.in_triangle(li):
            self.cast += 1
        if any(b.out_of_ambit(c) < 1 for c in li) or b.in_triangle(li):
            self.cast += 1
        if any(c.out_of_ambit(d) < 1 for d in li) or c.in_triangle(li):
            self.cast += 1

        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def count(self):
        return self.cast

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                if any(p.out_of_ambit(c) < 1 for c in self.li) or p.in_triangle(self.li):
                    self.cast -= 1
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                if any(p.out_of_ambit(c) < 1 for c in self.li) or p.in_triangle(self.li):
                    self.cast -= 1
                p = self.points.pop_last()

            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)

        if any(t.out_of_ambit(c) < 1 for c in self.li) or t.in_triangle(self.li):
            self.cast += 1
        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
