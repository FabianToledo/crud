class ClaseE:

    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

    def __str__(self):
        return "{},{}".format(self.n1,self.n2)

def mult(vo):
    vo.n1 = vo.n1 * 2 
    
    vo.n2 = vo.n1 * 3
    
    return (vo.n1,vo) 

x = [
    ClaseE(1,0),
    ClaseE(2,0),
    ClaseE(3,0)
]


for i in x:
    print(i)

b=map(mult,x)
l=filter(mult,x)
ko=list(l)
c=dict(b)

for k,v in c.items():
    print(k,v)

for z in ko:
    print(z)



