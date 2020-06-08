#coding=utf-8
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re, time, requests
from selenium import webdriver
from bs4 import BeautifulSoup

def FindLinks(driver, url, n):
    Links = []
    print(url)
    driver.get(url)
    print("this is FindLinks")
    for i in range(n):
        print(i)
        time.sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    #driver.find_element_by_xpath('//a[@id="expanding_cta_close_button"]').click()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #posts = soup.findAll('div', {'class':'clearfix _ikh _3-8y'})
    #posts = soup.findAll('div', {'class':'clearfix d_zado4aoci'})
    posts = soup.findAll('div', {'class':'_5pcr userContentWrapper'})
    #print(posts)
    for i in posts:
        
        #Links.append('https://www.facebook.com' + i.find('div',{'class':'_3x-2'}).attrs['href'].split('?',2)[0])
        #print(i.find('a',{'class':'_5pcq'}).attrs['href'])
        try:

            link_path = i.find('a',{'class':'_5pcq'}).attrs['href']
            if "www.facebook.com" not in link_path:
                link_path = "https://www.facebook.com" + link_path
                print(link_path)
            else:
                print(link_path)
            Links.append(link_path)
        except:

            print("this is final")
        
    print(Links)
    return Links


def expand(driver, url):
    driver.get(url)
    try:
        driver.find_element_by_xpath('//a[@lang="en_US"]').click()
    except:
        print("Now is in EN_US")
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    try:
        #driver.find_element_by_xpath('//div[@class="_5pcr userContentWrapper"]//a[@data-testid="UFI2CommentsCount/root"]').click()
        driver.find_element_by_xpath('//div[@class="_5pcr userContentWrapper"]//a[@class="see_more_link"]').click()
        #driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #time.sleep(1)
        #driver.find_element_by_id('expanding_cta_close_button').click() 
        print('There is more context!')
    except:
        print('There is less context!')
    k = 1
    #while k != 0:
    #    k = 0
    #    for i in driver.find_elements_by_xpath('//div[@class="_5pcr userContentWrapper"]//div[@data-testid="UFI2CommentsList/root_depth_0"]//a[@role="button"]'): 
    #        if bool(re.search('comment|More|Repl',i.text)) == True :
    #            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    #            time.sleep(2)
    #            #try:
    #            #    driver.find_element_by_xpath('//div[@style="display: block;"]//a[@id="expanding_cta_close_button"]').click()
    #            #except:
    #            #    print('No pupup!')
    #            try:
    #                i.click()
    #            except:
    #                print('Nothing')
    #            time.sleep(2)
    #            k += 1

def PostContent(driver, soup):
    userContent = soup.find('div', {'class':'_5pcr userContentWrapper'})
    print("userContent:")
    #print(userContent)
    #PosterInfo = userContent.find('div', {'class':'p_zado4anar _5eit l_zado4562e clearfix'})
    PosterInfo = userContent.find('div', {'class':'w_1f4ob_guph _5eit j_1f4ob_kc58 clearfix'})
    print("PosterInfo:")
    #print(PosterInfo)
    feedback = soup.find('form', {'class':'commentable_item'})
    print("feedback:")
    print(feedback)
    Name = PosterInfo.find('img').attrs['aria-label']
    print("Name:")
    print(Name)
    #ID = PosterInfo.find('a', {'class':'_5pb8 o_c3pynyi2g _8o _8s lfloat _ohe'}).attrs['href'].split('/?',2)[0].split('/',-1)[-1]
    ID = PosterInfo.find('a', {'class':'_5pb8 s_1f4ob_kc53 _8o _8s lfloat _ohe'}).attrs['href']
    print(ID)
    #ID =1
    Link = driver.current_url
    print("PostContent 7")
    #print(PosterInfo)
    try:
        Time = PosterInfo.find('abbr').attrs['title']
        print("PostContent 8")
    except:
        Time = PosterInfo.find('div', {'class':'_1atc fsm fwn fcg'}).text
        print("PostContent 9")
    try:
        Content = userContent.find('div', {'class':'_5pbx userContent _3576'}).text
    except:
        Content = ""
    print(Content)
    try:
        Like = '0' 
        Like = feedback.findAll(name='a',attrs={"aria-label":re.compile(r'^讚:')})
        #print(soup.find_all(class_=re.compile(‘^sis‘))) #查找類為sister的所有標簽

        Like = feedback.find('a', {'_1n9l':'UFI2TopReactions/tooltip_LIKE'}).find('a').attrs['aria-label']
    except:
        Like = '0' 
    try:
        ANGER = feedback.find('span', {'data-testid':'UFI2TopReactions/tooltip_ANGER'}).find('a').attrs['aria-label']
    except:
        ANGER = '0'
    try:
        HAHA = feedback.find('span', {'data-testid':'UFI2TopReactions/tooltip_HAHA'}).find('a').attrs['aria-label']
    except:
        HAHA = '0'
    try:
        comment = feedback.find('span', {'class':'_3dlh'})
        commentcount = comment.find('span', {'class':'_81hb'}).text
    except:
        commentcount = '0' 
    try:
        share = feedback.find('span', {'class':'_355t _4vn2'}).text
    except:
        share = '0' 
    print("PostContent end")
    print(Name)
    print(Link)
    print(Time)
    print(Content)
    print(Like)
    print(ANGER)
    print(HAHA)
    print(commentcount)
    print(share)
    print("result end ---------------")
    return pd.DataFrame(
        data = [{'Name':Name,
                 'ID':ID,
                 'Link':Link,
                 'Time':Time,
                 'Content':Content,
                 'Like':Like,
                 'ANGER':ANGER,
                 "HAHA":HAHA,
                 'commentcount':commentcount,
                 'share':share}],
        columns = ['Name', 'ID', 'Time', 'Content', 'Like', 'ANGER', 'HAHA', 'commentcount', 'share', 'Link'])
    
