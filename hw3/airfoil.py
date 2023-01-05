import glob
import math
import os 



class Airfoil: # Define class
    
    def __init__(self, input_dir):
        if input_dir[-1] == '/': # Path with slash
            input_dir = input_dir[:-1] # Eliminate the final path slash 

        self.input_dir = input_dir # Relative or absolute path - string
        self.parse_data()
        self.compute_chord()
        self.get_cps_angles()
        self.get_cls()

    def parse_data(self):
        """
            Read xy.dat and angles<degree>.dat files. 
            self.name is the name of the airfoil.
            self.points is a list of tuples with the airfoil coordinates. 

        """
        
        dat_files_list = glob.glob(self.input_dir +'/*.dat') # Get .dat files
        xy = self.input_dir +'/xy.dat' # xy.dat path name

        if xy in dat_files_list: # Search xy.dat file in the path directory
            input_dir_xy = xy
        else: # Raise exception
            raise Exception("File {} not found in the specified path".format(self.input_dir +'/*.dat'))

        data_xy = open(input_dir_xy, "r") 
        xy_data_lines = data_xy.read().splitlines() # list containing all lines in xy.dat
        self.name = xy_data_lines[0] # Name of airfoil
        xy_points_str = xy_data_lines[1:] # List containing each line of panel coordinates
        xy_list = [] 
        for item in xy_points_str: # Iterate over the coordinates
            xy_str_list = item.split() # Create ['x', 'y'] for current line
            tuple_xy = tuple(map(float, xy_str_list)) # Create (x,y) tuple of floats
            xy_list.append(tuple_xy)
        self.points = xy_list # [(x1,y1), (x2,y2), ...]
        data_xy.close()


    def compute_chord(self):
        """
            Compute the chord of the given airfoil.
        """
        x_vals_list = []
        for coord in self.points:
            x_vals_list.append(coord[0]) # Get x values from coordinates
        max_x = max(x_vals_list)
        min_x = min(x_vals_list)
        chord = max_x - min_x # Compute chord
        self.chord = chord

    def get_cps_angles(self):
        """
            Return a dictionary with angles as keys and pressure coefficients as values. 
            self.cps is the pressure coefficient dictionary.
            self.angles contains the angles of attack associated to the airfoil.
        """
        directory_name = self.input_dir 
        angles_files = glob.glob(directory_name + '/alpha*.dat') # Search for files with format 'alpha<angle>.dat' in the specified path
        if len(angles_files) == 0 : # Raise exception
            raise Exception("File {} not found in the specified path".format(self.input_dir +'/alpha*.dat'))

        cp_dic = {}
        for angle_file in angles_files: # Work with each angle file
            file_contents = open(angle_file, "r")
            cp_data = file_contents.read().splitlines()[1:] # Get pressure coefficients without newlines
            angle_name = angle_file.split('alpha')[1][:-4] # Get the angle value from the file name
            cp_dic[angle_name] = [round(float(i.strip()),4) for i in cp_data] # Fill list values of angle key with pressure coefficients
            file_contents.close()
        self.cps = cp_dic 
        self.angles = cp_dic.keys()


    def get_cls(self):
        """
            For each angle in self.angles, compute the corresponding lift coefficient (cl).
            self.cl_dic is a dictionary with angles as keys and each value corresponds to a list [cl, (x, y), cp_value (min substraction)]
        """
        self.cl_dic = {}
        for angle in self.angles:
            cl = self.get_cl(angle)
            min_sub = 1 # Initialize minimum value between cp and 1.00
            pos_min_sub = 0 # Initialize position of coordinates of minimum value
            for i in range(len(self.cps[angle])): # Iteration over cp's values
                elem = self.cps[angle][i]
                subs = abs( elem - 1) # Compute substraction between cp and 1
                if subs < min_sub: # If substractiion is less than minimum value, replace the minimum.
                    min_sub = subs
                    pos_min_sub = i # Save the corresponding position index
            x_min = (self.points[pos_min_sub +1 ][0] + self.points[pos_min_sub][0])/2 # Compute mean val for x in minimum position
            y_min = (self.points[pos_min_sub +1 ][1] + self.points[pos_min_sub][1])/2 # Compute mean val for y in minimum position

            self.cl_dic[angle] = [cl, (round(x_min,4), round(y_min,4)), self.cps[angle][pos_min_sub]] # Assign dictionary value

            
                
    def get_cl(self, angle):
        """
            Compute the lift coefficient for the specified angle.
        """
        cx = 0
        cy = 0
        for i in range(len(self.points)-1): # Compute delta_x and delta_y
            delta_x = self.points[i+1][0] - self.points[i][0]
            delta_y = self.points[i+1][1] - self.points[i][1]

            cp = self.cps[angle][i] # Get associated cp value
            delta_cx = -cp*delta_y/self.chord # Compute delta_cx and delta_cy for those coordinates
            delta_cy = cp*delta_x/self.chord

            cx += delta_cx
            cy += delta_cy
        angle_rad = float(angle)*math.pi/180 # Covert angle to radians
        cl = cy*math.cos(angle_rad) - cx*math.sin(angle_rad) # Compute cl
        return round(cl,4)

    def __str__(self):
        """
            Create print method with the specified format. 
            Name of test case: 

            alpha     cl           stagnation pt      
            -----  -------  --------------------------

        """
        # Generate header
        general_string = str("Test Case: {} \n\n".format(self.name))
        general_string = general_string + "alpha     cl           stagnation pt      \n" + "-----  -------  --------------------------\n"

        angles_list = list(self.angles) # Get angles values in a list
        angles_int = [float(elem) for elem in angles_list]
        angles_sorted = sorted(angles_int) # Sort angles values

        for angle in angles_sorted: # Print angle value as string according to the sign (+ , - or zero)
            if angle > 0:
                general_string = general_string + "%5.2f" % (angle)
                angle_str = '+' + str(angle)
            elif angle == 0:
                general_string = general_string + "%5.2f" % (angle)
                angle_str = str(angle)
            else:
                general_string = general_string + "%5.2f" % (angle)
                angle_str = str(angle)
            
            # Generate string
            general_string = general_string + "  " + "%7.4f" % (self.cl_dic[angle_str][0]) + "  ( " + "%6.4f" % (self.cl_dic[angle_str][1][0]) + ",  " + "%6.4f" % (self.cl_dic[angle_str][1][1]) + ")  " + "%6.4f" % (self.cl_dic[angle_str][2]) + "\n"
        return general_string

        







