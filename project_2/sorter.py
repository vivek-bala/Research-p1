import sys

def merge(left,right):
    result = []
    i,j = 0,0
    while ((i<len(left)) and (j<len(right))):
        if(left[i] <= right[j]):
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    result += left[i:]
    result += right[j:]
    return result

def mergesort(data):
    if (len(data)<=1):
        return data
    mid = int(len(data))/2
    left = mergesort(data[:mid])
    right = mergesort(data[mid:])
    return merge(left,right)
        

if __name__ == "__main__":
    args = sys.argv[1:]
    outfile = args[0]
    data_string_1 = args[1:]
    data_string_2 = ''.join(data_string_1)
    data_string_3 = data_string_2[1:len(data_string_2)-1].split(',')
    data_string_4=[]
    for x in range(0,len(data_string_3)):
        data_string_4.append(int(data_string_3[x]))
    data_1 = mergesort(data_string_4)
    data_2 = ','.join(map(str,data_1))
    f1 = open ('/home/vivek/project_2/'+outfile,'w')
    f1.write(str(data_2))
    f1.close()
    
    
