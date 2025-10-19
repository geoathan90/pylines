from pyvistaqt import BackgroundPlotter
import pyvista as pv
import numpy as np
from deletion import ClickToDelete

pv.set_plot_theme("dark")
p = BackgroundPlotter(window_size=(1000, 700))

# towers + pickable spheres at tops
for x, y, h, c in [(0,0,30,"cyan"), (40,10,25,"orange"), (80,-15,35,"lime")]:
    p.add_mesh(pv.Line((x,y,0),(x,y,h)), color=c, line_width=4, pickable=False)
    p.add_mesh(pv.Sphere(radius=.5, center=(x,y,h)), color=c, opacity=0.8, pickable=True)

p.add_mesh(pv.Plane(i_size=200, j_size=200), style="wireframe", color="dimgray", opacity=0.3, pickable=False)

pending = []
def on_pick(*args):
    # Try to get a 3D point from args; fall back to plotter.picked_point
    pt = None
    if args and hasattr(args[0], "__len__") and len(args[0]) == 3:
        pt = np.array(args[0], float)
    elif p.picked_point is not None:
        pt = np.array(p.picked_point, float)
    if pt is None or len(pt) != 3:
        return
    pending.append(pt)
    if len(pending) == 2:
        p.add_mesh(pv.Line(pending[0], pending[1]), color="magenta", line_width=6)
        pending.clear()

p.enable_point_picking(callback=on_pick, use_mesh=True, show_message=True, show_point=False, left_clicking=True)
p.add_key_event("x", lambda: pending.clear())
p.camera.position = (120,-120,80); p.camera.focal_point = (40,0,15); p.camera.zoom(1.2)
# p.app.exec_()  # uncomment if running outside Spyder

