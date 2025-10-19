import numpy as np

def _rotz(deg: float) -> np.ndarray:
    th = np.deg2rad(deg); c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s, 0],
                     [s,  c, 0],
                     [0,  0, 1]], float)

class TowerFrustum:
    """Line-model frustum: base square -> top square at height H.
    Nodes = 4 top corners + 4 midpoints of side legs.
    """
    def __init__(self, base_side: float, top_side: float, height: float):
        self.b2, self.t2, self.H = base_side/2, top_side/2, float(height)
        # local squares (z=0 for base, z=H for top), CCW from (-x,-y)
        self.base = np.array([[-self.b2,-self.b2,0],[ self.b2,-self.b2,0],
                              [ self.b2, self.b2,0],[-self.b2, self.b2,0]], float)
        self.top  = np.array([[-self.t2,-self.t2,self.H],[ self.t2,-self.t2,self.H],
                              [ self.t2, self.t2,self.H],[-self.t2, self.t2,self.H]], float)
        # segments: 4 base edges + 4 top edges + 4 legs
        self._segs_local = (
            [(self.base[i], self.base[(i+1)%4]) for i in range(4)] +
            [(self.top[i],  self.top[(i+1)%4])  for i in range(4)] +
            [(self.base[i], self.top[i])        for i in range(4)]
        )
        # nodes: 4 top corners + 4 mid-leg midpoints
        leg_mid = (self.base + self.top) * 0.5
        self._nodes_local = np.vstack([self.top, leg_mid])

    def world(self, center=(0,0,0), angle_grads_y: float = 0.0):
        """Return (segments, nodes) in world coords.
        angle_grads_y: rotation in grads RELATIVE TO +Y axis.
        Internally converted to yaw from +X: yaw_deg = 90 - grads*0.9
        """
        yaw_deg = 90.0 - (angle_grads_y * 0.9)
        R, o = _rotz(yaw_deg), np.asarray(center, float)
        segs = [( (R@a)+o, (R@b)+o ) for (a,b) in self._segs_local]
        nodes = (R @ self._nodes_local.T).T + o
        return segs, nodes
