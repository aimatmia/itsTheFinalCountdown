import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands, symbols ) ==========
  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present
  If vary is found, but frames is not, the entire
  program should exit.
  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  jdyrlandweaver
  ==================== """
def first_pass( commands ):
    basename = "DEFAULT"
    num_frames = 0
    for c in commands:
        if c[0] == 'basename':
            basename = c[1]
        elif c[0] == 'frames':
            if len([x for x in commands if x[0] == 'basename'])== 0:
                print "Name is \"DEFAULT\""
            num_frames = int(c[1])
        elif c[0] == 'vary':
            if len([x for x in commands if x[0] == 'frames']) == 0:
                print "No frames with 'vary' -> Exiting."
    return (basename, num_frames)


"""======== second_pass( commands ) ==========
  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).
  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.
  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands, num_frames):
    frames = [ {} for i in range(num_frames) ]
    cons = {};
    sources = {};
    amb = {};
    shading = "none"

    for command in commands:
        if command[0] == 'vary':
            knob_name = command[1]
            start_frame = command[2]
            end_frame = command[3]
            start_value = float(command[4])
            end_value = float(command[5])
            value = 0

            if ((start_frame < 0) or
                (end_frame >= num_frames) or
                (end_frame <= start_frame)):
                print 'Invalid vary command for knob: ' + knob_name
                exit()

            delta = (end_value - start_value) / (end_frame - start_frame)

            for f in range(num_frames):
                if f == start_frame:
                    value = start_value
                    frames[f][knob_name] = value
                elif f >= start_frame and f <= end_frame:
                    value = start_value + delta * (f - start_frame)
                    frames[f][knob_name] = value
                #print 'knob: ' + knob_name + '\tvalue: ' + str(frames[f][knob_name])
    return frames


def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]

    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
    (basename, num_frames) = first_pass(commands)
    anime = num_frames > 1
    knobs = second_pass(commands, num_frames)

    #print symbols
    sources = [symbols[i][1] for i in symbols if symbols[i][0] = "light"]
    if "shading" in symbols:
        shading = symbols["shading"][1];
        
    for frame in range(num_frames):

      tmp = new_matrix()
      ident( tmp )

      stack = [ [x[:] for x in tmp] ]
      print "stack", stack[-1]
      screen = new_screen()
      zb = new_zbuffer()
      clear_zbuffer(zb);
      tmp = []
      step = 0.1
      val = 1  
    
      for command in commands:
          print "commmmand---", command
          c = command[0]
          args = command[1:]

          if c == 'box':
              add_box(tmp,
                      args[0], args[1], args[2],
                      args[3], args[4], args[5])
              matrix_mult( stack[-1], tmp )
              draw_polygons(tmp, zb, screen, color, symbols[command[-1]][1], sources, shading))
              tmp = []
          elif c == 'sphere':
              add_sphere(tmp,
                        args[0], args[1], args[2], args[3], step)
              matrix_mult( stack[-1], tmp )
              draw_polygons(tmp, screen, color)
              tmp = []
          elif c == 'torus':
              add_torus(tmp,
                        args[0], args[1], args[2], args[3], args[4], step)
              matrix_mult( stack[-1], tmp )
              draw_polygons(tmp, screen, color)
              tmp = []
              
          elif c == 'set':
              symbols[args[0]][1] = args[1]
          elif c == 'set_knobs':
              for knob in symbols:
                if symbols[knob][0] == 'knob':
                  symbols[knob][1] = args[0]
                  
          elif c == 'move':
              if anime and args[3] != None:
                      knob = args[3]
                      val = knobs[frame][knob]
              tmp = make_translate(args[0] * val,
                                  args[1] * val,
                                  args[2] * val)
              print tmp, stack[-1]
              matrix_mult(stack[-1], tmp)
              stack[-1] = [x[:] for x in tmp]
              tmp = []
          elif c == 'scale':
              if anime and args[3] != None:
                      knob = args[3]
                      val = knobs[frame][knob]
              tmp = make_translate(args[0] * val,
                                  args[1] * val,
                                  args[2] * val)
            
              matrix_mult(stack[-1], tmp)
              stack[-1] = [x[:] for x in tmp]
              tmp = []
          elif c == 'rotate':
              if anime and args[2] != None:
                      knob = args[2]
                      val = knobs[frame][knob]
              theta = args[1] * (math.pi/180) * val
            
              if args[0] == 'x':
                  tmp = make_rotX(theta)
              elif args[0] == 'y':
                  tmp = make_rotY(theta)
              else:
                  tmp = make_rotZ(theta)
              matrix_mult( stack[-1], tmp )
              stack[-1] = [ x[:] for x in tmp]
              tmp = []
          elif c == 'push':
              stack.append([x[:] for x in stack[-1]] )
          elif c == 'pop':
              stack.pop()
          elif c == 'display':
              display(screen)
          elif c == 'save':
              save_extension(screen, args[0])
            
          if anime:
              "%03d"%12
              save_extension(screen, "anim/%s%03d" % (basename, frame))    
