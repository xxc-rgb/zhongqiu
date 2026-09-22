"""Procedural drawing helpers for the Mid-Autumn scene."""

from __future__ import annotations

import math
from typing import Iterable, Sequence

import pygame


Color = tuple[int, int, int]


def clamp(value: float, low: float, high: float) -> float:
    """Return value constrained to the inclusive range."""
    return max(low, min(high, value))


def lerp_color(start: Sequence[int], end: Sequence[int], amount: float) -> Color:
    """Interpolate two RGB colors."""
    amount = clamp(amount, 0.0, 1.0)
    return tuple(round(a + (b - a) * amount) for a, b in zip(start, end))  # type: ignore[return-value]


def vertical_gradient(surface: pygame.Surface, top: Color, bottom: Color) -> None:
    """Paint a vertical RGB gradient across a surface."""
    height = max(1, surface.get_height() - 1)
    for y in range(surface.get_height()):
        surface.fill(lerp_color(top, bottom, y / height), (0, y, surface.get_width(), 1))


def glow_circle(
    surface: pygame.Surface,
    center: tuple[int, int],
    radius: int,
    color: Color,
    layers: int = 10,
    alpha: int = 90,
) -> None:
    """Draw a soft radial glow using progressively smaller translucent circles."""
    if radius <= 0:
        return
    glow = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for index in range(layers, 0, -1):
        ratio = index / layers
        current_radius = max(1, round(radius * ratio))
        current_alpha = round(alpha * (1.0 - ratio) ** 2 + alpha * 0.04)
        pygame.draw.circle(glow, (*color, current_alpha), center, current_radius)
    surface.blit(glow, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)


def draw_text_glow(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    center: tuple[int, int],
    color: Color,
    glow_color: Color,
    glow_radius: int = 18,
) -> None:
    """Render text with a blurred-looking halo made from offset alpha copies."""
    glow = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    text_surface = font.render(text, True, (*glow_color, 150))
    text_rect = text_surface.get_rect(center=center)
    for angle in range(0, 360, 30):
        offset = (
            round(math.cos(math.radians(angle)) * glow_radius / 3),
            round(math.sin(math.radians(angle)) * glow_radius / 3),
        )
        glow.blit(text_surface, text_rect.move(*offset))
    surface.blit(glow, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
    solid = font.render(text, True, color)
    surface.blit(solid, solid.get_rect(center=center))


def draw_polyline_glow(
    surface: pygame.Surface,
    points: Iterable[tuple[int, int]],
    color: Color,
    width: int = 1,
) -> None:
    """Draw a low-key glowing line for distant atmospheric details."""
    points = list(points)
    if len(points) < 2:
        return
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.lines(overlay, (*color, 55), False, points, width + 5)
    surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
    pygame.draw.lines(surface, color, False, points, width)
