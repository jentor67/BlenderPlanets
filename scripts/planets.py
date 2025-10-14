import bpy
import random
import math

class planet:
    def __init__(self):
        self.r = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.sma = 0
        self.i = 0 # Inclination (0 - 2pie)  -- Tilt of the orbit relative to a reference plane
        self.omega = 0 # Argument of periapsis (0-2pie) -- orientation of the ellipse within the orbital plane
        self.omegaC = 0 # Longitude of the ascending node (0-2pie)-- horizontal oientation
        self.upsilon = 0 # Ture anomaly (0-2pie) the body's position along the orbit

    def create(self,theName,position,theparent):   
        radiusStart = .4
        radiusEnd = .7
        distanceStart =-10
        distanceEnd = 10
        
        if position == "Center" :
            self.r = 1
            self.x = 0
            self.y = 0
            self.z = 0
            c1 = .906
            c2 = .878
            c3 = .104
        else:
            self.r = random.uniform(radiusStart, radiusEnd)
            self.i = random.uniform(0, 2*math.pi)
            self.omega = random.uniform(0, 2*math.pi)
            self.omegaC = random.uniform(0, 2*math.pi)
            self.upsilon = random.uniform(0, 2*math.pi)
            self.sma = random.uniform(2,10)

            # change by the omega and upsilon
            totalAngle = self.omega+self.upsilon
            self.x, self.y = self.rotate2DBody(self.sma, self.y, totalAngle)

            # change the inclination
            self.y, self.z = self.rotate2DBody(self.y, self.z, self.i)

            # change the longitude of ascending node
            self.x, self.y = self.rotate2DBody(self.x, self.y, self.omegaC)

            c1 = random.random()
            c2 = random.random()
            c3 = random.random()
            
            
        # Create a UV sphere
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=self.r, 
            location=(self.x, self.y, self.z),
            segments=32,
            ring_count=16
        )
        
        s1 = bpy.context.active_object
        s1.name =theName
        
        # Create a new material
        mat = bpy.data.materials.new(name="SphereMaterial")
        mat.use_nodes = True  # Use shader nodes

        # Access the Principled BSDF node
        bsdf = mat.node_tree.nodes["Principled BSDF"]

        # Change base color (RGBA)
        bsdf.inputs["Base Color"].default_value = (c1, c2, c3, 1)  # greenish color

        # Assign the material to the sphere
        if s1.data.materials:
            s1.data.materials[0] = mat
        else:
            s1.data.materials.append(mat)
        
        if position != "Center" :
            s1.parent = theparent 

        return s1 
   
    def rotate2DBody(self, x, y, rotation):
        xprime = x*math.cos(rotation) - y*math.sin(rotation)
        yprime = x*math.sin(rotation) + y*math.cos(rotation)

        return xprime, yprime
