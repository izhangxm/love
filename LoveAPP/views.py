from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
import glob
from Love.settings import logger, BASE_DIR
import os
from LoveAPP.helper import wechat_log_analyse,word_cloud_generate
import math


def catch_data(request):
    resp_data = {'status': 1, "code": '0', "info": "ok"}
    try:
        csv_file_path = glob.glob(os.path.join(BASE_DIR, 'data/*.csv'))[-1]
        csv_flag = os.path.basename(csv_file_path).split('_')[0]
        ana_res = wechat_log_analyse(csv_file_path, csv_flag)
        img_list, top_10 = word_cloud_generate(csv_file_path, csv_flag)

    except Exception as e:
        resp_data['status'] = 0
        resp_data['code'] = 500
        resp_data['info'] = 'Failed: ' + str(e)

    return JsonResponse(resp_data)

def index(request):

    context = {}
    time_str = datetime.now().strftime('%H%M')
    if not os.path.exists(os.path.join(BASE_DIR,'data','.opened.txt')) and time_str != '1314':
        return render(request, 'sorry.html', context)

    csv_file_path = glob.glob(os.path.join(BASE_DIR,'data/*.csv'))[-1]
    csv_flag = os.path.basename(csv_file_path).split('_')[0]

    context['csv_flag'] = datetime.strptime(csv_flag,'%Y%m%d').strftime('%Y年%m月%d日')

    ana_res = wechat_log_analyse(csv_file_path,csv_flag)
    img_list, top_10 = word_cloud_generate(csv_file_path,csv_flag)


    ana_res.pop('content_lines')
    context = dict(context,**ana_res)

    context['word_cloud_pic'] = img_list[0]
    context['word_cloud_top10'] = ",".join(top_10)


    mode = 'r+'
    if not os.path.exists(os.path.join(BASE_DIR,'data','.opened.txt')):
        mode='w+'

    with open(os.path.join(BASE_DIR,'data','.opened.txt'),mode) as f:
        content = f.read()
        if content=='':
            opened_times = 1
            context['first_open'] = True
        else:
            opened_times = int(content)+1
            context['first_open'] = False
        f.seek(0)
        f.truncate()
        f.write(str(opened_times))

    context['opened_times'] = opened_times

    we_know_start = datetime.fromtimestamp(1586488011)# 2020-04-10 11:06:51
    now_time = datetime.now()
    now_time_str = now_time.strftime('%Y-%m-%d %H:%M:%S')
    distanse_time = now_time-we_know_start

    total_sec = math.ceil(distanse_time.total_seconds())
    total_min = math.ceil(total_sec/60)
    total_hor = math.ceil(total_min/60)
    total_day = math.ceil(total_hor/24)

    context['now_time'] = now_time.strftime('%Y年%m月%d日 %H点%M分%S秒')
    context['total_day'] = total_day
    context['total_hor'] = total_hor
    context['total_min'] = total_min
    context['total_sec'] = total_sec



    return render(request, 'index.html', context)


def log_action(request):
    resp_data = {'status': 1, "code": '0', "info": "ok"}

    try:
        action = request.GET.get('action')
        index = request.GET.get('index')
        logger.log('INFO','SYS','%s, %s' % (action, index) )



    except Exception as e:
        resp_data['status'] = 0
        resp_data['code'] = 500
        resp_data['info'] = 'Failed: ' + str(e)

    return JsonResponse(resp_data)
