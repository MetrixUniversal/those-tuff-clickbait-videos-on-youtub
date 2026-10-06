import math
import time
import tkinter as tk


WIDTH = 800
HEIGHT = 800
CIRCLE_RADIUS = 300
BALL_RADIUS = 10
BALL_SPEED = 240.0
GRAVITY = 500.0
IMPACT_LINE_LENGTH = 28.0
FRAME_MS = 16


def reflect_velocity(vx: float, vy: float, nx: float, ny: float) -> tuple[float, float]:
    normal_speed = vx * nx + vy * ny
    return vx - 2 * normal_speed * nx, vy - 2 * normal_speed * ny


class CircleBounce:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Circle Bounce")
        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            background="black",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.center_x = WIDTH / 2
        self.center_y = HEIGHT / 2
        self.boundary_radius = CIRCLE_RADIUS - BALL_RADIUS
        self.x = self.center_x
        self.y = self.center_y
        self.vx = BALL_SPEED * math.cos(math.radians(-37))
        self.vy = BALL_SPEED * math.sin(math.radians(-37))

        self.canvas.create_oval(
            self.center_x - CIRCLE_RADIUS,
            self.center_y - CIRCLE_RADIUS,
            self.center_x + CIRCLE_RADIUS,
            self.center_y + CIRCLE_RADIUS,
            outline="white",
            width=2,
        )
        self.impact_line: int | None = None
        self.ball = self.canvas.create_oval(
            self.x - BALL_RADIUS,
            self.y - BALL_RADIUS,
            self.x + BALL_RADIUS,
            self.y + BALL_RADIUS,
            fill="white",
            outline="white",
        )

        self.previous_time = time.perf_counter()
        self.root.bind("<Escape>", lambda _event: self.root.destroy())
        self.animate()

    def show_impact_line(self) -> None:
        if self.impact_line is not None:
            self.canvas.delete(self.impact_line)
        self.impact_line = self.canvas.create_line(
            self.x,
            self.y,
            self.x,
            self.y,
            fill="white",
            width=2,
        )
        self.canvas.tag_lower(self.impact_line, self.ball)

    def animate(self) -> None:
        now = time.perf_counter()
        dt = min(now - self.previous_time, 0.05)
        self.previous_time = now

        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        dx = self.x - self.center_x
        dy = self.y - self.center_y
        distance = math.hypot(dx, dy)

        if distance >= self.boundary_radius and distance > 0:
            nx = dx / distance
            ny = dy / distance
            self.x = self.center_x + nx * self.boundary_radius
            self.y = self.center_y + ny * self.boundary_radius

            if self.vx * nx + self.vy * ny > 0:
                self.vx, self.vy = reflect_velocity(self.vx, self.vy, nx, ny)
                self.show_impact_line()

        if self.impact_line is not None:
            speed = math.hypot(self.vx, self.vy)
            if speed > 0:
                direction_x = self.vx / speed
                direction_y = self.vy / speed
                self.canvas.coords(
                    self.impact_line,
                    self.x - direction_x * BALL_RADIUS,
                    self.y - direction_y * BALL_RADIUS,
                    self.x - direction_x * (BALL_RADIUS + IMPACT_LINE_LENGTH),
                    self.y - direction_y * (BALL_RADIUS + IMPACT_LINE_LENGTH),
                )
        self.canvas.coords(
            self.ball,
            self.x - BALL_RADIUS,
            self.y - BALL_RADIUS,
            self.x + BALL_RADIUS,
            self.y + BALL_RADIUS,
        )
        self.root.after(FRAME_MS, self.animate)


def main() -> None:
    root = tk.Tk()
    CircleBounce(root)
    root.mainloop()


if __name__ == "__main__":
    main()


# this is nice
