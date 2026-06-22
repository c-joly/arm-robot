import robot as rob
from math import cos,sin,pi,acos,atan2
import time
import numpy as np
from random import random,shuffle,randint
from scipy.integrate import solve_ivp

import pygfx as gfx
import pylinalg as la
import rendercanvas.auto



###########
# CONSTANTS
HEIGHT = 700
WIDTH = 700


# Load a robot
filename = "rob_alien.csv"
robot = rob.Robot(filename) # Robot for display
robot_grad = rob.Robot(filename) # Garbage for computing (and prevent display to be affected)



# Define the joint coordinates in a meshgrid format
l  = []
l_simple = []
N = 50 # Number of point per joint
t_end = 60
for joint in robot.joints:
    m,M = joint.data["limits"]
    if joint.data["type"]=="rotule":
        val = (np.linspace(m,M,N))
    else:
        val = np.linspace(m,M,max(round(N/20),4))
    val1 = val[0::2]
    val2 = val[1::2]
    val2 = val2[::-1]
    l_simple.append(val)
    val = np.concatenate((val1,val2))
    l.append(val)
l_ini = l.copy()
q = np.meshgrid(*l)
print(np.shape(q))
q = [item.flatten() for item in q]



print("Precomputing free space vizualisation - Please wait...")
precomp_free = set()
# Monte Carlo simulation
for i in range(round(WIDTH*HEIGHT/10)):
    for joint in robot_grad.joints:
        m,M = joint.data["limits"]
        joint.value = m+random()*(M-m)
    robot_grad.compute_chain()
    x,y,_ = robot_grad.end
    precomp_free.add((x,y,-.25))
    # radius = 2
    # for j in range(-radius,radius+1):
    #     for k in range(-radius,radius+1):
    #         xc = max(0,min(x+j,WIDTH-1))
    #         yc = max(0,min(y+k,HEIGHT-1))
    #         precomp_free.add((xc,yc,-10))
print("Done...")
# restore initial joint values







focus = 0 # Which joint is movable
print_free = True # By default we print the free space in green
automatic_free_space = False  # To generate a trajectory that scans all the joints values
automatic_trajectory = False  # To draw a predefined trajectory (rectangle currently) starting at the good initial condition
closed_loop_trajectory = False # Following the previous trajectory with arbitrary initial condition

# Two trajectory to  display
current_free_space = []  # Trajectory for scanning all the free space
current_traj = [] # For open / closed loop trajectories

auto_index = 0
angle = 0
stop = False


    
id = list(range(len(l)))   

dir = [True for _ in l_simple]
cur_id = 0
frame_traj = 0


canvas = rendercanvas.auto.RenderCanvas(title="Robot arm simulator")
renderer = gfx.renderers.WgpuRenderer(canvas)


freespace = gfx.Points(
    gfx.Geometry(positions=np.array(list(precomp_free)).astype(np.float32)),
    gfx.PointsMaterial(
        #thickness=1.0, 
        color=[0.0, 0.7, 0.3, 1.0],
    ),
)


def inverse_geom_RR(x,y):
    R2=x**2+y**2
    l0 = robot.joints[0].data["length"]
    l1 = robot.joints[1].data["length"]
    return(0,0)

 # Definition trajectoire de référence
# 0 et 20s
t0 = 0
tf = 40
""""""
l1 = robot.joints[0].data["length"]
l2 = robot.joints[1].data["length"]

def X_d(t):
    # X_d contient x_d et y_d
    return (0,0)


def q_d(t,q):
    return (0,0)

# Simuler pour obtenir q_ref grâce à q_d : bien prendre le dense_output.
X0 = None # Remplacer par la position initiale de la trajectoire compatible avec le modèle inverse

#result = solve_ivp(...)
#q_ref = result["sol"] """


class Timer:
    def __init__(self):
        self._t0 = None
        self._t = None

    def __call__(self):
        if self._t0 is None:
            self._t0 = time.perf_counter()
            self._t = self._t0
        t = time.perf_counter()
        self._t, dt = t, t - self._t
        return self._t - self._t0, dt


timer = Timer()

environment = gfx.Group().add(
    gfx.Background.from_color("#ffffff"),
    gfx.Grid(
        orientation="xy",
        material=gfx.GridMaterial(
            major_step=1.0,
            thickness_space="world",
            major_thickness=0.005,
            major_color="#000000",
            infinite=True,
        ),
    ),
)


def light(target):
    directional_light = gfx.DirectionalLight(intensity=3.0, target=target)
    directional_light.local.position = [-10.0, -10.0, 0.5]
    return gfx.Group().add(
        gfx.AmbientLight(intensity=2.0),
        directional_light,
    )

axes = []
for joint in robot.joints:
    axe = gfx.load_mesh("models/axe.stl")[0]
    axe.material = gfx.MeshPhongMaterial(color="#53565A")
    (x,y,alpha) = joint.data["pose"]
    axe.local.position = [x,y,0]
    axe.local.scale_x = joint.data["length"]
    axe.local.rotation = la.quat_from_axis_angle([0.0, 0.0, 1.0], alpha)
    axes.append(axe)



def camera():
    camera = gfx.OrthographicCamera()
    camera.local.position = [0.0, 0.0, 7.0]
    camera.show_pos(axes[0], up=[0, 1.0, 0.0])
    return camera


def register(event_handler):
    name = event_handler.__name__
    assert name.startswith("on_")
    event_name = name[3:]
    renderer.add_event_handler(event_handler, event_name)
    return event_handler


toggle_free = False
@register
def on_key_down(event):
    global focus,print_free,automatic_free_space,automatic_trajectory,auto_index,q,id,l,dir,cur_id
    global frame_traj,current_traj,closed_loop_trajectory,traj
    global toggle_free
    if event.key == "ArrowUp":
        robot.change_joint_value(focus,1)
    if event.key == "ArrowDown":
        robot.change_joint_value(focus,-1)
    if event.key == "ArrowLeft":
        focus = (focus-1) % len(robot.joints)
    if event.key == "ArrowRight":
        focus = (focus+1) % len(robot.joints)
    if event.key == "f":
        toggle_free = True
print_free = True

positions = []
def drawRobot():
    global toggle_free,print_free
    t,_ = timer()
    # Bloc de code spécifique robot RR pour la simulation de trajectoire
    if t<tf and False:
        robot.direct_Model(q_ref(t))
        pose = robot.end[0:2]
        positions.append(pose)
        #line.geometry.positions.set_data(np.array(np.array(positions),np.float32))
    for i,joint in enumerate(robot.joints):
        axes[i].material = gfx.MeshPhongMaterial(color="#53565A")
        (x,y,alpha) = joint.data["pose"]
        if joint.data["type"]=="rotule":
            alpha = alpha+joint.data["value"]
            length = joint.data["length"]
        else:
            length = joint.data["length"]+joint.data["value"]
        axes[i].local.position = [x,y,0]
        axes[i].local.scale_x = length
        axes[i].local.rotation = la.quat_from_axis_angle([0.0, 0.0, 1.0], alpha)
        if focus==i:
            axes[i].material = gfx.MeshPhongMaterial(color="#FF0000")
        else:
            axes[i].material = gfx.MeshPhongMaterial(color="#53565A")
    
    if toggle_free:
        freespace.visible = not freespace.visible
        toggle_free = False



scene = gfx.Scene().add(
    environment,
    light(target=axes[0]),
    *axes,
    freespace,
)

gfx.show(
    scene,
    renderer=renderer,
    camera=camera(),
    after_render=drawRobot,
)
