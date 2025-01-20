import random
def doctorotp():
    u_c=[chr(i)for i in range(ord('A'),ord('Z')+1)]
    l_c=[chr(i)for i in range(ord('a'),ord('z')+1)]
    doctorotp=''
    for i in range(2):
        adminotp+=random.choice(u_c)
        adminotp+=str(random.randint(0,9))
        adminotp+=random.choice(l_c)
    return adminotp