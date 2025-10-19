from pyvistaqt import BackgroundPlotter
import pyvista as pv
import numpy as np
from deletion import Deleter
from tower_frustum import TowerFrustum


pv.set_plot_theme("dark")
p = BackgroundPlotter(window_size=(1000, 700))

# =============================================================================
# # towers + pickable spheres at tops
# for x, y, h, c in [(0,0,30,"cyan"), (40,10,25,"orange"), (80,-15,35,"lime")]:
#     p.add_mesh(pv.Line((x,y,0),(x,y,h)), color=c, line_width=4, pickable=False)
#     p.add_mesh(pv.Sphere(radius=.05, center=(x,y,h)), color=c, opacity=0.8, pickable=True)
# =============================================================================

Z = TowerFrustum(base_side=15, top_side=10, height=20)
R = TowerFrustum(base_side=12, top_side=8,  height=28)

for (tw, center, grads, color) in [
    (Z, (398285, 4358426, 0),   0,   "cyan"),     
    (R, (398185, 4358626, 0), 10,  "orange"),
    
]:
    segs, nodes = tw.world(center=center, angle_grads_y=grads)
    for a, b in segs:
        p.add_mesh(pv.Line(a, b), color=color, line_width=3, pickable=False)
    p.add_mesh(pv.PolyData(nodes), render_points_as_spheres=True, point_size=12, color="yellow", pickable=True)


p.add_mesh(pv.Plane(i_size=200, j_size=200), style="wireframe", color="dimgray", opacity=0.3, pickable=False)


connectors = []   # will store {"actor": actor, "endpoints": (p0, p1)}
deleter = Deleter(p, connectors, tol=2.0)
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
    # deletion hook: eat the click if in delete mode
    if deleter.handle_pick(pt):
        return
    pending.append(pt)
    if len(pending) == 2:
        actor = p.add_mesh(pv.Line(pending[0], pending[1]), color="magenta", line_width=6, pickable=True)
        connectors.append({"actor": actor, "endpoints": (pending[0].copy(), pending[1].copy())})
        pending.clear()

p.enable_point_picking(callback=on_pick, use_mesh=True, show_message=False, show_point=False, left_clicking=True)
#p.add_key_event("x", lambda: pending.clear())
p.camera.position = (120,-120,80); p.camera.focal_point = (40,0,15); p.camera.zoom(1.2)
# p.app.exec_()  # uncomment if running outside Spyder

