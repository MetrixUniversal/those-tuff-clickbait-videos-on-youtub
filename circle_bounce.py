import math
import time
import tkinter as tk


WIDTH = 800
HEIGHT = 800
CIRCLE_RADIUS = 300
BALL_RADIUS = 10
BALL_GROWTH = 2
MAX_BALL_RADIUS = CIRCLE_RADIUS - 15
BALL_SPEED = 240.0
BOUNCE_SPEED_MULTIPLIER = 1.00000000000000000000000001
GRAVITY = 500.0
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
        self.ball_radius = BALL_RADIUS
        self.boundary_radius = CIRCLE_RADIUS - self.ball_radius
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
        self.impact_lines: list[tuple[int, float, float]] = []
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

    def show_impact_line(self, wall_x: float, wall_y: float) -> None:
        line = self.canvas.create_line(
            wall_x,
            wall_y,
            self.x,
            self.y,
            fill="white",
            width=2,
        )
        self.impact_lines.append((line, wall_x, wall_y))
        self.canvas.tag_lower(line, self.ball)

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

            if self.vx * nx + self.vy * ny > 0:
                self.vx, self.vy = reflect_velocity(self.vx, self.vy, nx, ny)
                self.vx *= BOUNCE_SPEED_MULTIPLIER
                self.vy *= BOUNCE_SPEED_MULTIPLIER
                self.ball_radius = min(
                    self.ball_radius + BALL_GROWTH,
                    MAX_BALL_RADIUS,
                )
                self.boundary_radius = CIRCLE_RADIUS - self.ball_radius
                wall_x = self.center_x + nx * CIRCLE_RADIUS
                wall_y = self.center_y + ny * CIRCLE_RADIUS
                self.show_impact_line(wall_x, wall_y)

            self.x = self.center_x + nx * self.boundary_radius
            self.y = self.center_y + ny * self.boundary_radius

        for line, anchor_x, anchor_y in self.impact_lines:
            self.canvas.coords(line, anchor_x, anchor_y, self.x, self.y)
        self.canvas.coords(
            self.ball,
            self.x - self.ball_radius,
            self.y - self.ball_radius,
            self.x + self.ball_radius,
            self.y + self.ball_radius,
        )
        self.root.after(FRAME_MS, self.animate)


def main() -> None:
    root = tk.Tk()
    CircleBounce(root)
    root.mainloop()


if __name__ == "__main__":
    main()


# this is nice
