import numpy as np

#initial input
lambda1 = 0.2/60
lambda2 = 0.6/60
lambda3 = 1.2/60
u = 3
simu_num = 60*24*30

#input procedure
x1 = np.random.poisson(lam = lambda1,size = simu_num)
x2 = np.random.poisson(lam = lambda2,size = simu_num)
x3 = np.random.poisson(lam = lambda3,size = simu_num)
sum_patient = x1.sum() + x2.sum() + x3.sum() #total numbel of patient
ux = np.random.poisson(lam = 3,size= (sum_patient,20))
ser_time = np.zeros(sum_patient,float)
for i in range(len(ux)):
    ser_time[i] = round(60/ux[i].mean()) #generate each patient's sevice time  unit:minute

#queuing model
time_axis = []
finish_people = 0
finish_time1 = 0
finish_time2 = 0
finish_time3 = 0
queuing_line = [0,0,0]#simulate the waiting queue:[0] is the first-class patient, then...
doctor = 0
#record the W_q
tcome1 = []
tcome2 = []
tcome3 = []
twait1 = []
twait2 = []
twait3 = []

def record_come_time(i, x1, x2, x3, tcome1, tcome2, tcome3):
    if x1[i] > 0:
        for j in range(x1[i]):
            tcome1.append(i)
    if x2[i] > 0:
        for j in range(x2[i]):
            tcome2.append(i)
    if x3[i] > 0:
        for j in range(x3[i]):
            tcome3.append(i)
    return(tcome1, tcome2, tcome3)

def average(tcome, twait):
    wq = []
    W_q = 0
    for i in range(len(twait)):
        wq.append(twait[i] - tcome[i])
        W_q += wq[i]
    W_q = W_q/(len(twait)+1)
    return W_q/60

#facilitating agency
def service_rule(i,finish_time1, finish_time2, finish_time3, queuing_line, \
                 doctor, finish_people, ser_time, twait1, twait2, twait3):
    if (i >= finish_time1) and (i >= finish_time2) and (i >= finish_time3):
        doctor = 0
    if doctor == 1:
        pass
    else:
        if queuing_line[0] > 0:
            doctor = 1
            queuing_line[0] -= 1
            finish_time1 = i + ser_time[finish_people]
            finish_people += 1
            twait1.append(i)
            if (i < finish_time2):
                twait2.pop()
                queuing_line[1] += 1
                finish_time2 = i
                finish_people -= 1
            if (i < finish_time3):
                queuing_line[2] += 1
                finish_time3 = i
                finish_people -= 1
                twait3.pop()
        else:
            if doctor == 2:
                pass
            else:
                if queuing_line[1] > 0:
                    doctor = 2
                    queuing_line[1] -= 1
                    finish_time2 = i + ser_time[finish_people]
                    finish_people += 1
                    twait2.append(i)
                    if (i < finish_time3):
                        twait3.pop()
                        queuing_line[2] += 1
                        finish_time3 = i
                        finish_people -= 1
                else:
                    if doctor == 3:
                        pass
                    else:
                        if queuing_line[2] > 0:
                            doctor = 3
                            queuing_line[2] -= 1
                            finish_time3 = i + ser_time[finish_people]
                            finish_people += 1
                            twait3.append(i)
                        else:
                            pass
    return(doctor, queuing_line, finish_time1, finish_time2, finish_time3, finish_people,twait1,twait2, twait3)

#simulate the process
for i in range(simu_num):
    time_axis.append(x1[i]+x2[i]+x3[i])
    #simulate queuing process
    if time_axis[i]>0:
        #update queue
        queuing_line = [queuing_line[0] + x1[i], queuing_line[1] + x2[i], queuing_line[2] + x3[i]]
        # collect the patient's time axis
        (tcome1, tcome2, tcome3) = record_come_time(i, x1, x2, x3, tcome1, tcome2, tcome3)
        #There is someone in first-class line
    (doctor, queuing_line, finish_time1, finish_time2, finish_time3, finish_people,twait1,twait2, twait3) \
    = service_rule(i, finish_time1, finish_time2, finish_time3, queuing_line, doctor, finish_people, ser_time,twait1,twait2, twait3)
    #print(twait1,twait2,twait3)

W_q1 = average(tcome1, twait1)
W_q2 = average(tcome2, twait2)
W_q3 = average(tcome3, twait3)
print(W_q1,W_q2,W_q3)
