from Controller import Controller
from Model import Model
from View import View

if __name__ == "__main__":
    controller = Controller()
    model = Model(controller=controller)
    view = View(controller)

    controller.set_model(model)
    controller.set_view(view)

    view.mainloop()
