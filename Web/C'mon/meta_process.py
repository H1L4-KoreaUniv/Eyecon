

def process_chart_data(metadata):

    output = {}
    count = []
    # print(metadata.student_info)
    value = [_['value'] for _ in metadata.student_info] #values of dic

    data_rate = []
    sum_label=0
    for i in range(1,len(metadata.student_info)+1):
        sum_label+=metadata.student_info[i-1]['value']
        # print(sum_label, i, sum_label/i)
        data_rate.append(round(sum_label/i,1))
    # print(data_rate)
    count.append(value.count(0))
    count.append(value.count(1))

    num = len(metadata.student_info) # num of data
    if(num !=0) :
        AVG = sum(value) / num # get grade
        if AVG >= 0.8:
            grade = 'high'
        elif AVG >= 0.5:
            grade = 'middle'
        else:
            grade = 'low'
    else:
        grade='low'

    # dictionary for chart data
    output['value_count'] = count
    output['grade']=grade
    output['warning']=metadata.warning # num of warning
    output['labels']=[_['time'] for _ in metadata.student_info]
    output['values']=value
    output['data_rate']=data_rate
    # print(output)
    return output