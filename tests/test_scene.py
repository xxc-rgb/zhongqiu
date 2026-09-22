import os
import unittest


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

try:
    import pygame
except ImportError:  # pragma: no cover - allows clear collection without dependency
    pygame = None


@unittest.skipIf(pygame is None, "pygame 未安装")
class SceneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))
        from scene import Scene

        cls.Scene = Scene

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_scene_resets_deterministically(self):
        first = self.Scene()
        second = self.Scene()
        self.assertEqual([(s.x, s.y) for s in first.stars], [(s.x, s.y) for s in second.stars])
        first.update(0.25)
        self.assertGreater(first.time, 0)
        first.reset()
        self.assertEqual(first.time, 0)
        self.assertFalse(first.paused)

    def test_title_centers_fengyan_theme(self):
        from scene import SUBTITLE, TITLE

        self.assertIn("峰岩", TITLE)
        self.assertIn("中秋快乐", TITLE)
        self.assertIn("峰", SUBTITLE)
        self.assertIn("岩", SUBTITLE)

    def test_update_stops_when_paused(self):
        scene = self.Scene()
        scene.paused = True
        scene.update(1.0)
        self.assertEqual(scene.time, 0)

    def test_draw_and_resize_surface(self):
        from scene import BASE_HEIGHT, BASE_WIDTH

        scene = self.Scene()
        canvas = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        scene.draw(canvas)
        resized = pygame.transform.smoothscale(canvas, (960, 540))
        self.assertEqual(resized.get_size(), (960, 540))

    def test_main_smoke_loop(self):
        from main import run

        self.assertEqual(run(max_frames=2), 0)


if __name__ == "__main__":
    unittest.main()
