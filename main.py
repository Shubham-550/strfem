from src.strfem import Viewer, Controller
from sample_frame import sample_frame


def main() -> None:
    controller = Controller()
    viewer = Viewer()

    sample_frame(controller)

    print(controller)

    # viewer.render(controller)


if __name__ == "__main__":
    main()
