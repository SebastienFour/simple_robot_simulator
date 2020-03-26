import model

m = model.Model()

print("\nDefault model: {}\n".format(m))

print("#### Setting speed for one motor ####\n")
m.m1.speed = 0.1
print("## Settings ##\nmodel:  {}".format(m))
linear_speed, rotational_speed = m.dk()
print("\nlinear_speed={}\nrotational_speed={}\n".format(linear_speed, rotational_speed))

print("#### Setting same speed for both motors ####\n")
m.m1.speed = 0.1
m.m2.speed = 0.2
print("## Settings ##\nmodel:  {}".format(m))
linear_speed, rotational_speed = m.dk()
print("\nlinear_speed={}\nrotational_speed={}\n".format(linear_speed, rotational_speed))

def test_dk():
    
    if linear_speed == type(float) and linear_speed >= 0 :
        print("ok !")
        
    else:
        print("fail !")
        
    if rotational_speed == type(float) and linear_speed >= 0 :
        print("ok !")
        
    else :
        print("fail !")

def test_ik():
    
    if linear_speed == type(float) and linear_speed >= 0 :
        print("ok !")
    
    else :
        print("fail !")
        
    if rotational_speed == type(float) and linear_speed >= 0 :
        print("ok !")
    
    else :
        print("fail !")