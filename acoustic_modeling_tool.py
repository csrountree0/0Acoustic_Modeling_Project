# link everything together
from acoustic_view import View
from acoustic_controller import Controller
c = Controller()
v = View(c)
v.initgui()
v.run()
