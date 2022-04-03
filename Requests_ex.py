import requests
from bs4 import BeautifulSoup
import re

#2
def tokenize_sentence(text):
    sentences = re.split('(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?|\\!)\\s', text)
    print("All sentence are ======================:",text,sentences)
    return sentences


def into_words(sentence):
    sentence = sentence.lower()
    sentence = re.findall('[a-z]\w+', sentence)
    #return all words of sentence
    return sentence


def remove_punctuation(s):
    return re.sub(r'[^\w\s]', '', s)


def binarySearch(arr, x):
    arr = sorted(arr)
    l = 0
    r = len(arr) - 1
    while l <= r:
        m = l + int(((r - l) / 2))
        if x == arr[m]:
            return m
        if x > arr[m]:
            l = m + 1
        else:
            r = m - 1
    return -1


def compare(sent1, sent2):
    #sent1 is user given snetencs words and its each word is getting check in from sent2 (website given sentence words)
    count = 0
    for x in sent1:
       if binarySearch(sent2, x) != -1:
            count += 1

    # print(count, sent2)

    n1 = len(sent1)
    n2 = len(sent2)

    if n1 == 0 or n2 == 0:
        return 0

    return float(100 * (count / n1)) #* (min(n1, n2) / max(n1, n2))

#7
def get_urls(sent):
    Base_string = "https://www.google.com/search?q="
    Google_Search = Base_string + sent
    res = requests.get(Google_Search)                  #get google seach response "a html page of google holding all searches"
    soup = BeautifulSoup(res.text, 'html5lib')           #extraxt all text 

    links_list = []

    links = soup.findAll("a")                       #find all <a> tag came from google search


    #convert above given links in a link form one  by one
    for link in links:
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            links_list.append(link.get('href').split("?q=")[1].split("&sa=U")[0])              

    links = []
    count = 0
    
   
    # only top  5 links is included excluding youtube links
    for x in links_list:
        if count == 5:
            break
        if 'youtube' not in x and 'pdf' not in x:
            links.append(x)
            count += 1
    
    print(links , " of sentenc" , sent)        
    return links


def get_original_words(sent):
    original_words = remove_punctuation(sent)
    original_words = into_words(original_words)
    original_words = sorted(original_words)
    return original_words

#8
def get_text_from_url(url):
    try:
        
        inside_webpage = requests.get(url)
    except:
        return []

    soup2 = BeautifulSoup(inside_webpage.text, 'html.parser')

    paragraphs = soup2.select('p')

    string2 = ''
    
    #add all pragrapgh tag into single para
    for para in paragraphs:
        string2 += para.text
    
   

    #all senences as a elemnt in list
    website_sent = tokenize_sentence(string2)
   
    website_words = []

    for sent in website_sent:
        sent = remove_punctuation(sent)
        website_words.append(into_words(sent))
    
  

    return website_words

#checking sent1 (user given sentence) 

def check(sent1, sent_website):
    result = []
    #sent1 is single sentence words
    for sent in sent_website:
        k = compare(sent1, sent)
        # print(k, sent)
        # k is % copied
        result.append(k)
    print(result)
    return result

#4
def check_one_sent(sent):
    ans = []
    url = get_urls(sent)
    #ech url we are cheking with user given sentence and  5 url is there
    for x in url:
        
        website_words = get_text_from_url(x)               #getting all words from url
        original_words = get_original_words(sent)

        #original words is soreted
        ans.append(check(original_words, website_words))
    
   
    #ans is %copied from  urls
    return ans, url

#5
def find_max_url(ans, url):
    #ans is % 
    mx = 0
    count = -1
    url_ans = ""
    for x in ans:
        count += 1
        for y in x:
            if y > mx:
                mx = y
                url_ans = url[count]

    return mx, url_ans

#3
def get_ans_for_one_sent(sent):
    ans, url = check_one_sent(sent)
    mx, url_ans = find_max_url(ans, url)
    return mx, url_ans

def myfun(x):
    return x[0]

#1
def main_function(txt):
    all_sentences = tokenize_sentence(txt)
    ans = []
    for x in all_sentences:
        if len(into_words(x)) <= 3:
            print(x , " less length sent ")
            continue
        prob, url_ans = get_ans_for_one_sent(x)
        ans.append([prob, url_ans, x])
    print("--- ---=========55555555==========",ans)   
    ans.sort(key=myfun,reverse=True)
    return ans