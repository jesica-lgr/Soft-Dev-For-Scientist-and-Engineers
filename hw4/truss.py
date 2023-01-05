import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
import warnings
import matplotlib


class Truss:
    """
        This class loads and analyze a 2D truss using the method of joints. If a third user input is given, then a plot is generated and saved in the specified file path.
    """

    def __init__(self, joints_file, beams_file):
        self.joints = {} # Dict. where each key is a joint with values [(x,y) (Fx, Fy), zerodisp]
        self.beams = {} #  Dict. where each key is a beam with associated joints as values (Ja, Jb).
        self.joints_file = joints_file
        self.beams_file = beams_file
        self.n_joints = 0 # Number of joints
        self.n_beams = 0 # Number of beams
        self.n_zerodisp = 0 # Number of fixed joints
        self.zerodisp_joints = [] # Fixed joints
        self.n_unknowns = 0 # Number of unknowns
        self.n_eqs = 0 # Number of equations
        self.bxy = {} # Dict. where each key is a beam with values (bx,by)
        self.joint_beams = {}
        self.parse_data() 
        self.compute_beamsxy()
        self.compute_beamsPerJoint()
        self.compute_sparsematrix()
        # if warnings.filterwarnings('error'):
        #     raise Exception("Matrix is singular") 
        # raise warnings.filterwarnings('error')
        self.X = self.solve_system()
        # try:
        #     warnings.filterwarnings('error') # Catch warnings as exceptions
        #     self.X = self.solve_system()
        # except scipy.sparse.linalg.dsolve.linsolve.MatrixRankWarning as e:


    def parse_data(self):
        """
            Read joints.dat and beams.dat files from specified truss# directory.
        """
        joints_f = open(self.joints_file, "r")
        joints_list = joints_f.read().splitlines()[1:] # Discart column names
        joints_list = [list(map(float, elem.split())) for elem in joints_list] # Get each joint name as an integer
        self.n_joints = len(joints_list)
        
        for joint in joints_list: # Organize the data of each line in the joints dictionary
            self.joints[int(joint[0])]  = [(joint[1], joint[2]), (joint[3], joint[4]), joint[5]]
            if joint[5] == 1: # If it is a rigid/fixed joint, count it
                self.n_zerodisp += 1 
                self.zerodisp_joints.append(int(joint[0]))
        
        beams_f = open(self.beams_file, "r")
        beams_list = beams_f.read().splitlines()[1:] # Discart column names
        beams_list = [list(map(int, elem.split())) for elem in beams_list] # Get each beam name as an integer
        self.n_beams = len(beams_list)

        for beam in beams_list: # Organize the data of each line in the beams dictionary
            self.beams[int(beam[0])]  = (beam[1], beam[2])

        joints_f.close()
        beams_f.close()

        self.n_unknowns = self.n_beams + 2*(self.n_zerodisp) 
        self.n_eqs = 2*(self.n_joints)

        if self.n_unknowns < self.n_eqs: # Underdetermined system
            raise RuntimeError("Truss geometry not suitable for static equilibrium analysis. System is underdetermined.")
        elif self.n_unknowns > self.n_eqs: # Overdetermined system
            raise RuntimeError("Truss geometry not suitable for static equilibrium analysis. System is overdetermined.")

    def compute_beamsxy(self):
        """
            Compute the components Bx and Bx of each beam force B1, B2, ..., etc., and store them in a dictionary. 
            self.bxy = {'beam_number': (Bx, By); ...}
        """
        for beam in self.beams.keys(): # Get extremal joints for each beam
            Ja = self.beams[beam][0]
            Jb = self.beams[beam][1] 
            Jb_pos = np.asarray(self.joints[Jb][0]) # Get xy positions for joint a and b and save in an array
            Ja_pos = np.asarray(self.joints[Ja][0])
            J_diff = Jb_pos.transpose() - Ja_pos.transpose() # Compute joints positions differece
            numerator_x = J_diff[0] # get x components of the joints difference
            numerator_y = J_diff[1] # get y components of the joints difference
            denominator = np.sqrt(J_diff.dot(J_diff.transpose()))
            bx = numerator_x/denominator
            by = numerator_y/denominator
            self.bxy[beam] = np.array([bx, by]) # x and y components of the beam

    
    def compute_beamsPerJoint(self):
        """
            Store the intersecting beams per joint, and store them in a dictionary. 
            self.joint_beams = {'joint': [B1, B2, ..]; ...}
        """

        for joint in self.joints.keys(): 
            self.joint_beams[joint] = []
            for beam in self.beams.keys():
                if joint in self.beams[beam]: # Joint is on one of the beams' sides
                    self.joint_beams[joint].append(beam)

    def compute_sparsematrix(self):
        """
            Compute the sparse matrix in a csr matrix format.
        """
        count_vals = 0 # Total number of non-zero elements in the previous rows
        self.cols = [] # List that stores columns indexes for non-zero values in the matrix
        self.data = [] # List that stores non-zero values in the matrix
        self.row_pointer = [] # List that stores count_vals for each row
        self.f = [] # List that stores force components FX, Fy in each joint
        for joint in self.joints.keys(): 
            associated_beams = self.joint_beams[joint] 
            associated_rows = ((joint*2)-2, (joint*2)-1) # Rows indexes for corresponding joints equations
            
            for i in range(2): # Move between pair of associated equations
                self.f.append(self.joints[joint][1][i]) # Append force component
                for beam in associated_beams: # Organize Bx or By for each beam associated to the current joint
                    self.data.append(self.bxy[beam][i]) # Append Bx or By
                    self.cols.append(beam-1) # Append corresponding column index

                if self.joints[joint][2] == 1: # Joint is a fixed joint i.e has associated unknowns Rx, Ry
                    self.data.append(1) # Consider R coefficient in the equation
                    index = self.zerodisp_joints.index(joint) # Index of current joint in the zerodisp_joints list
                    cols_index_R = self.n_beams + 2*index + i # Compute column index correspoding to R (Rx or Ry)
                    self.cols.append(cols_index_R) 
                    n_unknowns_row = len(associated_beams) + 1 # Number of unknowns in current row i considering the R

                else:
                    n_unknowns_row = len(associated_beams) # Number of unknowns in current row i (no unknown R)
                self.row_pointer.append(count_vals) # Append total non-zero values for pasts rows
                count_vals = count_vals + n_unknowns_row # Update (sum number of unknowns in current row)
        self.row_pointer.append(count_vals)
        self.data = np.array(self.data)
        self.cols = np.array(self.cols)
        self.row_pointer = np.array(self.row_pointer)
        self.f = np.array(self.f)
        self.M = scipy.sparse.csr_matrix((self.data, self.cols, self.row_pointer), shape=(self.n_eqs, self.n_unknowns)) # Create csr matrix

    def solve_system(self):
        """
            Solve system of equations from sparse matrix (self.M) and known forces per joint (self.f).
        """
        # print("Printing error: {}".format(warnings.filterwarnings('error', category=scipy.sparse.linalg.dsolve.linsolve.MatrixRankWarning))) # Catch warnings as exceptions
        # if warnings.filterwarnings('error') != None:
        #     raise Exception("Matrix is singular")  

        # with warnings.catch_warnings():
        #     warnings.filterwarnings('error')
        # #     raise RuntimeError("Singular Matrix")
        # Sorry, warnings never worked :( 
        MM = self.M.todense()
        if np.linalg.det(MM) == 0: # raise Exception("Matrix is singular") 
            raise RuntimeError("Singular Matrix")
    
        X = scipy.sparse.linalg.spsolve(self.M, self.f)

        return X

    def PlotGeometry(self, output_path):
        """
            Compute the sparse matrix in a csr matrix format.
        """

        x = [0]*self.n_beams*2
        y = [0]*self.n_beams*2

        for beam in self.beams.keys():
            J_a = self.beams[beam][0]
            J_b = self.beams[beam][1]
            x_a = self.joints[J_a][0][0]
            y_a = self.joints[J_a][0][1]
            x_b = self.joints[J_b][0][0]
            y_b = self.joints[J_b][0][1]

            x[2*beam-2] = x_a
            x[2*beam-1] = x_b
            y[2*beam-2] = y_a
            y[2*beam-1] = y_b

        plt.plot(x, y)
        plt.gca().margins(0.05,0.05)
        plt.savefig(output_path)

    def __repr__(self):
        """
            Create print method with the specified format. 

             Beam       Force    
            -----------------

        """
        # Generate header
        general_string = " Beam       Force\n" + "-----------------\n"

        for beam in self.beams.keys(): # Print angle value as string according to the sign (+ , - or zero)
            if self.X[beam - 1] < 0:
                general_string = general_string + "    {}".format(beam) + "      %4.3f" % (self.X[beam - 1]) + "\n"
            else:
                general_string = general_string + "    {}".format(beam) + "       %4.3f" % (self.X[beam - 1]) + "\n"

        return general_string

