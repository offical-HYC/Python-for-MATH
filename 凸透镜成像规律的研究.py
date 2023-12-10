from arcade import *

# 窗体宽高及标题
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "凸透镜成像"
# 移动速度
SPEED = 10


# 物
class Image(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.center_x, self.center_y = x, y
        self.append_texture(load_texture(image, flipped=True))


# 凸透镜
class Lens(Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.center_x, self.center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2


# 程序主体
class Program(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)  # 窗口初始化
        self.setup()  # 程序初始化

    # 初始化
    def setup(self):
        set_background_color(color.WHITE)  # 设置背景颜色
        self.focal_length = 250  # 初始焦距
        self.u = 500  # 初始物距
        self.v_size = 1  # 初始像物大小比例
        self.v_able = True  # 初始成像情况
        self.u_speed = 0
        self.lens_speed = 0  # 初始速度
        # 基本对象实例化
        self.lens = Lens("lens.png")  # 透镜

    # 绘制图像
    def on_draw(self):
        start_render()
        self.lens.draw()
        # 焦距提示
        draw_text(f"当前焦距：{self.focal_length}",50, 50, color.RED, font_name="zh-cn.ttf", font_size=20)
        # 光线的绘制
        draw_line(SCREEN_WIDTH // 2 - self.u, SCREEN_HEIGHT // 2 + 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                  color.RED, 10)  # 平行于主光轴的入射光线经凸透镜折射后过焦点
        draw_line(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, SCREEN_WIDTH // 2 + self.focal_length * 10, SCREEN_HEIGHT // 2 - 50 * 10,
                  color.RED, 10)
        draw_line(SCREEN_WIDTH // 2 - self.u, SCREEN_HEIGHT // 2 + 50, SCREEN_WIDTH + self.u * 10, SCREEN_HEIGHT // 2 - 50 * 10,
                  color.RED, 10)  # 过光心的光线方向不变
        # 焦点、二倍焦点的绘制
        draw_circle_filled(SCREEN_WIDTH // 2 - self.focal_length, SCREEN_HEIGHT // 2, 20, color.BLUE)
        draw_circle_filled(SCREEN_WIDTH // 2 + self.focal_length, SCREEN_HEIGHT // 2, 20, color.BLUE)
        draw_circle_filled(SCREEN_WIDTH // 2 - self.focal_length * 2, SCREEN_HEIGHT // 2, 20, color.BLUE)
        draw_circle_filled(SCREEN_WIDTH // 2 + self.focal_length * 2, SCREEN_HEIGHT // 2, 20, color.BLUE)
        if self.v_able:
            self.v_sun.draw()

        self.sun.draw()

    # 逻辑处理
    def on_update(self, delta_time: float):
        self.u += self.u_speed
        self.focal_length += self.lens_speed
        # 一倍焦距分虚实
        if self.u == self.focal_length or self.u <= 0:
            self.v_able = False
            return
        else:
            self.v_able = True
        if self.v_able:
            if self.u > self.focal_length:
                # 像物大小比例随物距变化而变化
                self.v_size = self.focal_length * 2 / self.u
                # 像的位置
                """
                凸透镜的成像规律是1/u + 1/v = 1/f（即：物距的倒数与像距的倒数之和等于焦距的倒数。）
                """
                self.v_x = SCREEN_WIDTH // 2 + 1 / (1 / self.focal_length - 1 / self.u)
                self.v_sun = Image("fish.png", self.v_x, SCREEN_HEIGHT // 2 - 25)
                self.v_sun.set_texture(1)
            else:
                self.v_size = self.u / self.focal_length * 5
                self.v_x = SCREEN_WIDTH // 2 - (self.u / 100) ** 2 * 120
                self.v_sun = Image("virtual-fish.png", self.v_x, SCREEN_HEIGHT // 2)


        self.sun = Image("fish.png", SCREEN_WIDTH // 2 - self.u, SCREEN_HEIGHT // 2)  # 物
        self.sun.change_x = self.u_speed

        self.v_sun.scale = self.v_size

    # 按下键盘移动物
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == key.A:
            self.u_speed = SPEED
        elif symbol == key.D and self.u > SPEED:
            self.u_speed = -SPEED
        elif symbol == key.W:
            self.lens_speed = SPEED
        elif symbol == key.S and self.focal_length > SPEED:
            self.lens_speed = -SPEED

    # 松开键盘还原
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == key.A or symbol == key.D:
            self.u_speed = 0
        elif symbol == key.W or symbol == key.S:
            self.lens_speed = 0


if __name__ == "__main__":
    program = Program(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    run()
