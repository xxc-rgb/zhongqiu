"""The procedural Mid-Autumn mountain and rock scene."""

from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass
from pathlib import Path

import pygame

from effects import draw_polyline_glow, draw_text_glow, glow_circle, vertical_gradient


BASE_WIDTH = 1280
BASE_HEIGHT = 720
TITLE = "峰岩 · 中秋快乐"
SUBTITLE = "峰起月明，岩守团圆"


@dataclass
class Star:
    x: float
    y: float
    radius: float
    phase: float
    brightness: float


@dataclass
class Particle:
    x: float
    y: float
    speed: float
    drift: float
    size: float
    phase: float


@dataclass
class Meteor:
    x: float
    y: float
    speed: float
    length: float
    life: float
    max_life: float


def find_font(size: int, bold: bool = False) -> pygame.font.Font:
    """Load a common CJK font on Windows, falling back to Pygame's default."""
    if not pygame.font.get_init():
        pygame.font.init()
    candidates = [
        Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "msyhbd.ttc" if bold else Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "msyh.ttc",
        Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "simhei.ttf",
        Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "simsun.ttc",
    ]
    for path in candidates:
        if path.exists():
            return pygame.font.Font(str(path), size)
    return pygame.font.Font(None, size)


class Scene:
    """Stateful animation scene rendered in the fixed logical coordinate system."""

    def __init__(self, seed: int = 20240917) -> None:
        self.seed = seed
        self.random = random.Random(seed)
        self.title_font = find_font(84, bold=True)
        self.subtitle_font = find_font(24)
        self.small_font = find_font(18)
        self.reset()

    def reset(self) -> None:
        """Reset animation time and regenerate deterministic particles."""
        self.time = 0.0
        self.paused = False
        rng = random.Random(self.seed)
        self.stars = [
            Star(rng.uniform(40, BASE_WIDTH - 40), rng.uniform(40, 430), rng.uniform(0.6, 2.4), rng.uniform(0, math.tau), rng.uniform(0.45, 1.0))
            for _ in range(105)
        ]
        self.particles = [
            Particle(rng.uniform(0, BASE_WIDTH), rng.uniform(430, 690), rng.uniform(4, 14), rng.uniform(-7, 7), rng.uniform(1, 3), rng.uniform(0, math.tau))
            for _ in range(42)
        ]
        self.meteors: list[Meteor] = []

    def update(self, dt: float) -> None:
        """Advance all animation state by dt seconds."""
        if self.paused:
            return
        self.time += max(0.0, min(dt, 0.1))
        for particle in self.particles:
            particle.y -= particle.speed * dt
            particle.x += math.sin(self.time * 0.8 + particle.phase) * particle.drift * dt
            if particle.y < 410:
                particle.y = 700
                particle.x = self.random.uniform(0, BASE_WIDTH)
        if len(self.meteors) < 2 and self.random.random() < dt * 0.16:
            self.meteors.append(Meteor(self.random.uniform(740, 1180), self.random.uniform(70, 230), self.random.uniform(420, 620), self.random.uniform(45, 85), 1.0, 1.0))
        for meteor in self.meteors:
            meteor.x -= meteor.speed * dt
            meteor.y += meteor.speed * 0.42 * dt
            meteor.life -= dt
        self.meteors = [meteor for meteor in self.meteors if meteor.life > 0 and meteor.x > -100]

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the complete scene to a 1280x720 logical surface."""
        vertical_gradient(surface, (9, 17, 48), (35, 18, 58))
        self._draw_stars(surface)
        self._draw_moon(surface)
        self._draw_meteors(surface)
        self._draw_mountains(surface)
        self._draw_clouds(surface)
        self._draw_rocks(surface)
        self._draw_particles(surface)
        self._draw_typography(surface)

    def _draw_stars(self, surface: pygame.Surface) -> None:
        for star in self.stars:
            pulse = 0.72 + 0.28 * math.sin(self.time * 1.7 + star.phase)
            value = round(255 * star.brightness * pulse)
            pygame.draw.circle(surface, (value, value, min(255, value + 28)), (round(star.x), round(star.y)), max(1, round(star.radius)))

    def _draw_moon(self, surface: pygame.Surface) -> None:
        center = (930, 190)
        breathing = 1.0 + 0.035 * math.sin(self.time * 1.2)
        glow_circle(surface, center, round(190 * breathing), (242, 202, 116), layers=18, alpha=70)
        pygame.draw.circle(surface, (255, 230, 163), center, round(82 * breathing))
        pygame.draw.circle(surface, (255, 241, 190), (center[0] - 15, center[1] - 18), round(66 * breathing))
        for offset, radius, alpha in [((-25, 18), 12, 28), ((21, -27), 9, 24), ((30, 25), 6, 20)]:
            crater = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(crater, (196, 155, 89, alpha), (center[0] + offset[0], center[1] + offset[1]), radius)
            surface.blit(crater, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)

    def _ridge(self, base_y: int, amplitude: int, phase: float, step: int = 32) -> list[tuple[int, int]]:
        points = [(0, BASE_HEIGHT), (0, base_y)]
        for x in range(0, BASE_WIDTH + step, step):
            y = base_y - amplitude * (0.5 + 0.5 * math.sin(x * 0.014 + phase))
            y -= amplitude * 0.35 * math.sin(x * 0.038 + phase * 1.7)
            points.append((min(x, BASE_WIDTH), round(y)))
        points.extend([(BASE_WIDTH, BASE_HEIGHT), (0, BASE_HEIGHT)])
        return points

    def _draw_mountains(self, surface: pygame.Surface) -> None:
        pygame.draw.polygon(surface, (19, 23, 54), self._ridge(430, 105, 0.3))
        pygame.draw.polygon(surface, (15, 19, 42), self._ridge(505, 145, 2.1))
        front = self._ridge(565, 190, 4.5)
        pygame.draw.polygon(surface, (9, 13, 29), front)
        draw_polyline_glow(surface, front[1:-2], (70, 65, 107), 1)

    def _draw_clouds(self, surface: pygame.Surface) -> None:
        fog = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        drift = (self.time * 18) % 150
        for row, y in enumerate((475, 520, 585)):
            for index in range(9):
                x = index * 170 - drift * (1 + row * 0.2)
                pygame.draw.ellipse(fog, (187, 180, 214, 18 + row * 5), (x, y + math.sin(index + self.time * 0.5) * 7, 260, 55))
        surface.blit(fog, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)

    def _draw_rocks(self, surface: pygame.Surface) -> None:
        left = [(0, 720), (0, 602), (85, 548), (140, 570), (193, 505), (253, 573), (323, 543), (378, 620), (450, 720)]
        right = [(830, 720), (875, 632), (934, 600), (980, 622), (1023, 545), (1075, 580), (1136, 520), (1205, 584), (1280, 565), (1280, 720)]
        pygame.draw.polygon(surface, (10, 12, 24), left)
        pygame.draw.polygon(surface, (8, 10, 20), right)
        pygame.draw.polygon(surface, (22, 22, 38), [(85, 548), (140, 570), (193, 505), (179, 584), (122, 608)])
        pygame.draw.polygon(surface, (19, 19, 32), [(1023, 545), (1075, 580), (1136, 520), (1112, 601), (1055, 618)])
        pygame.draw.lines(surface, (55, 51, 75), False, [(85, 548), (140, 570), (193, 505)], 2)
        pygame.draw.lines(surface, (45, 43, 64), False, [(1023, 545), (1075, 580), (1136, 520)], 2)

    def _draw_particles(self, surface: pygame.Surface) -> None:
        for particle in self.particles:
            alpha = round(120 + 70 * (0.5 + 0.5 * math.sin(self.time * 2 + particle.phase)))
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (255, 210, 126, alpha), (round(particle.x), round(particle.y)), max(1, round(particle.size)))
            surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)

    def _draw_meteors(self, surface: pygame.Surface) -> None:
        for meteor in self.meteors:
            alpha = round(255 * max(0.0, min(1.0, meteor.life)))
            trail = (round(meteor.x + meteor.length), round(meteor.y - meteor.length * 0.42))
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.line(overlay, (255, 226, 159, alpha), (round(meteor.x), round(meteor.y)), trail, 2)
            surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)

    def _draw_typography(self, surface: pygame.Surface) -> None:
        title_y = 430 + round(math.sin(self.time * 1.1) * 3)
        draw_text_glow(surface, self.title_font, TITLE, (640, title_y), (255, 235, 173), (255, 178, 75), 22)
        subtitle = self.subtitle_font.render(SUBTITLE, True, (225, 212, 189))
        surface.blit(subtitle, subtitle.get_rect(center=(640, title_y + 70)))
        hint = self.small_font.render("SPACE 暂停 · R 重置 · F 全屏 · ESC 退出", True, (155, 151, 184))
        surface.blit(hint, hint.get_rect(center=(640, 682)))
