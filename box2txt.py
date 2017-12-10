import os
files = os.listdir("boxfiles")

if not os.path.isdir("annotations"):
    os.mkdir("annotations")
    
for x in files:

    f = open("boxfiles/"+x,"r").readlines()
    for y in f: # one line, one frame
        print(y)
        line = y.split()
        '''
         .zfill(3) will pad zeros to make the number 3-digit
         this will help you in opening the files if all are on same pattern with same length
        '''
        file = open("annotations/"+os.path.splitext(os.path.splitext(x)[0])[0]+"_"+line[0].zfill(3)+".txt","w")
        lines = []

        for it in range(0,int(line[1])):
            if(abs(float(line[2+(it*4)])-float(line[2+2+(it*4)]))<5 or abs(float(line[2+1+(it*4)])-float(line[2+3+(it*4)]))<5 ):
                continue
            else:
                gtline = "1 " + " ".join(line[2+(it*4):2+4+(it*4)])
                lines.append(gtline)
        file.write("\n".join(lines))
        file.close()