def CrawlComment(soup):
    Comments = pd.DataFrame()
    userContent = soup.find('div', {'class':'_5pcr userContentWrapper'})
    userContent = soup.find('div', {'class':'_5pcr userContentWrapper'})
    for i in userContent.findAll('div', {'data-testid':'UFI2Comment/root_depth_0'}):
        try:
            CommentContent = i.find('span', {'dir':'ltr'}).text
        except:
            CommentContent = 'Sticker'
        Comment = pd.DataFrame(data = [{'CommentID':i.find('a', {'class':' _3mf5 _3mg0'}).attrs['data-hovercard'].split('id=',2)[1],
                                 'CommentName':i.find('img').attrs['alt'],
                                 'CommentTime':i.find('abbr',{'class':'livetimestamp'}).attrs['data-tooltip-content'],
                                 'CommentContent':CommentContent,
                                 'Link':driver.current_url}],
                        columns = ['CommentID', 'CommentName', 'CommentTime', 'CommentContent', 'Link'])
        Comments = pd.concat([Comments, Comment], ignore_index=True)
    
    for i in userContent.findAll('div', {'data-testid':'UFI2Comment/root_depth_1'}):
        try:
            CommentContent = i.find('span', {'dir':'ltr'}).text
        except:
            CommentContent = 'Sticker'
        Comment = pd.DataFrame(data = [{'CommentID':i.find('a', {'class':' _3mf5 _3mg1'}).attrs['data-hovercard'].split('id=',2)[1],
                                 'CommentName':i.find('img').attrs['alt'],
                                 'CommentTime':i.find('abbr',{'class':'livetimestamp'}).attrs['data-tooltip-content'],
                                 'CommentContent':CommentContent,
                                 'Link':driver.current_url}],
                        columns = ['CommentID', 'CommentName', 'CommentTime', 'CommentContent', 'Link'])
        Comments = pd.concat([Comments, Comment], ignore_index=True)        
    return Comments

def login(driver):
    
    email_t = driver.find_element_by_id('email')
    email_t.send_keys("xxxxxxx@gmail.com")
    pass_t= driver.find_element_by_id('pass')
    pass_t.send_keys("xxxxxxx")
    driver.find_element_by_id('loginbutton').click()

def set_fb():
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    
    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })
    
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://www.facebook.com/profile.php?id=100004435633198/posts')
    return driver

def main():
    driver = set_fb()
    login(driver)
    Links = FindLinks(driver, url = 'https://www.facebook.com/profile.php?id=100004435633198/posts', n = 500)
    
    PostsInformation = pd.DataFrame()
    PostsComments = pd.DataFrame()
    for i in Links:
        print('Dealing with: ' + i)
        try:
            expand(driver, i)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            #print(soup)
            PostsInformation = pd.concat([PostsInformation, PostContent(driver, soup)],ignore_index=True)
            print("this finished content")
            #PostsComments = pd.concat([PostsComments, CrawlComment(soup)],ignore_index=True)
        except:
            print('Load Failed: ' + i)
    
    #PostsInformation
    #PostsComments
    PostsInformation.to_excel('PostsInformation.xlsx', engine='xlsxwriter')
    #PostsComments.to_excel('PostsComments.xlsx')


if __name__ == '__main__':

        main()

