from PIL import Image,ImageFilter
im = Image.open("/Users/mac/Desktop/captcha/4HENG5.png")
pointset = []
raw = im.load()
width,height = im.size
for w in xrange(width):
    for h in xrange(height):
        if raw[w,h] != (0,0,0):
            im.putpixel((w,h),(255,255,255))

box = (23,14,width-23,height-15)
im = im.crop(box)
width,height = im.size
white = (255,255,255)
black = (0,0,0)
#print width,height
#im = im.filter(ImageFilter.)
raw = im.load()

def is_black(raw,point=(0,0)):
    if raw[point[0],point[1]] == black :
        return True
    else:
        return False

def is_single(raw,w,h,width,height):
    #print w,h
    left = (w-1,h)
    right = (w+1,h)
    up = (w,h+1)
    down = (w,h-1)
    points = filter(lambda  x : x[0]>0 and x[1]>0 and x[0]<width and x[1]<height,(left,right,up,down))
    #print points
    result = True
    for x in points :
        result &= not is_black(raw,x)
    return result

def is_breakpoint(marCol,pos):
    if marCol[pos] > 0 :
        return False
    left = pos -1
    right = pos+1
    if left>=0 and right<len(marCol) :
        if marCol[left]==0 and marCol[right]==0 :
            return False
        else :
            return True
    elif left<0 :
        if marCol[right] > 0 :
            return True
    else :
        if marCol[left] > 0 :
            return True
    return False

for w in range(width) :
    for h in range(height):
        if raw[w,h] == (0,0,0):
            if (w==0 and h==0) or (w==width-1 and h==height-1):
                im.putpixel((w,h),white)
            else :
                if is_single(raw,w,h,width,height) :
                    im.putpixel((w,h),white)
im = im.convert('L')

raw = im.load()
marCol = []
for w in xrange(width):
    black_num = 0
    for h in xrange(height):
        if raw[w,h]==0 :
            black_num += 1
    marCol.append(black_num)
print marCol
breakcols = []
breakpoints = []
for i in range(len(marCol)) :
    if is_breakpoint(marCol,i) :
        breakcols.append(i)

print breakcols
for x in range(0,len(breakcols),2) :
    p = (breakcols[x],breakcols[x+1])
    breakpoints.append(p)

if len(breakpoints) < 6 :
    print "divided faled"
else :
    breakpoints = filter(lambda x : x[1]-x[0]>=9,breakpoints)

subimgs = []
for x in breakpoints :
    sim = im.crop((x[0],0,x[1],height))
    subimgs.append(sim)
    sim.show()




print breakpoints



im.show()



