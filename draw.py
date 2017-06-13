from display import *
from matrix import *
from math import *
from gmath import *
import random

def lighting(matrix, index, normal, shading, color):
    color = [0, 0, 0]

    if len(shading['constants']) > 0:
        for constant in shading['constants']:
            ka = [shading['constants'][constant]['red'][0], light_shading['constants'][constant]['green'][0], shading['constants'][constant]['blue'][0]]
            kd = [shading['constants'][constant]['red'][1], light_shading['constants'][constant]['green'][1], shading['constants'][constant]['blue'][1]]
            ks = [shading['constants'][constant]['red'][2], light_shading['constants'][constant]['green'][2], shading['constants'][constant]['blue'][2]]

    # print ka, ks, kd
    for c in range(3):

        # print light_shading
        location = shading['light']['l1']['location']
        intensity = shading['light']['l1']['color']

        if (len(light_shading['ambient']) > 0):
            ambient = ambient_color(shading['ambient'][c], ka[c])
        else:
            ambient = ambient_color(intensity[c], ka[c])

        color[c] += ambient

        diffuse = diffuse_color(intensity[c], kd[c], normal, location)
        color[c] += diffuse

        specular = specular_color(intensity[c], ks[c], normal, location)
        color[c] += specular

    for c in range(3):
        if color[c] > 255:
            color[c] = 255
        else:
            color[c] = int(round(color[c]))

    return color
# ====================================================================
def scanline_convert(polygons, index, zbuffer, screen, color, normal, shading):
    if len(shading['light']) > 0 or len(shading['ambient']) > 0:
        color = lighting(polygons, index, normal, shading, color)

    # separate x and y coordintaes
    x_values = [polygons[index + j][0] for j in range(3)]
    y_values = [polygons[index + j][1] for j in range(3)]
    z_values = [polygons[index + j][2] for j in range(3)]
    pos = [0, 1, 2]
    # print "X: " + str(x_values)
    # print "Y: " + str(y_values)

    # get indices of top and bottom
    b_ind = y_values.index(min(y_values))
    t_ind = y_values.index(max(y_values[::-1]))
    # print "B: " + str(b_ind)
    # print "T: " + str(t_ind)

    pos.remove(b_ind)
    pos.remove(t_ind)
    m_ind = pos[0]
    # print "M: " + str(m_ind)

    # get desired coordinates
    by = y_values[b_ind]
    ty = y_values[t_ind]
    my = y_values[m_ind]

    bx = x_values[b_ind]
    tx = x_values[t_ind]
    mx = x_values[m_ind]

    bz = z_values[b_ind]
    tz = z_values[t_ind]
    mz = z_values[m_ind]

    # draw lines
    x0 = bx
    z0 = bz
    if ty != by:
        dx0 = (tx - bx) / float(ty - by)
        dz0 = (tz - bz) / float(ty - by)
    else:
        dx0 = 0
        dz0 = 0

    x1 = bx
    z1 = bz
    if my != by:
        dx1 = (mx - bx) / float(my - by)
        dz1 = (mz - bz) / float(my - by)
    else:
        dx1 = 0
        dz1 = 0
    for y in range(int(by), int(my)):
        draw_line( int(x0),
                   int(y),
                   z0,
                   int(x1),
                   int(y),
                   z1,
                   zbuffer, screen, color)

        x0 += dx0
        x1 += dx1
        z0 += dz0
        z1 += dz1

    x1 = mx
    z1 = mz
    if ty != my:
        dx1 = (tx - mx) / float(ty - my)
        dz1 = (tz - mz) / float(ty - my)
    else:
        dx1 = 0
        dz1 = 0
    for y in range(int(my), int(ty)):
        draw_line( int(x0),
                   int(y),
                   z0,
                   int(x1),
                   int(y),
                   z1,
                   zbuffer, screen, color)

        x0 += dx0
        x1 += dx1
        z0 += dz0
        z1 += dz1

    return z0
	
def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0);
    add_point(polygons, x1, y1, z1);
    add_point(polygons, x2, y2, z2);

