#include <sstream>
#include <stdexcept>
#include <string>
#include <iostream>
#include <cstdio>
#include <vector>
#include <cmath>
#include <typeinfo>


#define BOOST_DISABLE_ASSERTS
#include <boost/multi_array.hpp>
#include <jpeglib.h>
#include "jpeglib.h"

#include "hw6.hpp"
#include "image.hpp"

// Define position of the each entry in the submatrix (one submatrix per input's entry). Inside: entry is inside the input image. Outside positive: entry is outside the input's image bounds and to the right or down direction. Outside negative: entry is outside the input's image bounds and to the left or up direction.
#define Inside 0
#define OutsidePositive 1
#define OutsideNegative 2

// Class Image Constructor
Image::Image(std::string filename) {

    initial_filename = filename; // Image filename
    ReadGrayscaleJPEG(filename, img); // Read image and store it in img boost array
}

void Image::Save(std::string filename){
    if (filename.size() == 0){ // Use initial filename if no output filename is given
        WriteGrayscaleJPEG(initial_filename, img);
    } else { // Output final is given
        WriteGrayscaleJPEG(filename, img);
    }
}


void Convolution(boost::multi_array<unsigned char,2>& input, 
                    boost::multi_array<unsigned char,2>& output,
                    boost::multi_array<float,2>& kernel){
    // Check if kernel size is odd
    if (kernel.shape()[0]%2 == 0) {
        std:: cout << "Kernel size must be odd" << std:: endl;
        exit(0);
    } else if (kernel.shape()[0] < 3) { // Check if kernel size is greater than 3
        std:: cout << "Kernel size must be at least 3." << std:: endl;
        exit(0);
    }

    // Get kernel and input image sizes
    long unsigned int rows_kernel = kernel.shape()[0];
    long unsigned int cols_kernel = kernel.shape()[1];
    long unsigned int rows_input = input.shape()[0];
    long unsigned int cols_input = input.shape()[1];

    // Create a boost multiarray submatrix of same size as the kernel
    boost::multi_array<unsigned char,2> submatrix(boost::extents[rows_kernel][cols_kernel]);

    // For each entry in the image, compute the corresponding subarray values and fill the corresponding submatrix. Then perfom the convolution operation with each of the kernel's entries.

    for (unsigned int current_i=0; current_i< rows_input; current_i++){
        for (unsigned int current_j = 0; current_j < cols_input; current_j++){
           Create_subarray(input, submatrix, rows_kernel, cols_kernel, rows_input, cols_input, current_i, current_j); // Subarray contains unsigned chars in the range 0 - 255

            float sum_values = 0.; // Store convolution resulting value 
             // Perform element wise matrix multiplication
            for (unsigned int i=0; i< rows_kernel; i++){
                for (unsigned int j = 0; j < cols_kernel; j++){
                    sum_values += static_cast<float>(submatrix[i][j])*kernel[i][j];
                }
            }

            // Cast values to unsigned char range.
            if (sum_values < 0.){
                sum_values = 0.;
            } else if (sum_values > 255.){
                sum_values = 255.;
            } else {
                sum_values = (float)floor(sum_values);
            }
            
            output[current_i][current_j] = (unsigned char)(sum_values); // assign new value for current position in output multiarray

            
        }
    }
}

