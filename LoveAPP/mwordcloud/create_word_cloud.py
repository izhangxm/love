import jieba
import codecs
import sys
import pandas
import numpy as np
import imageio
from wordcloud import WordCloud, ImageColorGenerator
from os import listdir
from os.path import isfile, join
from Love.settings import BASE_DIR
import os


stopwords_filename = os.path.join(BASE_DIR,'LoveAPP/mwordcloud/data/stopwords.txt' )
font_filename = os.path.join(BASE_DIR,'LoveAPP/mwordcloud/fonts/STFangSong.ttf' )
template_dir = os.path.join(BASE_DIR,'LoveAPP/mwordcloud/data/templates/' )

def create_word_cloud(content_lines,des_dir,csv_flag):
    content = '\n'.join([line.strip() for line in content_lines if len(line.strip()) > 0 and line[0] != '<' and line[0] != '\"' and line[0] != "	"])
    stopwords = set([line.strip() for line in codecs.open(stopwords_filename, 'r', 'utf-8')])

    segs = jieba.cut(content)
    words = []
    for seg in segs:
        word = seg.strip().lower()
        if len(word) > 1 and word not in stopwords:
            words.append(word)

    words_df = pandas.DataFrame({'word': words})
    words_stat = words_df.groupby(by=['word'])['word'].agg(np.size)
    words_stat = words_stat.to_frame()
    words_stat.columns = ['number']
    words_stat = words_stat.reset_index().sort_values(by="number", ascending=False)

    print('# of different words =', len(words_stat))
    img_list= []

    prefix_time = csv_flag
    for file in listdir(template_dir):
        if file[-4:] != '.png' and file[-4:] != '.jpg':
            continue
        background_picture_filename = join(template_dir, file)
        if isfile(background_picture_filename):
            prefix = str(file.split('.')[0])

            bimg = imageio.imread(background_picture_filename)
            wordcloud = WordCloud(font_path=font_filename, background_color='white',
                                  mask=bimg, max_font_size=600, random_state=100)
            wordcloud = wordcloud.fit_words(
                dict(words_stat.head(100).itertuples(index=False)))

            bimgColors = ImageColorGenerator(bimg)
            wordcloud.recolor(color_func=bimgColors)
            file_name = prefix_time + "_" + prefix + '.png'
            output_filename = os.path.join(des_dir, file_name)
            img_list.append(file_name)

            print('Saving', output_filename)
            wordcloud.to_file(output_filename)

    top_words_file = os.path.join(des_dir,prefix_time + "_top_words_tab.txt")
    top_word = open(top_words_file,'w')
    tmp = words_stat.head(len(words_stat))
    # print(tmp)
    # print(tmp.shape)
    # print(tmp.iloc[0])
    # print(tmp.iloc[0][0])
    top_10 = []
    for i in range(len(words_stat)):
        top_word.write("{}\t{}\n".format(str(tmp.iloc[i][0]),str(tmp.iloc[i][1])))
        if i<10:
            top_10.append(str(tmp.iloc[i][0]))
    # print(words_stat.head(10))
    return img_list,top_10
