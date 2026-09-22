"""Launch the 中秋快乐 · 峰和岩 Pygame MVP."""

from __future__ import annotations

import argparse
import pygame

from scene import BASE_HEIGHT, BASE_WIDTH, Scene


def run(max_frames: int | None = None) -> int:
    """Run the animation loop. max_frames is useful for smoke tests."""
    pygame.init()
    try:
        flags = pygame.RESIZABLE
        window = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), flags)
        pygame.display.set_caption("中秋快乐 · 峰和岩")
        logical = pygame.Surface((BASE_WIDTH, BASE_HEIGHT)).convert()
        scene = Scene()
        clock = pygame.time.Clock()
        frames = 0
        running = True
        while running:
            dt = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        scene.paused = not scene.paused
                    elif event.key == pygame.K_r:
                        scene.reset()
                    elif event.key == pygame.K_f:
                        if flags & pygame.FULLSCREEN:
                            flags = pygame.RESIZABLE
                            window = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), flags)
                        else:
                            flags = pygame.FULLSCREEN
                            window = pygame.display.set_mode((0, 0), flags)
                elif event.type == pygame.VIDEORESIZE:
                    width = max(640, event.w)
                    height = max(360, event.h)
                    window = pygame.display.set_mode((width, height), flags)
            scene.update(dt)
            scene.draw(logical)
            width, height = window.get_size()
            scale = min(width / BASE_WIDTH, height / BASE_HEIGHT)
            target_size = (max(1, round(BASE_WIDTH * scale)), max(1, round(BASE_HEIGHT * scale)))
            scaled = pygame.transform.smoothscale(logical, target_size)
            window.fill((4, 7, 17))
            window.blit(scaled, scaled.get_rect(center=window.get_rect().center))
            pygame.display.flip()
            frames += 1
            if max_frames is not None and frames >= max_frames:
                break
        return 0
    finally:
        pygame.quit()


def main() -> int:
    parser = argparse.ArgumentParser(description="中秋快乐 · 峰和岩动画贺卡")
    parser.add_argument("--frames", type=int, default=None, help="运行指定帧数后退出，用于烟测")
    args = parser.parse_args()
    return run(args.frames)


if __name__ == "__main__":
    raise SystemExit(main())
