from random import randint


class Wheel:
    @staticmethod
    def spin_wheel():
        wheel = [100, 200, 300, 400, 500, 0, -1, 100, 200, 300, 400, 500]
        return wheel[randint(0, len(wheel) - 1)]
