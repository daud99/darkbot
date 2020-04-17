from search.darkbot.read_html import read_html
from search.darkbot.tor_connection import connect_tor
import requests
import re
import time
import validators
from bs4 import BeautifulSoup


def get_emails(current_obj):
    """Finds all emails associated with node

    Args:
        node (LinkNode): node used to get emails from
    Returns:
        emails (list): list of emails
    """
    #print('hello i m in get_emails')
    emails = []
    #response = node.response.text
    mails = re.findall(r'[\w\.-]+@[\w\.-]+', current_obj.html)
    mails=set(mails)
    for email in mails:
        if Crawler.valid_email(email):
            #print("self.uri is in getemails : " + node.uri)
            emails.append([email, current_obj.currenturl, current_obj.channel_name])
    return emails

class Crawler:

    def __init__(self, initialState, channel_name):

        if not initialState.startswith('http'):
            initialState = 'http://'+initialState

        if initialState[-1] == '/':
            initialState = initialState[0:len(initialState)-1]
        self.initialState = initialState
        baseState_parts = initialState.split('.')
        baseState = baseState_parts[0]+'.'+baseState_parts[1]
        self.baseState = baseState
        self.channel_name = channel_name
        self._emails = []
        self.html = ''
        self.currenturl = ''

    @property
    def emails(self):
        #print('email func')
        """
        Getter for node emails
        """
        if not self._emails:
            self._emails = get_emails(self)
        return self._emails

    @staticmethod
    def valid_email(email):
        #print('i m in validator of email')
        """Static method used to validate emails"""
        if validators.email(email):
            return True
        return False

    def get_ignored_extensions(self):
        IGNORED_EXTENSIONS = {'pdf', 'exe', 'rar', 'png', 'PNG', 'jpg',
					  'JPG', 'mp4', 'xlsx', 'doc', 'swf', 'zip',
					  '7z', 'md', 'css', 'js', 'docx', 'diff', 'py',
					  'ico', 'svg', 'md', 'atom', 'git', 'txt', 'patch',
					  'map', 'rc', 'json', 'ttf', 'otf', 'eot', 'woff',
					  'woff2', 'woff3', 'scss', 'less', 'bak', 'conf', 
					  'bak2', 'yml', 'xml', 'jade', 'rst'}
        return IGNORED_EXTENSIONS
    def find_ignored_words(self, link):
        ignored_word = ['signin', 'login', 'sign','auth','?']
        for i in range(0, len(ignored_word)):
            if ignored_word[i] not in link:
                return True
            else:
                return False

    def link_validator(self, raw_anchors, currentNode):
        
        #if currentNode.endswith('.php')
        if currentNode.endswith('.html') or currentNode.endswith('.php'):
            #currentNode = currentNode[0:len(currentNode)-5]
            temp2 = currentNode.rindex('/')
            currentNode = currentNode[0: temp2+1]
        '''
        if currentNode.endswith('/index'):
            currentNode =currentNode[0:len(currentNode)-6]
        '''
        valid_links =[]
        

        for x in raw_anchors:
            if self.find_ignored_words(x):
                node = x
                temp_node = node.split('.')
                if temp_node[-1] in self.get_ignored_extensions():
                    continue
                elif node.startswith('http') or node.startswith('https'):
                    
                    node_parts = node.split('/')
                    node_1 = node_parts[2]
                    x = self.initialState.split('://')[1]
                    if node_1.startswith(x):
                        
                        valid_links.append(node)
                elif node.startswith(self.baseState.split("//")[1]):
                    valid_links.append(node)



                else:
                    if currentNode.endswith('/'):
                        currentNode = currentNode[0:len(currentNode)-1]
                    if '://' not in node:
                        if node.startswith('/'):
                            node = currentNode + node
                            valid_links.append(node)
                        elif '#' in node:
                            continue
                            
                        else:
                            #temp1 = node.split('')
                            if ':' not in node:
                                node = currentNode+'/'+node
                                valid_links.append(node)
        return valid_links

    def BFS(self):
        final_email_list = []
        #print("This is path")
        currentNode = self.initialState

        '''
        if currentNode == goalState:
            return [goalState]
        '''
        frontier = [currentNode]
        explored= []

        end_time = time.time() + 40
        while (len(frontier)!=0 and time.time() < end_time):
            currentNode = frontier.pop(0)
            explored.append(currentNode)
            html = read_html(currentNode)

            if html not in [None,""]:
                self.currenturl = currentNode
                self.html = html
                print('Email and link for this url are below: '+self.currenturl)
                email_list=get_emails(self)
                for each_email in email_list:
                    print(each_email)
                #print(email_list)
                final_email_list.extend(email_list)
                #print("finallist")
                #print(final_email_list)
                #print('i m back')
                try:
                    bs = BeautifulSoup(html, 'html.parser')
                except AttributeError as a:
                    #print("Error while reading data at", url)
                    continue
                raw_achor_tags = bs.find_all('a')
                raw_achors= []
                for link in raw_achor_tags: 
                    if 'href' in link.attrs:

                        raw_achors.append(link.attrs['href'])
                print('link')
                for link in raw_achors:
                    print(link)
                valid_links = self.link_validator(raw_achors, currentNode).copy()
                for child in valid_links:
                    if child not in frontier and child not in explored:
                        '''
                        r = requests.get(child)
                        if(r.status_code==200):
                        '''
                        frontier.append(child)
                        #print(child)
                        
                        #print('Error')
        #print("explored")
        #print(explored)
        #print(final_email_list)
        return final_email_list


if __name__ == "__main__":
    c = Crawler("http://cardingeokeo3r6z.onion/wisdom/index.html")
    c.BFS()