from PIL import Image, ImageDraw
import numpy as np
import sys
from math import pow,sqrt
import csv

def calculate_average_intensity(pixels, center_x, center_y, size):
    total_intensity = 0
    count = 0
    for i in range(max(center_x - size, 0), min(center_x + size + 1, height)):
        for j in range(max(center_y - size, 0), min(center_y + size + 1, width)):
            total_intensity += pixels[i][j]
            count += 1
    return total_intensity / count

addr_to_pic = "images/img_denoised2.jpg"
image = Image.open(addr_to_pic)
bw = image.convert(mode="L")

#getting brightness data
pixels = list(bw.getdata())
width, height = bw.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
orig = sys.stdout

#sending image to a file
sys.stdout = open("fname" , 'w')
print(f"{height},{width}",end=",")
for i in range(height):
    for j in range(width):
        print(f"{pixels[i][j]}",end=",")
    print()
sys.stdout = orig
print("jobdone")

f=open("threshold.csv","w")

# finding the maximum intensity pixel and its coordinates
star_centroid_list=[]
while(True): 
    max1 = 0
    for i in range(height):
        for j in range(width):
            if max1<pixels[i][j]:
                max1 = pixels[i][j]
    if max1<=18:
        break
    f.write(str(max1)+',')
    max_coords = [(x, y) for x in range(height) for y in range(width) if pixels[x][y] == max1]
    if len(max_coords)<1:
        pixels[max_coords[0],max_coords[1]]=0
        continue 
      
    for i in max_coords:
        sumval=[0,0]
        sum=0
        count=0
        threshold=calculate_average_intensity(pixels, i[0], i[1], 6)
        if not threshold:
            pixels[i[0]][i[1]]=0
            break
        for m in range(sorted((i[0]-1,0))[1],min((i[0]+2,height-1))):
            for n in range(sorted((i[1]-1,0))[1],min((i[1]+2,width-1))):
                if pixels[m][n]>=threshold:
                     count+=1
        if count>=3:
            count=0     
            for m in range(sorted((i[0]-6,0))[1],min((i[0]+7,height-1))):
                for n in range(sorted((i[1]-6,0))[1],min((i[1]+7,width-1))):
                    if pixels[m][n]>=threshold:
                        sum+=(pixels[m][n]**2)
                        sumval[0]+=m*(pixels[m][n]**2)
                        sumval[1]+=n*(pixels[m][n]**2)
                        count+=1
            if count>=3:            
                star_centroid_list.append(((sumval[0]/sum)+1,(sumval[1]/sum)+1,np.sqrt(sum/count)))
            for m in range(sorted((i[0]-6,0))[1],min((i[0]+7,height-1))):
                for n in range(sorted((i[1]-6,0))[1],min((i[1]+7,width-1))):
                    pixels[m][n]=0 
            f.write(str(threshold)+',') 
        else:
            pixels[i[0]][i[1]]=0 
    f.write('\n')
                
f=open("stars(2).csv","w")
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
#for centroid in star_centroid_list[ :50]:
#    x, y, _ = centroid
#    draw.ellipse((x - 20, y - 20, x + 20, y + 20), outline="red")

# Save or show the image
#image.show()  # or image.save("output_with_circles.jpg")