void Create_subarray(boost::multi_array<unsigned char,2>& input, boost::multi_array<unsigned char,2>& submatrix, long unsigned int rows_kernel,  long unsigned int cols_kernel,  long unsigned int rows_input,  long unsigned int cols_input,  unsigned int current_i, unsigned int current_j){
    
    long unsigned int k = (rows_kernel - 1) /2; // Number of out of bounds cols and rows for current kernel
    
    // Determine position in the image of each of the submarray´s entries
    for (unsigned int i=0; i< rows_kernel; i++){
        for (unsigned int j = 0; j < cols_kernel; j++){
            int position_i;
            int position_j;

            // Entry's row value (subarray) is inside the image boundaries
            if ((current_i + i) >= k and (current_i + i) < (rows_input + k)){
                position_i = Inside;
            } else if ((current_i + i ) > k and current_i + i >= (rows_input + k)){ // Entry's row value is outside down from the image boundaries
                position_i = OutsidePositive;
            } else { // Entry's row value is outside up from the image boundaries
                position_i = OutsideNegative;
            }

            // Entry's column value (subarray) is inside the image boundaries
            if ((current_j + j )>= k and (current_j + j) < (cols_input + k)){
                position_j = Inside;
            } else if ((current_j + j) >= k and (current_j + j) >= (cols_input + k)){ // Entry's column value is outside right from the image boundaries
                position_j = OutsidePositive;
            } else { // Entry's column value is outside left from the image boundaries
                position_j = OutsideNegative;
            }

            // Relate kernel's entry with subarray's entry of current ij image position. Then, assign the corresponging input value to the submatrix.
            long unsigned int related_i = current_i - k + i; // Row position in kernel
            long unsigned int related_j = current_j - k + j; // Column position in kernel
            if (position_i == Inside) { // Submarray's row is inside input's image
                if (position_j == Inside){ // Submarray's column is inside input image i.e. submatrix gets the same related ij input's value 
                    submatrix[i][j] = input[related_i][related_j];
                } else if (position_j == OutsideNegative){ // Same value as previous column (left boundary).
                    submatrix[i][j] = input[related_i][0];
                } else if (position_j == OutsidePositive){ // Same value as previous column (right boundary).
                    submatrix[i][j] = input[related_i][cols_input -1];
                }

            } else if (position_i == OutsideNegative){ // Submarray's row is outside - up input's image
                if (position_j == Inside){ // Column is inside input's image i.e. submatrix gets the same related cols input's value and input's top row value
                    submatrix[i][j] = input[0][related_j];
                } else if (position_j == OutsideNegative){ // Column is outside- left input image i.e. same value as current ij entry (Top left corner of input's entry)
                    submatrix[i][j] = input[current_i][current_j];
                } else if (position_j == OutsidePositive){ // Column is outside- right input image i.e. same value as current ij entry. (Top right corner of input's entry)
                    submatrix[i][j] = input[current_i][current_j];
                }
            } else if (position_i == OutsidePositive){// Submarray's row is outside - down input's image
                if (position_j == Inside){ // Column is inside input image i.e. related col value and input's previous (buttom) row value
                    submatrix[i][j] = input[rows_input - 1][related_j];
                } else if (position_j == OutsideNegative){ // Column is outside- left input image i.e. same value as current ij entry (buttom left corner of input's entry).
                    submatrix[i][j] = input[current_i][current_j];
                } else if (position_j == OutsidePositive){ // Column is outside- right input image i.e. same value as current ij entry (buttom right corner of input's entry).
                    submatrix[i][j] = input[current_i][current_j];
                }
            } 
        }
    }
}

void Create_kernel(long unsigned int size_kernel, boost::multi_array<float,2>& kernel){
    boost::array<size_t,2> extents; // 2D multiarray
    extents.assign(size_kernel);
    kernel.resize(extents); // resize kernel to given size
}

void Create_BoxBlurKernel(long unsigned int size_kernel, boost::multi_array<float,2>& kernel){
    float factor = 1/(float)(size_kernel*size_kernel); // multiplying factor for kernel entries - normalization

    // Assign value to each of the kernel's entries
    for (long unsigned int current_i=0; current_i< size_kernel; current_i++){
        for (long unsigned int current_j = 0; current_j < size_kernel; current_j++){
            kernel[current_i][current_j] = factor; 
        }
    }
}


void Image::BoxBlur(long unsigned int size_kernel){
    boost::multi_array<float,2> kernel; 
    boost::multi_array<unsigned char,2> output;

    // Get image size
    long unsigned int rows = img.shape()[0];
    long unsigned int cols = img.shape()[1];
    // Resize output image to image size
    output.resize(boost::extents[rows][cols]);

    Create_kernel(size_kernel, kernel); // Create kernel's structure
    Create_BoxBlurKernel(size_kernel,kernel); // Create blur kernel

    Convolution(img, output, kernel); // Apply convolution between image and kernel
    img = output; // update img to blurred output for further processing
}

unsigned int Image::Sharpness(){
    boost::multi_array<float,2> kernel; 
    boost::multi_array<unsigned char,2> output;

    long unsigned int rows = img.shape()[0];
    long unsigned int cols = img.shape()[1];
    output.resize(boost::extents[rows][cols]);

    // Fixed size of sharpness kernel
    long unsigned int size_kernel = 3;
    
    Create_kernel(size_kernel, kernel); // Create kernel structure

    // Fill kernel's entries
    kernel[0][0] = 0.;
    kernel[0][2] = 0.;
    kernel[2][0] = 0.;
    kernel[2][2] = 0.;
    kernel[1][0] = 1.;
    kernel[0][1] = 1.;
    kernel[2][1] = 1.;
    kernel[1][2] = 1.;
    kernel[1][1] = -4.;
    
    
    Convolution(img, output, kernel); // Apply convolution between input (blurred) image and kernel and store it in 'output' multiarray.

    unsigned char sharp_value = 0; // Initial sharpness value

    // Find the maximum sharpness value among the output's multiarray.
    for (unsigned int i = 0; i<rows; i++ ){
        for (unsigned int j = 0; j<cols; j++){
            if ((output[i][j]) > sharp_value){
                sharp_value = output[i][j];
            }
        }
    }

    return (unsigned int) sharp_value; // Return sharpness value
}