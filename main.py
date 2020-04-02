from model.neuro import Net
from .simulator import *
from .GA import *

net = Net(2, 4)
net.randomize()
net.save("", "net2")
net.show()
print(net.run([[2.14], [2.14], [2.14], [2.14]]))
