from PIL import Image, ImageDraw
import numpy as np
import sys
from math import pow,sqrt
import csv


addr_to_pic = "images/img_denoised2.jpg"
image = Image.open(addr_to_pic)
bw = image.convert(mode="L")

#getting brightness data
pixels = list(bw.getdata())
width, height = bw.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
orig = sys.stdout

#sending image to a file
sys.stdout = open("fname.csv" , 'w')
print(f"{height},{width}",end=",")

for i in range(height):
    for j in range(width):
        print(f"{pixels[i][j]}",end=",")
    print()
sys.stdout = orig
print("jobdone")

# finding the maximum intensity pixel and its coordinates
star_centroid_list=[]
while(True): 
    max = 0
    for i in range(height):
        for j in range(width):
            if max<pixels[i][j]:
                max = pixels[i][j]
    if max<=6:
        break
    print(max)
    max_coords = [(x, y) for x in range(height) for y in range(width) if pixels[x][y] == max]
    if len(max_coords)<1:
        pixels[max_coords[0],max_coords[1]]=0
        continue   
    for i in max_coords:
        sumval=[0,0]
        sum=0
        sumweight=0
        count=0
        for m in range(sorted((i[0]-1,0))[1],min((i[0]+2,height-1))):
            for n in range(sorted((i[1]-1,0))[1],min((i[1]+2,width-1))):
                if pixels[m][n]>=2:
                    count+=1
        if count>=3:
            count=0     
            for m in range(sorted((i[0]-6,0))[1],min((i[0]+7,height-1))):
                for n in range(sorted((i[1]-6,0))[1],min((i[1]+7,width-1))):
                    if pixels[m][n]>=2:
                        sumweight+=pixels[m][n]
                        sumval[0]+=m*pixels[m][n]
                        sumval[1]+=n*pixels[m][n]
                        sum+=pixels[m][n]
                        count+=1
            if count>=3:            
                star_centroid_list.append(((sumval[0]/sumweight)+1,(sumval[1]/sumweight)+1,sum/count))
            for m in range(sorted((i[0]-6,0))[1],min((i[0]+7,height-1))):
                for n in range(sorted((i[1]-6,0))[1],min((i[1]+7,width-1))):
                    pixels[m][n]=0  
        else:
            pixels[i[0]][i[1]]=0      
                        
f=open("stars.csv","w")
f.write("x coord,y coord, mean intensity")
f.write("\n")
for i in star_centroid_list:
    f.write(str(i[1]))
    f.write(",")
    f.write(str(i[0]))
    f.write(",")
    f.write(str(i[2]))
    f.write("\n")
f.close()


# Draw circles around identified stars
#draw = ImageDraw.Draw(image)
#for centroid in star_centroid_list:
#    x, y, _ = centroid
#   draw.ellipse((x - 20, y - 20, x + 20, y + 20), outline="red")

# Save or show the image
#image.show()  # or image.save("output_with_circles.jpg")
