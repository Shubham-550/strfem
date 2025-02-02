from src.strfem import Viewer, Controller
from sample_frame import sample_frame


def main() -> None:
    controller = Controller()
    viewer = Viewer()

    # Sample frame
    sample_frame(controller)

    # Analysis
    controller.linear_elastic_analysis()

    # Reporting
    print(controller)

    # viewer.render(controller)


if __name__ == "__main__":
    main()
