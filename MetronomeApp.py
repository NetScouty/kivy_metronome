import time
import threading
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.widget import Widget


class Controller(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.actual_value = int(self.bpm_l.text)
        self.pause = True

    def new_value(self, *args):
        self.bpm_l.text = str(int(args[1]))

    def changing_bpm(self, op):
        actual_value = int(self.bpm_l.text)
        if op == '+':
            if actual_value < 250:
                self.bpm_l.text = str(actual_value + 1)
        elif op == '-':
            if actual_value > 30:
                self.bpm_l.text = str(actual_value - 1)
        self.bpm_slider.value = self.bpm_l.text
        return self.bpm_l.text

    def play(self, *args):
        if self.pause:
            self.pause = False
            thread = threading.Thread(target=self._play, daemon=True)
            thread.start()

    
    def close(self, *args):
        self.pause = False


    def _play(self):
        wav = SoundLoader.load('click.wav')
        bpm = 30/int(self.actual_value)
        while not self.pause:
            start = time.time()
            wav.play()
            stop = time.time()
            func_delay = stop - start
            time.sleep(bpm-func_delay)


    def stop(self):
        if not self.pause:
            self.pause = True


class MetronomeApp(App):
    def build(self):
        return Controller()


if __name__ == '__main__':
    app = MetronomeApp()
    app.run()
