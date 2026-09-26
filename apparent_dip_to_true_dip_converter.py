import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def compute_true_dip(app_dip_deg, app_dir_deg, strike_deg):
    """
    Convert apparent dip to true dip.
    Returns (true_dip_deg, true_dip_dir_deg, matplotlib_figure) on success,
    or None on invalid geometry (θ = 0°).
    """
    # Validate ranges
    if not (0 <= app_dip_deg <= 90):
        return None
    if not (0 <= app_dir_deg < 360):
        return None
    if not (0 <= strike_deg < 360):
        return None

    # Compute acute angle θ between apparent direction and strike
    delta = abs(app_dir_deg - strike_deg) % 180
    theta_deg = min(delta, 180 - delta)

    # Check for parallel case
    if theta_deg < 1e-9:
        return None

    # Convert to radians
    app_dip_rad = math.radians(app_dip_deg)
    theta_rad = math.radians(theta_deg)

    # Compute true dip
    true_dip_rad = math.atan(math.tan(app_dip_rad) / math.sin(theta_rad))
    true_dip_deg = math.degrees(true_dip_rad)
    # Clip to 0-90
    true_dip_deg = max(0.0, min(90.0, true_dip_deg))

    # Compute true dip direction (strike + 90°)
    true_dir_deg = (strike_deg + 90) % 360

    # Create 3D sketch
    fig = _create_sketch(app_dip_deg, app_dir_deg, strike_deg, theta_deg, true_dip_deg, true_dir_deg)

    return true_dip_deg, true_dir_deg, fig

def _create_sketch(app_dip_deg, app_dir_deg, strike_deg, theta_deg, true_dip_deg, true_dir_deg):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=25, azim=-60)

    # Coordinates: X east, Y north, Z up
    # Strike direction (line) along strike_deg from north (Y axis)
    strike_rad = math.radians(strike_deg)
    # Dip direction (true) is strike+90
    dip_dir_rad = math.radians((strike_deg + 90) % 360)

    # Planar geological structure: a rectangle dipping true_dip_deg
    # Dip direction vector on horizontal plane
    dip_x = math.sin(dip_dir_rad)
    dip_y = math.cos(dip_dir_rad)
    # Strike direction vector (perpendicular to dip)
    strike_x = math.sin(strike_rad)
    strike_y = math.cos(strike_rad)

    # Plane dimensions
    L = 2.0  # half-length along strike
    W = 1.5  # half-width down-dip

    # Corners of the plane: center at origin, sloping
    # Use strike and dip direction to define plane coordinates
    corners = []
    for s in [-1, 1]:
        for w in [-1, 1]:
            px = s * L * strike_x + w * W * dip_x
            py = s * L * strike_y + w * W * dip_y
            # Z from dip angle: actual dip down-dip = w*W * sin(dip), up-dip upward?
            # Actually, w negative (up-dip side) should be higher, w positive lower.
            pz = - w * W * math.sin(math.radians(true_dip_deg))
            corners.append([px, py, pz])
    # Order corners for a quad
    quad = [[corners[0], corners[1], corners[3], corners[2]]]  # ccw

    # Plot the plane as a semi-transparent surface
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    plane = Poly3DCollection(quad, alpha=0.3, facecolor='blue', edgecolor='k')
    ax.add_collection3d(plane)

    # Plot strike line (horizontal, along strike)
    ax.plot([-L*strike_x, L*strike_x], [-L*strike_y, L*strike_y], [0, 0],
            'k-', linewidth=2, label='Strike')

    # Plot true dip line from center down-dip
    ax.plot([0, W*dip_x], [0, W*dip_y], [0, -W*math.sin(math.radians(true_dip_deg))],
            'r-', linewidth=2, label='True dip')

    # Apparent dip line: vertical cross-section along apparent dip direction
    app_rad = math.radians(app_dir_deg)
    app_x = math.sin(app_rad)
    app_y = math.cos(app_rad)
    # Intersection of vertical plane with the dipping plane: line along apparent direction
    # For simplicity, draw a line on the plane surface from center to apparent dip projection
    # But easier: draw a line from center out along apparent direction on the plane surface
    # The plane equation: z = -tan(true_dip)* (x*cos(dip_dir_rad?) )
    # Actually dip direction: vector d = (sin(dip_dir_rad), cos(dip_dir_rad))
    # Plane: (x,y) dot d = (some t), z = -t * tan(true_dip)
    # For a given direction v = (sin(app_rad), cos(app_rad)), the t = t0 * (v·d)
    # So z = -t0*(v·d)*tan(true_dip) = -|v·d| * sqrt(x^2+y^2) * tan(true_dip)
    # But we can just sample a point along apparent direction on the plane.
    t0 = 1.0
    v_dot_d = (app_x*dip_x + app_y*dip_y)
    if abs(v_dot_d) > 1e-9:
        z_app = -t0 * v_dot_d * math.tan(math.radians(true_dip_deg))
        ax.plot([0, t0*app_x], [0, t0*app_y], [0, z_app],
                'g--', linewidth=2, label='Apparent dip')
    else:
        # Apparent direction perpendicular to dip direction? then apparent dip is horizontal? skip
        pass

    # Add angle annotations
    # True dip angle arc
    ax.text(0.2, 0.2, -0.3, f'θ = {theta_deg:.0f}°', color='blue')
    ax.text(0.8, 0.8, -0.6, f'δ = {true_dip_deg:.1f}°', color='red')

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 0.5])
    ax.set_xlabel('East')
    ax.set_ylabel('North')
    ax.set_zlabel('Up')
    ax.legend(loc='upper left')
    ax.set_title('3D Sketch of Planar Structure and Dips')

    plt.tight_layout()
    return fig
