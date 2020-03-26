import model

m = model.Model()

def test_dk():
    
    print("\n### Test of dk function ###\n")
    
    print("\nDefault model: {}\n".format(m))
    
    print("#### Setting speed for one motor ####\n")
    m.m1.speed = 0.1
    print("## Current settings ##\nmodel:  {}".format(m))
    linear_speed, rotational_speed = m.dk()
    print("\nlinear_speed={}\nrotational_speed={}\n".format(linear_speed, rotational_speed))

    print("#### Setting same speed for both motors ####\n")
    m.m1.speed = 0.1
    m.m2.speed = 0.2
    print("## Current settings ##\nmodel:  {}".format(m))
    linear_speed, rotational_speed = m.dk()
    print("\nlinear_speed={}\nrotational_speed={}\n".format(linear_speed, rotational_speed))

    print("#### Setting opposed speed for both motors ####\n")
    m.m1.speed = 0.1
    m.m2.speed = -0.1
    print("## Current settings ##\nmodel:  {}".format(m))
    linear_speed, rotational_speed = m.dk()
    print("\nlinear_speed={}\nrotational_speed={}\n".format(linear_speed, rotational_speed))
    
    print("#### Setting speed of motor2 = 2 * motor1 ####\n")
    m.m1.speed = 0.1
    m.m2.speed = 0.2
    print("## Current settings ##\nmodel:  {}".format(m))
    linear_speed, rotational_speed = m.dk()
    print("\nlinear_speed={}\nrotational_speed={}\n".format(linear_speed, rotational_speed))
    
    m.m1.speed = 0
                    #resetting speeds
    m.m2.speed = 0

test_dk()


def test_ik():
    
    print("\n### Test of ik function ###\n")
    
    print("\nDefault model: {}\n".format(m))
    
    print("#### Setting linear speed ####\n")
    linear_speed = 0.1
    rotational_speed = 0
    print("## Current settings ##\nmodel:  {}".format(m))
    m1_speed, m2_speed = m.dk()
    print("\nm1_speed={}\nm2_speed={}\n".format(m1_speed, m2_speed))
    
    print("#### Setting rotational speed ####\n")
    linear_speed = 0
    rotational_speed = 0.1
    print("## Current settings ##\nmodel:  {}".format(m))
    m1_speed, m2_speed = m.dk()
    print("\nm1_speed={}\nm2_speed={}\n".format(m1_speed, m2_speed))
    
    print("#### Setting both linear and rotationnal speed ####\n")
    linear_speed = 0.1
    rotational_speed = 0.1
    print("## Current settings ##\nmodel:  {}".format(m))
    m1_speed, m2_speed = m.dk()
    print("\nm1_speed={}\nm2_speed={}\n".format(m1_speed, m2_speed))
    
test_ik()