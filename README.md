# Simulator: Generate hot water with solar panels

Authors: Forero Philippe, Germanier Johan, Henry Oscar, Feurgard Mael

## Python dependencies

The follow program need the following packages:

- PyQt5
- pyqtgraph
- superqt
- scipy
- numpy

Additionally, the following packages can be needed if one want to enable correct solar course computations for a solar panel
outside of the UTC+2 timezone:

- pytz
- tzwhere

## Setup

The program is based on the following files

- `main.py`: Entry point. Run this script to start the program. You can change the number of tabs opened here.
- `TabContent.py`: Core of the program. Describe the content of a tab and how its different elements interact with one another.
- `Section.py`: External code used to build the Section widget.
- `ParametersWidget.py`: Describe the widgets used to tune the parameters of the model (mostly sliders).
- `MeteoReader.py`: Used to parse and aggregate meteorological data, as well as display it.
- `Solarvizu.py`: Widget to display the solar panel (shape, inclination, orientation).
- `ResultsWidget.py`: Assemble the widgets used to display the results of the simulator.
- `PhysicsModel.py`: Script to compute the solar course and the shadow projected by a solar panel (and thus the energy it produces).
- `water.py`: Physical model used to compute how much water can be heated with a given amount of energy.
- `meteo.csv`: The default meteo file loaded. It has a header line (describe the content of each column) and two columns, one for the dates (accurate to the hour) and the other for the among of Wh/m^2 received on the ground during the said hour.

To run it, simply use `python main.py` (in a Python environment having the needed packages)