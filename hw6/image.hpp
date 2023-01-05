#ifndef IMAGE_HPP
#define IMAGE_HPP

#include <string>
#include <boost/multi_array.hpp>

/* Creates an Image class with data attributes: filename (string) and img (boost multiarray). Save method receives 'filename' saves the array 'img' as a JPG file. BoxBlur method receives an odd size for the kernel and returns a blurred image 'img'. Sharpness method computes the sharpeness of the image and returns it as an unsigned integer. */
class Image {
    public:
        std::string initial_filename;
        boost::multi_array<unsigned char, 2> img;
        
        Image(std::string filename);
        void Save(std::string filename);
        void BoxBlur(long unsigned int size_kernel);
        unsigned int Sharpness(void);

};

/* Reads an input image, performs the convolution with the given kernel and stores new image in 'output' multiarray. */
void Convolution(boost::multi_array<unsigned char,2>& input, 
                    boost::multi_array<unsigned char,2>& output,
                    boost::multi_array<float,2>& kernel);

/* Creates a subarray for each pixel in an image. The size of the subarray is equal to the size od the given kernel. */
void Create_subarray(boost::multi_array<unsigned char,2>& input, boost::multi_array<unsigned char,2>& submatrix, long unsigned int rows_kernel,  long unsigned int cols_kernel,  long unsigned int rows_input,  long unsigned int cols_input,  unsigned int current_i, unsigned int current_j);

/* Creates the structure of a kernel of the given size. */
void Create_kernel(long unsigned int size_kernel, boost::multi_array<float,2>& kernel);

/* Fills kernel with values corresponding to a Blur kernel of the given size. */
void Create_BoxBlurKernel(long unsigned int size_kernel, boost::multi_array<float,2>& kernel);

#endif /* IMAGE_HPP */