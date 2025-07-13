import numpy as np
import cv2


class PenTool:

    def __init__(self, width: int, height: int, r: int, background: tuple):

        self.arr = []

        self.m = 0

        self.s_p = 0

        self.mouse_pos = 0

        self.radius = r

        self.w = width

        self.h = height

        self.dragging = False

        self.reflection = False

        self.active_box = None

        self.background = background

        self.janela = np.zeros((self.w, self.h, 3), dtype=np.uint8)

        self.buffer = np.zeros((self.w, self.h, 3), dtype=np.uint8)

        self.t = False

    def clean_buff(self):
        self.buffer = self.janela.copy()

    def save(self):
        self.bezier_curve(self.arr, self.janela)

    @staticmethod
    def insert_update(pos, value, array):
        if pos > len(array) - 1:
            return array.insert(pos, value)
        array[pos] = value

    @staticmethod
    def simetric_point(point1, medium_p):
        xb = (2 * medium_p[0]) - point1[0]
        yb = (2 * medium_p[1]) - point1[1]
        return tuple([xb, yb])

    @staticmethod
    def factorial(numero):
        result = 1

        while numero != 0:
            result *= numero
            numero -= 1

        return result

    @staticmethod
    def distance(pos1, pos2):
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        return ((dx ** 2) + (dy ** 2)) ** (1 / 2)

    def combination(self, n, k):
        return self.factorial(n) // (self.factorial(k) * self.factorial(n - k))

    def bezier_equation(self, t, var, degree, i):
        return self.combination(degree, i) * ((1 - t) ** (degree - i)) * ((t ** i) * var)

    def gen_point(self, t, array):

        fx, fy = 0, 0
        grau = len(array) - 1

        for i in range(len(array)):
            x, y = array[i]

            fx += self.bezier_equation(t, x, grau, i)
            fy += self.bezier_equation(t, y, grau, i)

        return [fx, fy]

    def bezier_curve(self, array, buf):
        pixels = []
        for t in np.linspace(0, 1, int(self.distance(array[0], array[-1]))):
            px, py = self.gen_point(t, array)
            pixels.append((int(px), int(py)))

        for i in range(len(pixels)-1):
            cv2.line(buf, pixels[i], pixels[i + 1], (0, 0, 255), 1)

    def draw(self, array):

        for i in range(len(array)):
            if i + 1 < len(array):
                cv2.line(self.buffer, array[i], array[i + 1], (0, 0, 255), 1)

            cv2.circle(self.buffer, array[i], self.radius, (255, 255, 255), -1)

    def mouse_callback(self, event, x, y, flags, param):

        self.clean_buff()

        if self.active_box:
            self.mouse_pos = (x, y)
            if len(self.arr) - 1 == 3:
                self.insert_update(self.active_box, self.simetric_point((x, y), self.m), self.arr)
            else:
                self.insert_update(self.active_box, (x, y), self.arr)

        if event == cv2.EVENT_LBUTTONUP:
            self.save()

            if len(self.arr) + 1 >= 4:
                if self.t:
                    self.arr = [self.m, (x, y)]
                else:
                    self.arr = [self.m]

            self.arr.append((x, y))

            self.active_box = self.arr.index((x, y)) + 1

            self.dragging = False

            self.t = False

        if self.dragging:

            self.s_p = self.simetric_point((x, y), self.m) if not self.reflection else self.s_p
            self.mouse_pos = (x, y)
            self.draw([self.s_p, self.m, self.mouse_pos])
            self.t = True

        if event == cv2.EVENT_LBUTTONDOWN:

            self.m = (x, y)

            if len(self.arr) <= 4:
                self.arr.append((x, y))

            self.dragging = True
            self.reflection = False

    def launch(self):

        self.janela[:, :] = [56, 49, 46]

        cv2.namedWindow('dst')
        cv2.setMouseCallback('dst', self.mouse_callback)

        while True:

            cv2.imshow('dst', self.buffer)

            k = cv2.waitKey(10) & 0xFF

            if self.active_box:
                self.bezier_curve(self.arr, self.buffer)

            if k == 27:
                break

            if k == ord("s"):
                self.save()
                self.reflection = True
                self.active_box = None

        cv2.destroyAllWindows()


pen_tool = PenTool(800, 800, 4, (56, 49, 46))

if __name__ == '__main__':
    pen_tool.launch()

