"""
GameEngine: owns the frog and all vehicles, and runs one frame's worth
of game logic.

Starter version: the frog can move, hop across the road, and reach the
goal - but there's no lives system, no score, and no timer. Collision
detection also has a known bug (see game/collisions.py) that Task 1
asks you to fix.
"""

import random

import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS, GRID_ROWS, GOAL_ROW, ROAD_ROWS, START_ROW, CELL_SIZE, WIDTH, HEIGHT,
)

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]   # one entry per road row, alternating direction
STARTING_LIVES = 3
ATTEMPT_TIME = 30.0


class GameEngine:
    def __init__(self):
        self.restart()

    def restart(self):
        self.lives = STARTING_LIVES
        self.score = 0
        self.time_left = ATTEMPT_TIME
        self.game_over = False
        self.game_won = False
        self.max_row_reached = START_ROW
        self._build_entities()


    def _build_entities(self):
        start_col = GRID_COLS // 2
        self.frog = Frog(
            col=start_col, row=START_ROW,
            start_col=start_col, start_row=START_ROW,
            cols=GRID_COLS, start_row_limit=START_ROW,
        )
        frog_x_range = (start_col * CELL_SIZE, start_col * CELL_SIZE + CELL_SIZE)

        self.vehicles = []
        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]
            vehicle_width = 40 if i % 2 == 0 else 70   # mix of cars and wider trucks
            spacing = 300
            count = 2

            # Try a few random phases and keep the first one that doesn't
            # already overlap the frog's starting column - guarantees a
            # safe first lane instead of leaving it to chance.
            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True
                for n in range(count):
                    offset = phase + n * spacing
                    x = offset if speed > 0 else WIDTH - offset - vehicle_width
                    positions.append(x)
                    if not (x + vehicle_width <= frog_x_range[0] or x >= frog_x_range[1]):
                        safe = False
                if safe:
                    break

            for x in positions:
                self.vehicles.append(Vehicle(x=x, row=row, width=vehicle_width,
                                              height=CELL_SIZE - 8, speed=speed))

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.restart()
            return

        if self.game_over or self.game_won:
            return

        if key == pygame.K_UP:
            self.frog.move(0, -1)
            if self.frog.row < self.max_row_reached:
                self.score += 10 * (self.max_row_reached - self.frog.row)
                self.max_row_reached = self.frog.row
        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)
        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def update(self, dt=1 / 60):
        if self.game_over or self.game_won:
            return

        for v in self.vehicles:
            v.update(road_width_px=WIDTH)

        if check_collision(self.frog, self.vehicles):
            self.lives -= 1
            self.frog.reset()
            self.max_row_reached = START_ROW
            self.time_left = ATTEMPT_TIME
            if self.lives <= 0:
                self.lives = 0
                self.time_left = 0
                self.game_over = True
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self.lives -= 1
            self.frog.reset()
            self.max_row_reached = START_ROW
            self.time_left = ATTEMPT_TIME
            if self.lives <= 0:
                self.lives = 0
                self.time_left = 0
                self.game_over = True
            return

        if self.frog.row == GOAL_ROW:
            self.score += 100
            self.game_won = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.frog, self.vehicles)
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 14))
        renderer.draw_text(surface, font, f"Score: {self.score}", (150, 14))
        renderer.draw_text(surface, font, f"Time: {max(0, int(self.time_left))}", (290, 14))
        renderer.draw_text(surface, font, "Arrow keys to move. R to restart.", (10, HEIGHT - 24))

        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER! Press R to restart")
        elif self.game_won:
            renderer.draw_banner(surface, font, f"YOU WIN! Score: {self.score} - Press R to restart")


