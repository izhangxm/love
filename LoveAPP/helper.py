import os
import re
from LoveAPP.mwordcloud.create_word_cloud import create_word_cloud
import glob
import json
from Love.settings import BASE_DIR


def wechat_log_analyse(csv_file_full_path,csv_flag, force_update=False):
    if csv_file_full_path is None or (not os.path.exists(csv_file_full_path)):
        raise Exception('CSV file is not found.')
    result_catch_file = os.path.join(BASE_DIR,'data', csv_flag+'_res_ana_catch.json')
    if os.path.exists(result_catch_file) and force_update is False:
        fp = open(result_catch_file,'r')
        content = fp.read()
        if len(content)>10:
            jsos_result = json.loads(content)
            return jsos_result

    res_ana = {'voice_duration':0,'voice_count':0,'voice_avg':0,'emoji_count':0,'u_send':0,'I_send':0,'content_lines':[],'total_count':0}
    fp = open(csv_file_full_path, 'r')
    re_p = re.compile(r'("[\d]{10}"[\s\S]*?"[\d]{1,}"\n)')
    all_content = fp.read()
    r = re.findall(re_p, all_content)
    for line in r:
        line = line.strip().replace('\n','')
        res = line.split(r'","')
        if len(res) != 9:
            continue

        content = res[4]
        res_ana['content_lines'].append(content)

        des = res[1]
        if des == '0':
            res_ana['I_send']+=1
        else:
            res_ana['u_send'] += 1

        ct_type = res[-1].strip().replace('"', '')
        if ct_type == '50':
            res_ana['voice_count'] += 1
            re_p = re.compile(r'<duration>([\d]+)</duration>')
            _dd = re.search(re_p, content)
            if _dd:
                res_ana['voice_duration'] += int(_dd.group(1))
        elif ct_type == '47':
            res_ana['emoji_count'] += 1

        res_ana['total_count'] += 1

    res_ana['voice_avg'] = int( 1.0 * res_ana['voice_duration']/res_ana['voice_count'])
    fp.close()

    json.dump(res_ana, open(result_catch_file,'w+'))

    return res_ana



def word_cloud_generate(csv_file_full_path, csv_flag, force_update=False):
    if csv_file_full_path is None or (not os.path.exists(csv_file_full_path)):
        raise Exception('CSV file is not found.')
    res_ana = wechat_log_analyse(csv_file_full_path, csv_flag)

    cloud_pic_dir = os.path.join(BASE_DIR,'static/wordcloud')
    if force_update:
        img_list, top_10 = create_word_cloud(res_ana['content_lines'], cloud_pic_dir,csv_flag)
        return img_list, top_10

    top_10 = []
    img_list = glob.glob(os.path.join(cloud_pic_dir,csv_flag+'_*.png'))
    if len(img_list)>0:
        img_list = [os.path.basename(x) for x in img_list]
        top_words_file = os.path.join(cloud_pic_dir, csv_flag + "_top_words_tab.txt")
        with open(top_words_file, 'r') as fp:
            for line in fp.readlines()[:10]:
                top_10.append(line.split('\t')[0])
        return img_list, top_10
    else:
        return create_word_cloud(res_ana['content_lines'], cloud_pic_dir,csv_flag)



# 行为日志分析功能
def log_analyz(log_file_full_path):
    res_ana = {'tryed_times':0}

    return res_ana




if __name__ == '__main__':
    img_list, top_10 = word_cloud_generate(os.path.join(BASE_DIR,'data/20200528_Chat_5d49d5e5a0fa8888e12851bc36341455.csv'))
    print('ddd')