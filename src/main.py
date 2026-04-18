import os

from src.code_review_with_llm.Controller import Controller
from src.code_review_with_llm.Model import Model
from src.code_review_with_llm.View import View

if __name__ == "__main__":
    if not os.getenv("CI"):
        controller = Controller()
        model = Model(controller=controller)
        view = View(controller)

        controller.set_model(model)
        controller.set_view(view)

        view.mainloop()
