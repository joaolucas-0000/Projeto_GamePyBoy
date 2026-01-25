
from emulator import GameBoyEmulator
from config import ROM_PATH, WINDOW_SCALE, DEBUG

def main():
    try:
        emu = GameBoyEmulator(
            rom_path=ROM_PATH,
            window_scale=WINDOW_SCALE
        )

        if DEBUG:
            print("[INFO] Emulator started")

        while emu.tick():
            pass

    except Exception as e:
        print("[FATAL ERROR]", e)
        raise

    finally:
        print("[INFO] Emulator stopped")

if __name__ == "__main__":
    main()
