import sys
import truss
import warnings

if len(sys.argv) <= 2:
    print('Usage:')
    print('  python3 {} [joints file] [beams file] [optional plot output file]'.format(sys.argv[0]))
    sys.exit(0)

joints_file = sys.argv[1]
beams_file = sys.argv[2]

try:
    a = truss.Truss(joints_file, beams_file)
except RuntimeError as e:
    print('RuntimeError: {}'.format(e))
    sys.exit(2)
try:
#     warnings.filterwarnings('error', category = scipy.sparse.linalg.dsolve.linsolve.MatrixRankWarning) # Catch warnings as exceptions
    a.solve_system() # Call system of equations solver
except RuntimeError as e:
    print('RuntimeError: {}'.format(e))
    sys.exit(2)

print(a)

if len(sys.argv) == 4:
    a.PlotGeometry(sys.argv[3]) # Create Plot
