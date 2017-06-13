import math

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]
    
    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N

def magnitude(v):
    return math.sqrt(sum([pow(component, 2) for component in v]))

def normalize(v):
    m = magnitude(v)
    return [component / float(m) for component in v]

def subtract_vector(v_one, v_two):
    diff = [0, 0, 0]
    for i in range(3):
        diff[i] = v_one[i] - v_two[i]

    return diff

def scalar_mult_two(v, scalar):
    return [component * scalar for component in v]

def dot_product(v_one, v_two):
    v_one = normalize(v_one)
    v_two = normalize(v_two)
    return v_one[0] * v_two[0] + v_one[1] * v_two[1] + v_one[2] * v_two[2]

def ambient_color(color, ka):
    return color * ka

def diffuse_color(color, kd, normal, light_vector):
    return color * kd * max(0, dot_product(normal, light_vector))

def specular_color(color, ks, normal, light_vector):
    P = scalar_mult_two(normal, dot_product(normal, light_vector))
    R = subtract_vector(scalar_mult_two(P, 2), light_vector)
    view_vector = [0, 0, 1]

    exp = 120
    return color * ks * pow(max(0, dot_product(R, view_vector)), exp)
