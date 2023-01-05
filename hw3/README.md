# CME 211 - Homework #3

### Jesica Gonzalez


### Description

In computational fluid dynamics, usually we analyze the behaviour of objects called airfoils, which form the airplane wings and can be modelated as a set of points/coordinates. Depending on the angle of attack of the airfoil with respect to the air, the pressure coefficient changes in each of the points. This is important because a pressure coefficient close to 1 characterize a stagnation point. 
For each point, we can calculate the components of the lift force related to that angle. If we sum them together, we can obtain the lift coefficient for that angle of attack and that particular airfoil geometry. 

Therefore, the general parameters that characterize an airfoil is: geometry, angle of attack, lift coefficient and stagnation point.

We can model (abstract) an airfoil as an object with certain attributes/characteristics, decompose it by functions that act specificly on that object (methods) and encapsulate all of this through a class. 

In this assignment, a class Airfoil was created and imported from the main program main.py.

The class was design to contain 7 methods. One method (__str__)is used for generating a string with the desired data of the airfoil in the specified output formatting for printing. 
__init__ method initializes the arifoil and calls the additional methods.

The additional methods are:
    **parse_data(self):**
        """
            Read xy.dat and angles<degree>.dat files. 
            self.name is the name of the airfoil.
            self.points is a list of tuples with the airfoil coordinates. 

        """

    **compute_chord(self):**
        """
            Compute the chord of the given airfoil.
        """

    **get_cps_angles(self):**
        """
            Return a dictionary with angles as keys and pressure coefficients as values. 
            self.cps is the pressure coefficient dictionary.
            self.angles contains the angles of attack associated to the airfoil.
        """

    **get_cls(self):**
        """
            For each angle in self.angles, compute the corresponding lift coefficient (cl).
            self.cl_dic is a dictionary with angles as keys and each value corresponds to a list [cl, (x, y), cp_value (min substraction)]
        """
    
    **get_cl(self, angle):**
        """
            Compute the lift coefficient for the specified angle.
        """

In addition, an exception generation was implemented while reading the .dat files to provide the user a clearer description for the error when the specified file is not found in the given directory. This exception is rased before trying to open the file. The program accepts file paths both with and without trail delimiter.
