# deletion.py
import numpy as np
import pyvista as pv

class ClickToDelete:
    """Toggle a 'delete mode': click a registered line to remove it."""
    def __init__(self, plotter: pv.Plotter):
        self.p = plotter
        self.active = False
        self._counter = 0
        self._id_to_name = {}

    def add_line(self, a, b, color="magenta", line_width=6, name=None):
        """Create a deletable line, add it to the scene, and register it."""
        mesh = pv.Line(a, b)
        did = int(self._counter); self._counter += 1
        mesh.field_data["deletable_id"] = np.array([did], dtype=np.int64)  # travels with picked copy
        if name is None:
            name = f"conn_{did}"
        self.p.add_mesh(mesh, name=name, color=color, line_width=line_width, pickable=True)
        self._id_to_name[did] = name
        return name

    def _picked_mesh(self, *args):
        if args and isinstance(args[0], pv.DataSet):
            return args[0]
        return getattr(self.p, "picked_mesh", None)

    def _on_pick(self, *args):
        m = self._picked_mesh(*args)
        if m is None or "deletable_id" not in m.field_data:
            self._hint("[not deletable] click a magenta line")
            return
        did = int(m.field_data["deletable_id"][0])
        name = self._id_to_name.pop(did, None)
        if name:
            try: self.p.remove_actor(name)
            except Exception: pass
            self._hint("deleted")
        else:
            self._hint("not found")

    def _hint(self, msg):
        self.p.add_text(f"[Delete mode] {msg}\nClick a line to delete · press X to exit",
                        font_size=10, name="delete_hint")

    def enter(self):
        if self.active: return
        self.active = True
        self.p.disable_point_picking()
        self.p.enable_mesh_picking(callback=self._on_pick, left_clicking=True, show_message=True)
        self._hint("Click a line to delete")

    def exit(self):
        if not self.active: return
        self.active = False
        self.p.disable_mesh_picking()
        try: self.p.remove_actor("delete_hint")
        except Exception: pass
