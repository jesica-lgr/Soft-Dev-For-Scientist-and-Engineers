# Image processing in C++: Blur and sharpness
## Homework 6 
### Jesica Leticia Gonzalez Robles 
### SUID: 06654005
### CME211 Fall 2022

This program performs two of the most popular image processing operations: blurring/smoothing and sharpening of an image by computing the convolution between the image and a given kernel.

The implementation is divided into the following files: main.cpp, image.cpp, and hw6.cpp, with the corresponding HPP files for the later two. A makefile is provided to compile and execute the program. 

**HW6** files contains the *ReadGrayscaleJPEG* used to read a JPEG image from a filename as store it as a boost multiarray. Similarly, it contains the *WriteGrayscaleJPEG*, which writes the contents of a Boost MultiArray to a grayscale JPEG image.

**IMAGE** files declare/define an Image class from a give filename. It reads the image and store the image data as the following data attributes: filename (string) and img (boost multiarray). The *Save* method receives 'filename' saves the array 'img' as a JPG file. *BoxBlur* method receives an odd-size value for the kernel, creates the corresponding Blur kernel and returns a blurred output image. *Sharpness* method computes the sharpeness of the output image by performing the convolution with a fixed-size 3x3 kernel that approximates the Laplacian operator and returns the sharpness result as an unsigned integer. 

Sharpness kernel:
$$
\begin{bmatrix} 
0 & 1 & 0 \\ 
1 & -4 & 1 \\ 
0 & 1 & 0 \end{bmatrix}
$$

Additional functions were implemeted for the computation, such as:

- *Convolution*: Reads an input image, performs the convolution with the given kernel and stores new image in 'output' multiarray.
- *Create_subarray*: Creates a subarray for each pixel in an image. The size of the subarray is equal to the size od the given kernel.
- *Create_kernel*: Creates the structure of a kernel as a boost multiarray of the given size.
- *Create_BoxBlurKernel*: Receives an odd size for the kernel, creates it structure and fills it with values corresponding to a Blur kernel of the given size where all entries are normalized (total sum is equal to 1).

**MAIN** file stores the name of the original image "stanford.jpg" and reloads the image by creatig a new instance of the Image class, and blurres it with each following values: {3, 7, 11, 15, 19, 23, 27}. For each of this cases, it computes and outputs the resulting image sharpness and stores it in a JPG file called "BoxBlur(kernel size).jpg". 

```bash
make
./main
```
Expected output:

```c++
Original image: 255
BoxBlur( 3): 139
BoxBlur( 7): 44
BoxBlur(11): 27
BoxBlur(15): 21
BoxBlur(19): 16
BoxBlur(23): 11
BoxBlur(27): 9
```

**Note:** The last three outputs give different results as the ones stated in the hw 6 file. (BoxBlur(19): 19, BoxBlur(23): 17, and BoxBlur(27): 19). I tried multiple things, together with Rishu, Thomas, and Axel in several OH but unfortunately, we couldn't fix this issue. Therefore, they asked me to add this note for it to be considered while grading. 






