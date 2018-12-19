# Queuing-Model-with-Preemptive-Priorities

带有两个优先级的排队模型模拟，并使用cv2将图片流合成视频进行展示。


## 问题提出

有三类病人：（1）病危型，病情致命，必须马上治疗；（2）严重型，拖延治疗会使病情加重；（3）平稳型，治疗不及时并没有严重的后果。病人们按照以上优先级进行排队，每个优先级内部再按照到达顺序排队。

预测显示，大约有10%的病危型病人，30%的严重型病人，60%的平稳型病人。因为严重的疾病在紧急处理后还要进行进一步治疗，所以花在急诊室的时间并不是很长，进而我们可以认为三种类型的病人接受治疗的时间是相同的。

由于病危病人和严重型病人的治疗不能耽误，所以这是一个强占性优先权排队模型。查询一般的数据为μ=3，λ=2。

## 理论公式求解结果

𝑊q_1=0.024 h,
𝑊q_2=0.154 h,
𝑊q_3=1.033 h
## 模拟结果（模拟五次后取平均）
模拟一天：
𝑊q_1 = 0 h,𝑊q_2 = 0.036732026 h,𝑊q_3 = 0.430246914 h

模拟一个月：
𝑊q_1 = 0.01708074 h,𝑊q_2 = 0.120085 h,𝑊q_3 = 0.82134644 h

模拟十年：
𝑊q_1 = 0.012631 h,𝑊q_2 = 0.1118465 h,𝑊q_3 = 1.10392767 h

## 模拟示例说明
我们的一级病人为：![first-class patient](https://github.com/yukiiwong/Queuing-Model-with-Preemptive-Priorities/blob/master/1.jpg)

我们的二级病人为：![second-class patient](https://github.com/yukiiwong/Queuing-Model-with-Preemptive-Priorities/blob/master/2.jpg)

我们的三级病人为：![third-class patient](https://github.com/yukiiwong/Queuing-Model-with-Preemptive-Priorities/blob/master/3.jpg)

过程图片示例：![sample](https://github.com/yukiiwong/Queuing-Model-with-Preemptive-Priorities/blob/master/1397.jpg)

视频示例：[video](https://github.com/yukiiwong/Queuing-Model-with-Preemptive-Priorities/blob/master/camera_test.avi)
