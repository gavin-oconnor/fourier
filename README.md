# Fourier Series Visualization
This program begins by letting the user draw a path using their mouse.
The user should press the space bar when they are finished drawing.
Next, the program uses the path as a complex function. This complex function can be represented as sum
of rotating vectors. A rotating vector can be represented as $e^{2{\pi}it}$ as t moves from 0-1. We can
change this vectors length and itial angle by multiplying it by another complex number called Cn. The main work in
this problem is calculating all the complex constants to find the series which approximates f(t).  
**The program uses a 101 term series of rotating vectors to approximate f(t)**.      
  $$f(t) \approx \sum_{n=-50}^{50}c_ne^{2{\pi}int}$$   where    $$c_n = \int_{0}^{1} e^{-2{\pi}int}f(t) \,dt$$

3Blue1Brown has a [video that explains fourier series very
well.](https://www.youtube.com/watch?v=r6sGWTCMz2k&t=1315s), and that is what this project is based on.  
  
    
    
**Below shows a crude image of a house drawn first by hand them estimated with the sum of rotating vectors**. 

![Image of a house drawn with fourier series](https://github.com/gavin-oconnor/fourier/blob/main/house_example.png)
