import bs4
import csv
import re
import sys
import getopt
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main(argv):
    # default args
    start_page = -1
    end_page = -1
    try:
        opts, args = getopt.getopt(argv, "hs:e:", ["s_page=", "e_page="])
    except:
        print('[Error]: lack of parameter or invalid argument, please use \'-h\' for help')
        exit()
    for opt, arg in opts:
        if opt == '-h':
            print('[Usage]: spider.py -s <start_page>(int) -e <end_page>(int)')
            exit()
        elif opt in ("-s", "--s_page"):
            if int(arg) < 1 or int(arg) > 700:
                print('[Error]: start page cannot be lower than 1')
                sys.exit()
            start_page = arg
        elif opt in ("-e", "--e_page"):
            if int(arg) > 700:
                print('[Error]: end page cannot be greater than 700')
                sys.exit()
            if int(arg) < 0:
                print('[Error]: end page cannot be lower than 1')
                sys.exit()
            end_page = arg
        else:
            print('[Error]: lack of parameter or invalid argument, please use \'-h\' for help')
            exit()
    if start_page == -1 or end_page == -1:
        print('[Error]: lack of parameter or invalid argument, please use \'-h\' for help')
        exit()
    fin_anime = [[], [], [], [], [], []]
    #   fin_anime[0] = title,
    #   fin_anime[1] = param,   #   param:  ['views_num','bullet_comment_num','fans_num','score']
    #   fin_anime[2] = tag,     #   tag:    ['tag1',...,'tag_n']
    #   fin_anime[3] = seiyuu.  #   seiyuu: ['json1',...,'json_n']
    #   fin_anime[4] = av_num

    # 20 anime per page
    this_page = 0
    # try:
    for page in range(int(start_page) - 1, int(end_page)):
        this_page = page
        print('==================================================')
        print('WW                get page:' + str(page + 1) + "                  WW")
        print('==================================================')
        one_page = get_fin_anime(page)
        for title in one_page[0]:
            fin_anime[0].append(title)
        for param in one_page[1]:
            fin_anime[1].append(param)
        for tag in one_page[2]:
            fin_anime[2].append(tag)
        for seiyuu in one_page[3]:
            fin_anime[3].append(seiyuu)
        for av_num in one_page[4]:
            fin_anime[4].append(av_num)
        # for img_url in one_page[5]:
        #     fin_anime[5].append(img_url)
    # except Exception as e:
    #     print(e)
    #     print("[Error]: Page " + str(this_page+1) + " cannot be well analyzed.")
    #     exit()
    # form csv
    form_csv(fin_anime)


