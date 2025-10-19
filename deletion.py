import numpy as np

def _pt_seg_dist(p, a, b):
    p, a, b = map(np.asarray, (p, a, b))
    ab = b - a
    t = np.dot(p - a, ab) / (np.dot(ab, ab) + 1e-12)
    t = np.clip(t, 0.0, 1.0)
    return np.linalg.norm(p - (a + t * ab))

class Deleter:
    def __init__(self, plotter, connectors, tol=2.0):
        self.p = plotter
        self.conns = connectors   # list of dicts: {"actor": actor, "endpoints": (p0, p1)}
        self.tol = tol
        self.enabled = False
        self._note_name = "_delete_note"
        self.p.add_key_event("x", self.toggle)

    def toggle(self):
        self.enabled = not self.enabled
        if self.enabled:
            self.p.add_text("DELETE MODE: click a connector", font_size=10, name=self._note_name)
        else:
            try: self.p.remove_actor(self._note_name)
            except Exception: pass

    def handle_pick(self, pt):
        if not self.enabled:
            return False  # not handled
        # choose nearest connector by point-to-segment distance
        best_i, best_d = -1, np.inf
        for i, c in enumerate(self.conns):
            a, b = c["endpoints"]
            d = _pt_seg_dist(pt, a, b)
            if d < best_d:
                best_i, best_d = i, d
        if best_i >= 0 and best_d <= self.tol:
            try: self.p.remove_actor(self.conns[best_i]["actor"])
            except Exception: pass
            self.conns.pop(best_i)
        return True  # handled
