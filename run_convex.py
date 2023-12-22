#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void
from r2point import Interval

print('Введите точки, образующие треугольник:')
a = R2Point()
t = True
while t:
    t = False
    b = R2Point()
    if b == a:
        print('Точка совпадает с предыдущей, попробуйте ещё раз.')
        t = True
t = True
while t:
    t = False
    c = R2Point()
    if R2Point.area(a, b, c) == 0:
        print('Точки не образуют треугольник, попробуйте ещё раз.')
        t = True
print('Ввод завершён')

li = (Interval(b, a), Interval(c, b), Interval(c, a))

f = Void()
try:
    while True:
        if isinstance(f, Void):
            f = f.add(R2Point(), li)
        else:
            f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, C = {f.count()}")
        print()
except(EOFError, KeyboardInterrupt):
    print("\nStop")
