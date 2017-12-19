from .HausdorffMethod import hausdorff
from .Database import database
from joblib import Parallel, delayed
import time

#Find the mean of hausdorff list, to remove duplicates
def mean_key_value_list(l):
    freq={}
    sum={}
    for x in l:
        if(x[1] in freq.keys()):
            freq[x[1]]+=1
            sum[x[1]]+=x[0]
        else:
            freq[x[1]]=1
            sum[x[1]]=x[0]
    result=[]
    for x in freq.keys():
        result.append([sum[x]/freq[x],x])
    return result


#Method to handle parallelism
def wai(template_points,test_points,method,img_shape,name,i):
    start_time = time.time()
    val = hausdorff(template_points,test_points,method,img_shape,name,i)
    print(i,name,val)
    # print("--- %s Seconds ---" % (time.time() - start_time))
    return [val,name]


#Recognize the detected image
def recognize(img_data,gr):
    method,test_points,skew,laugh,img_shape = img_data
    hausdorff_list=[]
    
    templates = database(skew,laugh,gr)

    #Non parallel version
    # hausdorff_list = [ wai(template_points,test_points,method,img_shape,name,i) for i,(name,template_points) in enumerate(templates) ]

    #Parallel version
    hausdorff_list =  Parallel(n_jobs=-1)(delayed(wai)(template_points,test_points,method,img_shape,name,i) for i,(name,template_points) in enumerate(templates)) 


    #Remove all hausdorff values which ae greater than threshold as they are not present in out database , supposed to be done in LHD
    # for i in range(len(hausdorff_list)-1,-1,-1):
    #     if(hausdorff_list[i][0]>=threshold):
    #         hausdorff_list.remove(hausdorff_list[i])


    #If no images matched closely, then the hausdorff list is empty
    if(len(hausdorff_list)==0):
        return "Not Found"

    #Find the mean of hausdorff list, to remove duplicates
    # if(method==1 or method==2):
    #     hausdorff_list = mean_key_value_list(hausdorff_list)
   
    hausdorff_list.sort()
    k=3
    #If multiple matches, find the min distance match from the database
    return [name for _,name in hausdorff_list[:k]]