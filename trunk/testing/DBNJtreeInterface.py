#don't have to import BayesNet, DiscreteDistribution, 
#or numarray because it is done in ExampleModels
import sys
sys.path.append('../dist/lib')
sys.path.append('../dist')
import examples.ExampleModels as EX
from pbnt.Inference import *
from pbnt.Utilities import *

def test():
    """ Constructs a DBN and uses the Jtree unrolled to perform inference on the model.
    """
    umbrellaDBN = EX.DBNUmbrella()
    for node in umbrellaDBN.nodes:
        if node.id == 1:
            rain = node
        if node.id == 2:
            umbrella == node
    
    #The number of time slices to unroll
    T = 5
    engine = JunctionTreeInterfaceEngine(umbrellaDBN, T)
    evI = [umbrella]*5
    evT = range(5)
    evV = [1,1,2,1,1]
    ev = zip(evI,evT)
    engine.evidence[ev] = evV
    
    Q = engine.marginal(rain, 3)
    