import machinevisiontoolbox as mvt
from matplotlib import pyplot as plt

"""
Task 1
The mvt library contains a method called Blobs() which takes an mvt.Image 
object as the first input, and a variety of parameters to fine-tune what information it collects and 
what filtering it performs as keyword arguments (these are outlined in the documentation). 
Use this method to extract the blobs from red_mask.jpg.
"""
def task_1():
    img = mvt.Image.Read("prac_images/red_mask.jpg")
    K_gauss = mvt.Kernel.Gauss(sigma=5, h=15)
    s_gauss = img.convolve(K_gauss)
    se = mvt.Kernel.Circle(5)  # or similar
    #clean = s_gauss.open(se)
    clean = s_gauss.close(mvt.Kernel.Circle(5))

    blobs = clean.blobs()
    mvt.Image.disp(clean, block=True)

    return

"""
Task 2
Use the Blobs object's circularity property to determine the shape of each stored blob.
Are there other ways you could calculate the circularity using information stored in blobs 
if the circularity method was unavailable? 
"""
def task_2():
    blobs = task_1()
    for blob in blobs:
        if blob.circularity >= 1: print("Circle")
        else: print("Not circle") 

"""
Task 3
Plot the centroids and bounding boxes of the stored Blobs. 
Do they visually match up with the shapes you can see in your binary images?
NOTE: There are methods attached to the Blobs object which will help you with this; 
refer to the documentation.
"""
def task_3():
    blobs = task_1()
    blobs.plot_box(color='g', linewidth=2)
    blobs.plot_centroid(label=True)      
    

"""
Task 4
Repeat tasks 1-3 on green_mask.jpg. 
You will notice that this mask isn't very good and needs to be cleaned up. 
Add a clean-up step before calling the blobs function. 
What kind of functions will help remove the extra noise without altering the shapes you need?
NOTE: The blobs function will show a divide by zero error if your binary images contain any 
single pixel noise or thin line artifacts. If you get this error, then you need to be more 
aggressive with the cleaning, or find an alternative method (this bug may or may not have been fixed yet).
"""

"""
Task 5
Repeat tasks 1-4 on blue_mask.jpg. This time, there is a large strip that has incorrectly been masked. 
Using the same clean-up methods as before may not work as they would significantly alter the shapes we 
want to keep. Instead, keep it in the image, and use the information returned by the blobs function to 
discard the unwanted blobs.
"""

"""
Task 6
Currently, your blob information is stored separately for each colour channel. 
It may be useful to you to have all the information in one place for easy reference. 
Create a variable of your choice (such as a Python dictionary) that collates this 
information in a useful way. Think about what identifying information about a blob 
should be stored so it can be referenced uniquely if needed.
"""

if __name__ == "__main__":
    print(task_1())
    #task_3()