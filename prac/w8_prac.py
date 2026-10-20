import machinevisiontoolbox as mvt
import matplotlib.pyplot as plt

if __name__ == "__main__":
    im = mvt.Image.Read("prac_images/highway.jpg")
    
    # Task 1
    print(im.size)

    # Task 2
    im.disp(block=True)

    # Task 3
    #im.hist().plot(block=True)

    # Task 4
    # slide a portion of the image and plot the intensities of each of the pixels
    """
    plt.figure()
    plt.plot(im.image[:, 1155])
    plt.xlabel("x")
    plt.ylabel("intensity")
    plt.title("Pixel intensities along col 1155")
    plt.show()

    plt.figure()
    plt.plot(im.image[1280, :])
    plt.xlabel("x")
    plt.ylabel("intensity")
    plt.title("Pixel intensities along col 1155")
    plt.show()
    """