from flask import Flask,request
from jira import JIRA
from atlassian import Confluence
import time
import requests
import json
import pyodbc


username = 'vasundhara.chauhan@innovaccer.com'
password = 'Innovaccer@123'
jira = JIRA(basic_auth=(username, password), options = {'server': 'https://support.innovaccer.com/'})
projects = jira.projects()
print(projects)
urljira = "https://support.innovaccer.com/rest/project-templates/1.0/createshared/10580"
headersjira = {
  'vasundhara.chauhan@innovaccer.com': 'Innovaccer@123',
  'Content-Type': 'application/json',
  'Authorization': 'Basic dmFzdW5kaGFyYS5jaGF1aGFuQGlubm92YWNjZXIuY29tOklubm92YWNjZXJAMTIz'
}



app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def helloIndex():
    if request.method == 'POST':

      
      
        z=str(request.headers.get('project_name'))
        print(z[:3])
        leadName=request.headers.get('project_lead')
        keyName=z[:3].upper()
        print(keyName)
        print(leadName)
        payload = { "key": keyName,"name": z,"lead": leadName }
       
        payloadjira=json.dumps(payload)
        print(payloadjira)
        response = requests.request("POST", urljira, headers=headersjira, data = payloadjira)
  
        print(response)      
        
    return 'hello daksh'



@app.route('/incustomer',methods=['GET', 'POST'])
def webpage():
    return """<iframe src="https://apps.powerapps.com/play/f25e48bc-65f0-4f33-aeac-576c1b98ae34?source=iframe" 
            frameborder="0" 
            marginheight="0" 
            marginwidth="0" 
            width="100%" 
            height="100%" 
            scrolling="auto"></iframe>"""  
  
@app.route('/securitytest',methods=['GET'])
def azure():

    try:
      drivers = [item for item in pyodbc.drivers()]
      print(drivers)
      driver = drivers[-1]
      print("driver:{}".format(driver))
      server = 'incustomer.database.windows.net'
      database = 'inno' 
      uid = 'inno@incustomer'
      pwd = '{$Dell2020@#12}' 

      con_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}'
      print(con_string)
      cnxn = pyodbc.connect(con_string)
      
    except Exception as e: 
      print(e)
      print('brooo')
    return 'TEST PASSED'  

@app.route('/confluence/',methods=['GET', 'POST'])
def confluenceapi():
  
    URL = 'https://innovaccer.atlassian.net/wiki'
    USER = 'daksh.singhal@innovaccer.com'
    PASS = 'XaTy5HruIAFDtTGyUwL93C83'

    confluence = Confluence(
        url = URL,
        username = USER,
        password = PASS)

    if request.method == 'POST':

        projconfluence=str(request.headers.get('confluence_name'))
        print(projconfluence+'conf')
        keyName=projconfluence[:3].upper()
        print(keyName)

        #print(response)
        dest_space=keyName
        dest_space_name=projconfluence

        def search_space_exists(dest_space):
            print('hey')
            flag = 0
            try:
                resp = requests.get(URL + '/rest/api/space?spaceKey=' + dest_space, headers=get_header(), auth=(USER,PASS))
                print(resp)
                if not resp.status_code // 100 == 2:
                    print("Error: Unexpected response {}".format(resp))
                else:
                    if not resp.json()['results']:
                        flag = 1
                        print('1')
                    return flag
            except requests.exceptions.RequestException as e:
                print("Error: {}".format(e))
                return 'Failed'
        print('Done with search')
        def create_space(dest_space, dest_space_name):

            payload = json.dumps({
                "key" : dest_space,
                "name" : dest_space_name,
                "metadata" : {}
            })

            try:
                resp = requests.request("POST", URL + '/rest/api/space', data=payload, headers=get_header(), auth=(USER, PASS))
                if not resp.status_code // 100 == 2:
                    print("Error: Unexpected response {}".format(resp))
                else:
                    print('Space Created!')
            except requests.exceptions.RequestException as e:
                # A serious problem happened, like an SSLError or InvalidURL
                print("Error: {}".format(e))
        print('Done with creation')
        def get_page_title(dest_space):

            res = requests.get(URL + '/rest/api/space/' + dest_space + '?expand=homepage', headers=get_header(), auth=(USER, PASS))

            if not res.status_code // 100 == 2:
                print("Error: Unexpected response {}".format(res))
            else:
                print('Title obtained!')
                return res.json()['homepage']['title']
        print('Done with title')
        def main():

            print('in main')
            SOURCE_SPACE = 'CS'
            SOURCE_PAGE_TITLE = 'Customer Lifecycle'
            DEST_SPACE = dest_space
            DEST_SPACE_NAME = dest_space_name
            required_pages = ['Kick-Off','Implementation','UAT / Training','Support','Growth']
            print(required_pages)

            chk = search_space_exists(DEST_SPACE)
            print(chk)
            if chk:
                create_space(DEST_SPACE, DEST_SPACE_NAME)
                print('space created')
                DEST_SPACE_TITLE = get_page_title(DEST_SPACE)
                print('space created')
                srcPageID = confluence.get_page_id(SOURCE_SPACE, SOURCE_PAGE_TITLE)
                print(srcPageID)
                destPageID = confluence.get_page_id(DEST_SPACE, DEST_SPACE_TITLE)
                print('space created')
                load_content(srcPageID, destPageID, SOURCE_PAGE_TITLE)
                print('loaded')
            elif chk == 'Failed':
                print('API not working.')
            else:
                print('Space already exists!')

        print('Done with main')
        
        def get_header():

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            return headers
        print('Done with search')
        def get_url(src_pid):

            url = URL + '/rest/api/content/' + src_pid + '/pagehierarchy/copy'

            return url
        print('Done with search')
        def copy_page_hierarchy(src_pid, dest_pid, src_title):

            payload = json.dumps( {
            "copyAttachments": True,
            "copyPermissions": True,
            "copyProperties": True,
            "copyLabels": True,
            "originalPageId": src_pid,
            "destinationPageId": dest_pid,
            "titleOptions": {
                "prefix": "",
                "replace": src_title,
                "search": src_title
            }
            } )

            return payload
        print('Done with search')
        def load_content(src_pid, dest_pid, src_title):

            url = get_url(src_pid)
            body = copy_page_hierarchy(src_pid, dest_pid, src_title)
            headers = get_header()

            try:
                resp = requests.request("POST", url, data=body, headers=headers, auth=(USER, PASS))

                # Consider any status other than 2xx an error
                if not resp.status_code // 100 == 2:
                    print("Error: Unexpected response {}".format(resp))
                else:
                    print(resp.json())
                    print('Page Created!')

            except requests.exceptions.RequestException as e:

                # A serious problem happened, like an SSLError or InvalidURL
                print("Error: {}".format(e))
        print('Done with search')
        main()

    return "hello daku-confluence"

        

if __name__ == '__main__':
    
    app.run()
