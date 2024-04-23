import flet as ft

class MyApp(ft.FletApp):
    def build(self):
        # Crear la AppBar
        appbar = ft.AppBar(title="Mi AppBar")
        
        # Crear un GestureDetector para detectar eventos de mouse
        gesture_detector = ft.GestureDetector(
            on_tap_down=self.on_tap_down,
            on_tap_up=self.on_tap_up,
            on_double_tap=self.on_double_tap,
            on_long_press=self.on_long_press,
            on_pan_start=self.on_pan_start,
            on_pan_update=self.on_pan_update,
            on_pan_end=self.on_pan_end,
        )
        
        # Añadir el GestureDetector a la AppBar
        appbar.add_widget(gesture_detector)
        
        return appbar

    def on_tap_down(self, event):
        print("Tap down:", event)

    def on_tap_up(self, event):
        print("Tap up:", event)

    def on_double_tap(self, event):
        print("Double tap:", event)

    def on_long_press(self, event):
        print("Long press:", event)

    def on_pan_start(self, event):
        print("Pan start:", event)

    def on_pan_update(self, event):
        print("Pan update:", event)

    def on_pan_end(self, event):
        print("Pan end:", event)

if __name__ == '__main__':
    MyApp.run()
