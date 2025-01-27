# strfem

strfem is a Python-based project implementing the Finite Element Method (FEM) for the linear static analysis of bar members. This project is inspired by the video series [**"Programming the Finite Element Model"**](https://www.youtube.com/playlist?list=PLmw2x4fCMxg5zDmmB4eUK-YIKFycOjOjm) by [Civil Engineering Essentials](https://www.youtube.com/@CivilEngineeringEssentials), which demonstrates FEM programming in MATLAB. This repository translates the concepts and techniques into Python, providing an accessible and modern alternative for structural analysis.

## Features

- Linear static analysis for bar members.
- Object-oriented implementation for modularity and extensibility.
- Comprehensive classes for:
  - Nodes
  - Elements (bars)
  - Materials
  - Loads (nodal, distributed, and concentrated)
  - Supports and boundary conditions
- Designed for scalability to handle complex structural systems.

## Requirements

- Python 3.8+
- Recommended libraries:
  - NumPy
  - Matplotlib
    Install dependencies via:

```bash
pip install -r requirements.txt
```

## Project Structure

```
strfem/
├── src/
│   ├── __init__.py
│   ├── str_controller.py        # Manages the FEM process
│   ├── str_line.py              # Defines bar elements
│   ├── str_load.py              # Handles loads
│   ├── str_material.py          # Material properties
│   ├── str_node.py              # Node definitions
│   ├── str_section.py           # Cross-sectional properties
│   └── ... (more FEM-related modules)
├── tests/
│   └── test_main.py           # Unit tests
├── README.md                     # Project documentation
└── requirements.txt              # Dependencies
```

## How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/Shubham-550/strfem.git
   cd strfem
   ```

2. Run the main FEM script:

   ```bash
   python src/str_controller.py
   ```

3. Modify input files or parameters to analyze different bar structures.

## Credits

This project is heavily inspired by the video series **"Programming the Finite Element Model"** by [Civil Engineering Essentials](https://www.youtube.com/@CivilEngineeringEssentials). The original series demonstrates the implementation of FEM in MATLAB for the linear static analysis of bar members. This project translates those concepts into Python to make them accessible to a wider audience.

Special thanks to Civil Engineering Essentials for the clear and detailed explanations in their videos.

## Contributing

Contributions are welcome! If you'd like to improve the code, add features, or fix bugs, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Happy coding and structural analysis!

README was created using ChatGPT
