
def process_chart_data(metadata):

    output = {}
    count = []
    # print(metadata.student_info)

    # values of dic
    value = [_['value'] for _ in metadata.student_info]  # values of dic
    data_rate = []
    sum_label =0
    for i in range(1 ,len(metadata.student_info ) +1):
        sum_label += metadata.student_info[i-1]['value']
        data_rate.append(round(sum_label/i , 2))

    # get percentage of value 0 and 1
    value_len = len(value)
    if value_len != 0:
        count.append(round(value.count(0 ) /value_len ,2 ) *100)
        count.append(100 -count[0])

    num = len(metadata.student_info) # num of data
    if num != 0:
        grade = sum(value) / num  # get grade
    else:
        grade = 0

    # dictionary for chart data
    output['value_count'] = count
    output['grade' ] =grade
    output['warning' ] =metadata.warning # num of warning
    output['labels' ] =[_['time'] for _ in metadata.student_info]
    output['values' ] =value
    output['data_rate' ] =data_rate
    # print(output)
    return output