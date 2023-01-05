#include <iostream>
#include <fstream>
#include <string>



// Define constants to size the static array
#define ni 210
#define nj 210 
// Define directions of movement through the array
#define North 0
#define West 1
#define South 2
#define East 3


using namespace std;

int main(int argc, char** argv){ 

    if (argc < 3) {
        cout << "Usage: \n" << argv[0] << " " << "<maze file>" << " "<< "<solution file> \n" << endl;
        return 1;
    }

    int a[ni][nj] = {0}; // Initialize static array

    // Get files from uer input
    string filename_maze = argv[1]; 
    string filename_solution = argv[2];

    ifstream maze; // Declare storage for input file
    ofstream f; // Declare storage for output file

    int rows, cols; // Stores total number of rows and columns in maze file
    int row, col; // Moves through rows and columns

    maze.open(filename_maze.c_str()); 
    if (maze.is_open()){
        maze >> rows >> cols; // read the size of maze
        
        if (rows > 210 or cols > 210){ // Check if maze exceeds limits
            cout << "Not enough storage available" << endl;
            return 0; // quit the program

        }

        while (maze >> row >> col) { // Read each line of the file
            a[row][col] = 1; // Set each entry in row, col index to 1
            // cout << row << ' ' << col << endl;
        }
    
       maze.close();
        
    } else {
        cout << "Failed to open maze file" << endl;
    }
    
    int d = South; // Direction of movement facing south
    int i = 0; // Row index
    int j = 0; // Column index
    int initial_i = 0; // Row of maze entry
    int initial_j; // Column of maze entry
    int next_i; // Row index for next step
    int next_j; // Column index for next step
    int right_i; // Row index of right side entry
    int right_j; // Column index of right side entry
    int turn_verification = 0; // Debugging tool to count number of turns in direction. Max 4 turns within {0,1,2,3} values.

    for (int k = 0; k < cols; k++){ // Find first no-wall coordinate
        if (a[0][k] != 1){
            initial_j = k; // Set column index of maze entry 
            break;
        }
    }

    // Initial coordinates
    i = initial_i;
    j = initial_j;
    //cout << "initial i = " << initial_i << ' ' << "j = " << initial_j << endl;

    f.open(filename_solution.c_str());
    if (f.is_open()) {

        f << i << ' ' << j << endl; // Write maze entry coordinate
            
        while (i < rows-1 and turn_verification < 5) {
            bool right_free = false; // Entry of maze is just one entry in the first row. Right side initially is always a wall.
            turn_verification = 0; 
            while (!right_free and turn_verification < 5){ // While there is a wall at the right and turn_verification is no more than a full anticlockwise turn.
                switch(d){ // Evaluate depending on current facing direction
                    case North :
                        // cout << "Case: " << North << endl;
                        right_i = i; // Coordinates of next step
                        right_j = j+1;

                        if (right_j < cols && a[right_i][right_j] != 1){ // Index within limits and no wall at the right
                            d = East; // update direction to right side
                            next_i = right_i; // update movement coordinates
                            next_j = right_j;
                            right_free = true; // Right side is free
                        } else {
                            d = West; // update direction to opposite side (anti-clockwise)
                            right_free = false; // Right side is not free (wall)
                        }
                        // cout << "right_free: " << right_free << endl;
                        break;

                    case West :
                        // cout << "Case: " << West << endl;
                        right_i = i-1;
                        right_j = j;

                        if (right_i >= 0 && a[right_i][right_j] != 1){
                            d = North; // update direction
                            next_i = right_i;
                            next_j = right_j;
                            right_free = true;
                        } else {
                            d = South; // update direction
                            right_free = false;
                        }
                        // cout << "right_free: " << right_free << endl;
                        break;

                    case South :
                        // cout << "Case: " << South << endl;
                        right_i = i;
                        right_j = j-1;

                        if (right_j >= 0 && a[right_i][right_j] != 1){
                            d = West; // update direction
                            next_i = right_i;
                            next_j = right_j;
                            right_free = true;
                        } else {
                            d = East; // update direction
                            right_free = false;
                        }
                        // cout << "right_free: " << right_free << endl;
                        break;

                    case East :
                        // cout << "Case: " << East << endl;

                        right_i = i+1;
                        right_j = j;

                        if (right_i < rows && a[right_i][right_j] != 1){
                            d = South; // update direction
                            next_i = right_i;
                            next_j = right_j;
                            right_free = true;
                        } else {
                            d = North; // update direction
                            right_free = false;
                        }
                        // cout << "right_free: " << right_free << endl;
                        // cout << "right_i: " << right_i << "right_j: " << right_j << endl;
                        break;
                }
                turn_verification++; // Count current turn
            }        
            

            if (right_free){
                i = next_i; // move to next coordinates
                j = next_j;
                // cout << i << ' ' << j << endl; 
                f << i << ' ' << j << endl; // write step coordinates to output file
            } 
        }

    } else{
            cout << "Failed to open output file" << endl;
    }
    f.close();
    
    // cout << "Turn Verification = " << turn_verification << endl; 

    return 0;
}   