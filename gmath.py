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

def colorize(normal, shading, color):
    ambient = ambient_color(shading, color)
    diffuse = diffuse_color(normal, shading, color)
    specular = specular_color(normal, shading, color)
    print ambient, '|', diffuse, '|', specular
    I = [ambient[0] + diffuse[0] + specular[0],
         ambient[1] + diffuse[1] + specular[1],
        ambient[2] + diffuse[2] + specular[2]]
    return [int(max(min(x, 255), 0)) for x in I]

def ambient_color(shading, color):
    src_color = shading["ambient"]
    const = shading["constants"]["constants"]
    amb_const = [ const["red"][0], const["green"][0], const["blue"][0] ]
    #color * ka 
    ambient = [ amb_const[0] * src_color[0], #R
                amb_const[1] * src_color[1], #G
                amb_const[2] * src_color[2] ] #B
    return ambient 

def diffuse_color(normal, shading, color):
    #color * kd * max(0, dot_product(normal, light_vector))
    const = shading["constants"]["constants"]
    diff_const = [ const["red"][1], const["green"][1], const["blue"][1] ]

    normal = normalize(normal)

    total_diffuse = [0, 0, 0]
    for entry in shading["light"]:
        light_src = shading["light"][entry]
        source = light_src['color'] 
        location = light_src['location'] 
        dot_prod = dot_product(normal, location)

        diffuse = [ source[0] * diff_const[0] * dot_prod,
                    source[1] * diff_const[1] * dot_prod,
                    source[2] * diff_const[2] * dot_prod ]
        total_diffuse = [ total_diffuse[0] + diffuse[0],
                          total_diffuse[1] + diffuse[1],
                          total_diffuse[2] + diffuse[2] ]
    return total_diffuse
def specular_color(normal, shading, color):
    #P = scalar_mult_two(normal, dot_product(normal, light_vector))
    #R = subtract_vector(scalar_mult_two(P, 2), light_vector)
    #return color * ks * pow(max(0, dot_product(R, view_vector)), exp)

    const = shading["constants"]["constants"]
    specular_const = [ const["red"][1], const["green"][1], const["blue"][1] ]

    normal = normalize(normal)

    total_specular = [0, 0, 0]
    for entry in shading["light"]:
        light_src = shading["light"][entry]
        source= light_src["color"]
        location = light_src["location"]
        dot_prod = dot_product(normal, location)

        a = [2 * dot_prod * x for x in normal]
        b = [ a[0] - location[0],
              a[1] - location[1],
              a[2] - location[2] ]
        b = normalize(b)
        view = normalize([1, 1, 1])
        c = dot_product(b, view)
        
        specular_r = source[0] * specular_const[0] * c
        specular_g = source[1] * specular_const[1] * c
        specular_b = source[2] * specular_const[2] * c

        total_specular = [ total_specular[0] + specular_r,
                           total_specular[1] + specular_g,
                           total_specular[2] + specular_b ]

    return total_specular
