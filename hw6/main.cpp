#include <sstream>
#include <stdexcept>
#include <string>
#include <iostream>
#include <cstdio>
#include <vector>
#include <cmath>


#define BOOST_DISABLE_ASSERTS
#include <boost/multi_array.hpp>
#include <jpeglib.h>
#include "jpeglib.h"

#include "image.hpp"


int main(){
    
    std::string filename = "stanford.jpg"; // Reads original image
    std::string output; // Variable that stores output (modified) image

    // Create list of kernel sizes for blurring 
    std::vector<long unsigned int> size_kernel_vec = {3, 7, 11, 15, 19, 23, 27};
    long unsigned int vecSize = size_kernel_vec.size();

    Image image1(filename); // Create new  Image instance
    unsigned int sharp_value = image1.Sharpness(); // Get sharpness of original image
    std::cout<< "Original image: " << sharp_value << std::endl;

    // For each blur value reload the original image, create a new instance, blur it and compute the output (blurred image) sharpness.
    for (unsigned int i = 0; i < vecSize; i++){
        Image image1(filename);
        image1.BoxBlur(size_kernel_vec[i]);

        // Save output image as "BoxBlur#.jpg".
        if (size_kernel_vec[i] < 10){
            output = "BoxBlur0" + std::to_string(size_kernel_vec[i]) + ".jpg";
            image1.Save(output);
            sharp_value = image1.Sharpness();
            std::cout<< "BoxBlur( " << size_kernel_vec[i] << "): " << sharp_value << std::endl;

        } else {
            output = "BoxBlur" + std::to_string(size_kernel_vec[i]) + ".jpg";
            image1.Save(output);
            sharp_value = image1.Sharpness();
            std::cout<< "BoxBlur(" << size_kernel_vec[i] << "): " << sharp_value << std::endl;
        }
    }

    return 0;
}