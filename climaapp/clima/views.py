from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
# Create your views here.
def get_html_content(cidade):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    cidade = cidade.replace(' ','+')
    html_content = session.get(f'https://www.google.com/search?q=weather+in+{cidade}').text
    return html_content

def index(request):
    context_dict = None
    if 'cidade' in request.GET:
        cidade = request.GET.get('cidade')
        html_content = get_html_content(cidade)
        soup = BeautifulSoup(html_content,'html.parser')
        regiao = soup.find('div',attrs={'id':'wob_loc'}).text
        diahora = soup.find('div',attrs={'id':'wob_dts'}).text
        status = soup.find('span',attrs={'id':'wob_dc'}).text
        temperatura = soup.find('span',attrs={'id':'wob_tm'}).text
        dicionario ={'regiao':regiao,'diahora':diahora,'status':status,'temperatura':temperatura,}
        context_dict = {'tempo':dicionario}

    return render(request,'clima/index.html',context_dict)
