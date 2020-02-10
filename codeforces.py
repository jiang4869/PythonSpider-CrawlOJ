from pyquery import PyQuery as pq
import requests
import time


def solve_tr(tr):
    """
    解析我们所需要的内容
    :param tr: tr元素
    :return: dict
    """
    problemName = tr.find('.status-small>a').text()
    state = tr.find(':nth-child(6)').text()
    it = {'problemName': problemName, 'state': state}
    return it


def get_pages_num(doc):
    """
    获取需要爬取的页码数量
    :param doc: pyquery返回的解析器
    :return: int,页码数量
    """
    try:
        length = doc.find('#pageContent>.pagination>ul>*').length
        last_li = doc.find('#pageContent>.pagination>ul>li:nth-child(' + str(length-1) + ')')
        # print('length', length)
        print(last_li.text())
        # for item in items:
        #     print(item)

        return max(1, int(last_li.text()))

    except Exception :
        return None


def crawl_one_page(doc):
    """
    爬取每一页中的内容
    :param doc: pyquery返回的解析器
    """
    items = doc.find('[data-submission-id]').items()
    for item in items:
        it = solve_tr(item)
        with open('data.txt', 'a+', encoding='utf-8') as f:
            f.write(str(it) + '\n')
        print(it)


def get_username():
    """
    获取用户名
    :return:
    """
    username = input('请输入用户名：')
    return username


def main():
    base = 'https://codeforces.com/submissions/'
    username = get_username()
    url = base+username+'/page/1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }

    response = requests.get(url=url, headers=headers)
    doc = pq(response.text)
    # 注释部分为测试代码
    # crawl_one_page(doc)
    # with open('index.html', 'w', encoding='utf-8') as f:
    #     f.write(doc.text())
    num = get_pages_num(doc)

    if num is not None:
        for i in range(1, num + 1):
            url = base+username+'/page/'+str(i)
            print(url)
            response = requests.get(url=url)
            doc = pq(response.text)
            crawl_one_page(doc)
            time.sleep(2)

    else:
        print('username is no exist or you are no submission')


if __name__ == '__main__':
    main()