def form_csv(fin_anime):
    # headers = ['title', 'views', 'bullet_comment', 'fans',
    #            'score', 'tags', 'seiyuu', 'av_num']
    data = [[], [], [], [], [], [], [], []]
    for title in fin_anime[0]:
        data[0].append(title)
    for param in fin_anime[1]:
        data[1].append(param[0])
        data[2].append(param[1])
        if len(param) == 2:
            data[3].append('null')
            data[4].append('null')
        else:
            data[3].append(param[2])
            data[4].append(param[3])
    for tag in fin_anime[2]:
        data[5].append(tag)
    for seiyuu in fin_anime[3]:
        data[6].append(seiyuu)
    for av_num in fin_anime[4]:
        data[7].append(av_num)

    rows = []
    try:
        for i in range(len(data[0])):
            rows.append([data[0][i], data[1][i], data[2][i], data[3][i], data[4][i]
                            , data[5][i], data[6][i], data[7][i]])
    except IndexError as e:
        print(e)
        exit()
    try:
        with open('bilibili_fin_anime.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            # writer.writerow(headers)
            writer.writerows(rows)
    except Exception as e:
        print(e)

    #   download cover
    # for anime in rows:
    #     img_url = 'https://' + anime[7]
    #     with open('./cover_img/' + anime[0] + '.jpg', 'wb') as f_img:
    #         f_img.write(requests.get(img_url).content)


def get_fin_anime(page):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('log-level=3')
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    anime_num = 0
    fin_anime_list = []
    href_list = []
    title_list = []
    param_set = []  # element in param_set: ['views_num','bullet_comment_num','fans_num','score']
    seiyuu_set = []
    av_num_list = []
    img_url_list = []
    view = ''
    url = 'https://www.bilibili.com/v/anime/finish/#/all/default/0/' + str(page + 1) + '/'

    #   get href, title, av_num of every anime
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    # for j in range(1, 8):
    #     js = "var q=document.documentElement.scrollTop=" + str(500 * j)
    #     browser.execute_script(js)
    #     time.sleep(3)
    soup = bs4.BeautifulSoup(browser.page_source, 'lxml')
    div_list = soup.find_all('div', class_='r')
    v_info_list = soup.find_all('span', class_="v-info-i")
    titles = soup.find_all('a', class_='title')
    av_No = soup.find_all('div', class_='l-item')
    href_re = re.compile(r'www.bilibili.com/video/av\d*')
    av_re = re.compile(r'av\d*')
    title_re = re.compile(r'>.*')
    v_info_re = re.compile(r'<span>.*')
    # img_re = re.compile(r'src="[\w\d.@]*')
    for div in div_list:
        href = href_re.findall(str(div))
        href_list.append(href[0])
    for item in titles:
        name = title_re.findall(str(item))[0]
        title_list.append(str(name).lstrip('>').rstrip('</a>'))
    for av in av_No:
        num = av_re.findall(str(av))[0]
        # img_src = img_re.findall(str(av))
        # img_url_list.append(str(img_src[0]).lstrip('src="').rstrip('"'))
        av_num_list.append(num)
    for i in range(len(v_info_list)):
        if i % 2 == 0:
            view = v_info_re.findall(str(v_info_list[i]))
        else:
            comment = v_info_re.findall(str(v_info_list[i]))
            param_set.append([str(view).lstrip('\'[<span><div>').rstrip('</span></div>\']'),
                              str(comment).lstrip('\'[<span><div>').rstrip('</span></div>\']')])
    browser.close()
    print('================================================================================')
    print('WW                                   get titles                              WW ')
    print('================================================================================')
    print(title_list)
    print('================================================================================')
    #   get intro page of every anime
    print('      waiting for getting intro_page urls, about 4 min based on your network    ')
    print('================================================================================')
    href_counter = 0
    intro_page_list = []
    for href_item in href_list:
        browser = webdriver.Chrome(options=chrome_options)
        browser.get('https://' + href_item)
        time.sleep(10)
        browser.get(browser.current_url)
        href_counter += 1
        print('get intro_page urls ' + str(href_counter) + '/20: ' + browser.current_url)
        intro_soup = bs4.BeautifulSoup(browser.page_source, 'lxml')
        intro_div_list = intro_soup.find_all('div', class_='media-info clearfix report-wrap-module')
        intro_href_re = re.compile(r'www.bilibili.com/bangumi/media/md\d*/')
        if len(intro_div_list) == 0:
            intro_page_list.append("Null")
        else:
            for div in intro_div_list:
                intro_page = intro_href_re.findall(str(div))
                if len(intro_page) >= 1:
                    intro_page_list.append(intro_page[0])
                else:
                    intro_page_list.append("Null")
        browser.close()

    #   get tags, scores, fans_num, seiyuu of every anime
    print('waiting for accessing intro_pages:' + str(anime_num + 1) + '/20')
    tag_set = []
    for intro_page in intro_page_list:
        if intro_page != "Null":
            browser = webdriver.Chrome(options=chrome_options)
            browser.get('http://' + intro_page)
            detail_soup = bs4.BeautifulSoup(browser.page_source, 'lxml')
            tags = detail_soup.find_all('span', class_='media-tag')
            if len(detail_soup.find_all('div', class_='media-info-score-content')) == 0:
                score = '<div class="media-info-score-content"> Null </div>'
            else:
                score = detail_soup.find_all('div', class_='media-info-score-content')[0]
            fans = detail_soup.find_all('em')[1]
            print(type(detail_soup.find_all('span', style='opacity: 0;')))
            if len(detail_soup.find_all('span', style='opacity: 0;')) <= 1:
                seiyuu = str(detail_soup.find_all('span', style='opacity: 0;')).\
                    lstrip(' <span class="hide" style="opacity: 0;">').rstrip('</p></span>')
            else:
                seiyuu = str(detail_soup.find_all('span', style='opacity: 0;')[0]). \
                    lstrip(' <span class="hide" style="opacity: 0;">').rstrip('</p></span>')
            print('================================================================================')
            print("WW                        get Seiyuus" + str(anime_num + 1) + '/20                               WW')
            print(seiyuu)
            print('================================================================================')
            tag_list = []
            for tag in tags:
                tag_list.append(str(tag)[24:len(tag) - 8])
            tag_set.append(tag_list)
            param_set[anime_num].append(str(fans).lstrip('<em>').rstrip('</em>'))
            param_set[anime_num].append(str(score).lstrip('<div class="media-info-score-content">').rstrip('</div>'))
            anime_num += 1
            seiyuu_set.append(seiyuu)
        else:
            print("WW                           get Null intro page                              WW")
            tag_set.append(['Null'])
            param_set[anime_num].append('Null')
            param_set[anime_num].append('Null')
            seiyuu_set.append('Null')
            anime_num += 1
    print('================================================================================')
    print("get param:  ['views_num','bullet_comment_num','fans_num','score']")
    print(param_set)
    print('================================================================================')
    print("get_tags")
    print(tag_set)
    print('================================================================================')
    return [title_list, param_set, tag_set, seiyuu_set, av_num_list]


if __name__ == '__main__':
    main(sys.argv[1:])

