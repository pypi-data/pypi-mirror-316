# VisualShape3D

## About VisualShape3D
VisualShape3D is designed to facilitate the creation of 3D polygons for educational purposes. In this context, a 3D polygon is referred to as a 3D shape and is constructed through a systematic process:

1) A 2D polygon is created in the yz plane using a class called `Shape`, with specified parameters as follows:
   ```python
   from VisualShape3D.Shape3D import Shape
   shape1 = Shape('rectangle', W, H)
   shape2 = Shape('triangle', W, H, A)
   shape3 = Shape('rectangleWithHole', W, H, A, B, C, D)
   shape4 = Shape('fourSided', W, H, A, B)
   shape5 = Shape('fiveSided', W, H, A, B, C, D)
   shape6 = Shape('regularPolygon', n, R)
   shape7 = Shape('polygon', [(x1, y1), (x2, y2), ..., (xn, yn)])
   ```
   Once a 2D shape is created, its vertices are generated automatically.

2) The polygon is then transformed to a new position (X, Y, Z) while adopting a new orientation based on its facets. The transformation can be executed as follows:
   ```python
   shape1 = shape1.transform(to=(X, Y, Z), angles=(alpha1, beta1))
   ```
   Alternatively, it can be done in steps:
   ```python
   shape1 = shape1.transform(to=(X, Y, Z))
   shape1 = shape1.transform(alpha=alpha1)
   shape1 = shape1.transform(beta=beta1)
   ```
   The reference point for translation can be any 3D point; by default, the first vertex of the polygon serves as the reference point.

3) The results can then be visualized within the VisualShape3D framework, which is built upon Matplotlib:
   ```python
   from VisualShape3D.Visual import VisualShape3D
   vs3d = VisualShape3D()
   vs3d.add_shape(shape1)
   vs3d.show()
   ```

**Core Features**
The transformation process includes translation, which involves moving the reference point to a new 3D position, and rotation, which consists of adjusting the facets to a new direction about the Z-axis. The first vertex acts as the pivot point for these transformations, including rotation around the first edge. Notably, these operations are independent of one another.


## Requirements

* [Python](http://www.python.org) 3 
* Matplotlib is installed.

## Documentation

To be continued.

## Installation
```bash
pip install VisualShape3D
```

## Usage
```Python
import VisualShape3D.shapes as sp
sp.shapes()
```

```
from VisualShape3D.Shape3D import Shape 
W,H = 1, 0.7
shape1 = Shape('rectangle',W,H)
shape2 = shape1.transform(alpha = 30)
shape3 = shape2.transform(beta = 30)
shape4 = shape3.transform(to=(-0.5,-0.5,0))
```

```
%matplotlib notebook
from VisualShape3D import Visual as vm 
visual = vm.VisualShape3D({'facecolor':'yellow','alpha':0.7})
visual.add_shape(shape1,{'facecolor':'slategrey','alpha':0.7})
visual.add_shape(shape2,{'facecolor':'slategrey','alpha':0.7})
visual.add_shape(shape3,{'facecolor':'slategrey','alpha':0.7})
visual.add_shape(shape4,{'facecolor':'slategrey','alpha':0.7})
visual.show()
```

## Update log
`1.1.6` VisualShape3D.geometry -> VisualShape3D.Shape3D; VisualShape3D.VisualModels -> VisualShape3D.Visual
`1.0.7`  fix the bug of Shape_rectangleWithHole
`1.0.6`  Change the about VisualShape3D
`1.0.5`  Add "Modeling a house with shape" and "Building model" jupyter files


## License

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Contact
heliqun@ustc.edu.cn