def draw_polygons( matrix, zbuffer, screen, color, shading ):
    if len(matrix) < 2:
        print 'Need at least 3 points to draw'
        return

    point = 0
    while point < len(matrix) - 2:

        normal = calculate_normal(matrix, point)[:]
        #print normal
        if normal[2] > 0:
            polygon_color = [50, 50, 50]

            scanline_convert(matrix, point, zbuffer, screen, polygon_color, normal, shading)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z);
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z);
  
    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1);
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1);
  
    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1);
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1);
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z);
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z);
  
    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1);
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z);
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z);
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1);

def add_sphere( edges, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)
    num_steps = int(1/step+0.1)
    
    lat_start = 0
    lat_stop = num_steps
    longt_start = 0
    longt_stop = num_steps

    num_steps+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            
            p0 = lat * (num_steps) + longt
            p1 = p0+1
            p2 = (p1+num_steps) % (num_steps * (num_steps-1))
            p3 = (p0+num_steps) % (num_steps * (num_steps-1))

            if longt != num_steps - 2:
	        add_polygon( edges, points[p0][0],
		             points[p0][1],
		             points[p0][2],
		             points[p1][0],
		             points[p1][1],
		             points[p1][2],
		             points[p2][0],
		             points[p2][1],
		             points[p2][2])
            if longt != 0:
	        add_polygon( edges, points[p0][0],
		             points[p0][1],
		             points[p0][2],
		             points[p2][0],
		             points[p2][1],
		             points[p2][2],
		             points[p3][0],
		             points[p3][1],
		             points[p3][2])

def generate_sphere( cx, cy, cz, r, step ):
    points = []
    num_steps = int(1/step+0.1)
    
    rot_start = 0
    rot_stop = num_steps
    circ_start = 0
    circ_stop = num_steps
            
    for rotation in range(rot_start, rot_stop):
        rot = step * rotation
        for circle in range(circ_start, circ_stop+1):
            circ = step * circle

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points
        
def add_torus( edges, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)
    num_steps = int(1/step+0.1)
    
    lat_start = 0
    lat_stop = num_steps
    longt_start = 0
    longt_stop = num_steps
    
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * (num_steps) + longt;
            if (longt == num_steps - 1):
	        p1 = p0 - longt;
            else:
	        p1 = p0 + 1;
            p2 = (p1 + num_steps) % (num_steps * num_steps);
            p3 = (p0 + num_steps) % (num_steps * num_steps);

            add_polygon(edges,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(edges,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )

def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    num_steps = int(1/step+0.1)
    
    rot_start = 0
    rot_stop = num_steps
    circ_start = 0
    circ_stop = num_steps

    print num_steps
    
    for rotation in range(rot_start, rot_stop):
        rot = step * rotation
        for circle in range(circ_start, circ_stop):
            circ = step * circle

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    t = step

    while t <= 1.00001:
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    t = step
    while t <= 1.00001:
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]
                
        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, zbuffer, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
		   int(matrix[point][2]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
		   int(matrix[point+1][2]),
                   zbuffer, screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, z0, x1, y1, z1, zbuffer, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
	zt = z0
        x0 = x1
        y0 = y1
	z0 = z1
        x1 = xt
        y1 = yt
	z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        wide = True
        loop_start = x
        loop_end = x1
        dx_E = dx_NE = 1
        dy_E = 0
        d_E = A
        distance = x1 - x
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_NE = 1
            d_NE = A + B
        else:         #octant 8
            d = A - B/2
            dy_NE = -1
            d_NE = A - B


    else: #octants 2/7
        tall = True
        dx_E = 0
        dx_NE = 1
        distance = abs(y1 - y)
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_E = dy_NE = 1
            d_NE = A + B
            d_E = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_E = dy_NE = -1
            d_NE = A - B
            d_E = -1 * B
            loop_start = y1
            loop_end = y
	
	
    while ( loop_start < loop_end ):
        plot( zbuffer, screen, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):
            x+= dx_NE
            y+= dy_NE
            d+= d_NE
        else:
            x+= dx_E
            y+= dy_E
            d+= d_E

        z += dz
        loop_start+= 1

    plot( screen, zbuffer, color, x, y, z )

#end draw_line
