from Controller import Controller
from Model import Model
from View import View

if __name__ == "__main__":
    controller = Controller()
    model = Model(controller)
    view = View(controller)

    controller.set_model(model)
    controller.set_view(view)

    repo_url = "https://github.com/psf/requests"
    pr_id_list = [7217]
    ollama_model = "llama3:latest"

    #controller.run([repo_url, pr_id_list, ollama_model], 1)
    controller.run([4, 5, 2026, 2026], 2)
    #controller.run([-1, -1, -1, -1], 2)

