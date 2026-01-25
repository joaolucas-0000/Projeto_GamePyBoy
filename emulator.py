# emulator.py

from pyboy import PyBoy

class GameBoyEmulator:
    def __init__(self, rom_path, window_scale=3):
        self.pyboy = PyBoy(
            rom_path,
            window="SDL2",
            scale=window_scale,
            sound=True 
        )


        self.pyboy.set_emulation_speed(1.0)
        self.running = True

    def tick(self):
        return self.pyboy.tick()

    def stop(self):
        self.running = False
        self.pyboy.stop()
