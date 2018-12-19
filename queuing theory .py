import numpy as np
from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy


#initial input
lambda1 = 2*0.2/60
lambda2 = 1.3*0.6/60
lambda3 = 1.2/60
u = 3*1.1
simu_num = 60*24*10

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
def service_rule(i,finish_time1, finish_time2, finish_time3, queuing_line, doctor, finish_people, ser_time, twait1, twait2, twait3):
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


##### Visualise the queuing procedure
# input patients' picture
patient1_pic = Image.open('1.jpg').resize((75, 75))
patient2_pic = Image.open('2.jpg').resize((75, 75))
patient3_pic = Image.open('3.jpg').resize((75, 75))

def wait_queue(i,img_bg,patient_pic):
    if queuing_line[i] == 1:
        # put first-class one
        img_bg.paste(patient_pic, (500, 212+100*i))
    elif queuing_line[i] == 2:
        # put first-class two
        new2_1 = patient_pic.copy()
        img_bg.paste(patient_pic, (500, 212+100*i))
        img_bg.paste(new2_1, (400, 212+100*i))
    elif queuing_line[i] == 3:
        # put first-class three
        new2_1 = patient_pic.copy()
        new2_2 = patient_pic.copy()
        img_bg.paste(patient_pic, (500, 212+100*i))
        img_bg.paste(new2_1, (400, 212+100*i))
        img_bg.paste(new2_2, (300, 212+100*i))
    elif queuing_line[i] == 4:
        # put first-class four
        new2_1 = patient_pic.copy()
        new2_2 = patient_pic.copy()
        new2_3 = patient_pic.copy()
        img_bg.paste(patient_pic, (500, 212+100*i))
        img_bg.paste(new2_1, (400, 212+100*i))
        img_bg.paste(new2_2, (300, 212+100*i))
        img_bg.paste(new2_3, (200, 212+100*i))
    elif queuing_line[i] == 5:
        # put first-class four
        new2_1 = patient_pic.copy()
        new2_2 = patient_pic.copy()
        new2_3 = patient_pic.copy()
        new2_4 = patient_pic.copy()
        img_bg.paste(patient_pic, (500, 212+100*i))
        img_bg.paste(new2_1, (400, 212+100*i))
        img_bg.paste(new2_2, (300, 212+100*i))
        img_bg.paste(new2_3, (200, 212+100*i))
        img_bg.paste(new2_4, (100, 212+100*i))
    elif queuing_line[i] >= 6:
        # put first-class four
        new2_1 = patient_pic.copy()
        new2_2 = patient_pic.copy()
        new2_3 = patient_pic.copy()
        new2_4 = patient_pic.copy()
        new2_5 = patient_pic.copy()
        img_bg.paste(patient_pic, (500, 212+100*i))
        img_bg.paste(new2_1, (400, 212+100*i))
        img_bg.paste(new2_2, (300, 212+100*i))
        img_bg.paste(new2_3, (200, 212+100*i))
        img_bg.paste(new2_4, (100, 212+100*i))
        img_bg.paste(new2_5, (5, 212+100*i))
    else:
        pass
    return  img_bg

def sickroom(img_bg, patient1_pic, patient2_pic, patient3_pic, doctor):
    if doctor == 1:
        sick1 = patient1_pic.copy()
        img_bg.paste(sick1, (900,220))
    elif doctor == 2:
        sick2 = patient2_pic.copy()
        img_bg.paste(sick2, (900, 220))
    elif doctor == 3:
        sick3 = patient3_pic.copy()
        img_bg.paste(sick3, (900, 220))
    else:
        draw = ImageDraw.Draw(img_bg)
        draw.rectangle([(700, 150), (1000, 300)], fill=(0, 255, 0))
    return img_bg

#simulate the process
for i in range(simu_num):

    # generate the background
    img_bg = Image.new("RGB", (1000, 700), 'white')

    # generate the waitting queue
    draw = ImageDraw.Draw(img_bg)
    draw.line([(100, 200), (600, 200)], fill=(255, 0, 0), width=7)
    draw.line([(100, 300), (600, 300)], fill=(255, 0, 0), width=7)
    draw.line([(100, 400), (600, 400)], fill=(255, 0, 0), width=7)
    draw.line([(100, 500), (600, 500)], fill=(255, 0, 0), width=7)
    #set the service table
    draw.rectangle([(700, 150), (1000, 300)], fill=(0, 255, 0))
    # set the time table
    font = ImageFont.truetype('arial.ttf', 25)
    draw.text((50, 50), "TIME: {} day {}:{}".format(i//3600, i // 60, i % 60), fill=(0, 0, 0), font=font)
    draw.text((600, 250), "First", fill=(255, 0, 0), font=font)
    draw.text((600, 350), "Second", fill=(255, 0, 0), font=font)
    draw.text((600, 450), "Third", fill=(255, 0, 0), font=font)
    draw.text((700, 120), "Sickroom", fill=(255, 0, 0), font=font)
    time_axis.append(x1[i]+x2[i]+x3[i])
    #simulate queuing process
    if time_axis[i]>0:
        #update queue
        queuing_line = [queuing_line[0] + x1[i], queuing_line[1] + x2[i], queuing_line[2] + x3[i]]
        # put our cute patients in
        #print(queuing_line,doctor)
        # collect the patient's time axis
        (tcome1, tcome2, tcome3) = record_come_time(i, x1, x2, x3, tcome1, tcome2, tcome3)
        #print(tcome1,tcome2,tcome3)
        #There is someone in first-class line
    (doctor, queuing_line, finish_time1, finish_time2, finish_time3, finish_people,twait1,twait2, twait3) \
    = service_rule(i, finish_time1, finish_time2, finish_time3, queuing_line, doctor, finish_people, ser_time,twait1,twait2, twait3)
    #print(twait1,twait2,twait3)
    W_q1 = average(tcome1, twait1)
    img_bg = sickroom(img_bg, patient1_pic, patient2_pic, patient3_pic, doctor)
    font1 = ImageFont.truetype('arial.ttf', 20)
    draw.text((700, 360), "Wq_1 = {}".format(W_q1), fill=(0, 0, 0), font=font1)
    W_q2 = average(tcome2, twait2)
    draw.text((700, 400), "Wq_2 = {}".format(W_q2), fill=(0, 0, 0), font=font1)
    W_q3 = average(tcome3, twait3)
    draw.text((700, 440), "Wq_3 = {}".format(W_q3), fill=(0, 0, 0), font=font1)
    #print(W_q1, W_q2, W_q3)
    img_bg = wait_queue(0, img_bg, patient1_pic)
    img_bg = wait_queue(1, img_bg, patient2_pic)
    img_bg = wait_queue(2, img_bg, patient3_pic)
    #img_bg.show()
    img_bg.save('./picss/{}.jpg'.format(i))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 100
size = (1000,700)
out = cv2.VideoWriter('camera_test3.avi', fourcc, fps, size)
for i in range(60*24*10):
    pic = cv2.imread('./picss/{}.jpg'.format(i))
    out.write(pic)

out.release()
pass
