import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup as  bs 
import json
import time
import requests 
import base64
from auth_data import sokolovcredentials


ring = 'ольцо'
ring2 = 'ечатка'
brosh = 'рошь' 
brace = 'раслет'
earrings = 'ерьги'
earring = 'ерьга'
drop = 'одвеска'
necklace = 'олье'
chain = 'епь'
piercing = 'ирсинг'
necklace2 = 'нур'
necklace3 = 'рест'
bombom = 'олокольчик'
spoon = 'ожка'


def addsclean(list):
   
            
    str2 = []
    for item in list: 
        if item not in str2:          #delete doubles
            str2.append(item)
        
 
    str2 =','.join(str2)
    return str2.lower()

    
def namer():
    try:
      if ring   in title:
          return   'Кольцо SOKOLOV ' + article + ' ' + material.lower()
      elif bombom   in title:
          return   'Колокольчик SOKOLOV ' + article + ' ' + material.lower()
      elif spoon   in title:
          return   'Ложка SOKOLOV ' + article + ' ' + material.lower()        
      elif ring2 in title:
          return      'Кольцо SOKOLOV ' + article + ' ' + material.lower()
      elif brace in title:
          return      'Браслет SOKOLOV ' + article + ' ' + material.lower()
      elif necklace2 in title:
          return      'Колье SOKOLOV ' + article + ' ' + material.lower()    
      elif brosh  in title:
          return  'Брошь SOKOLOV ' + article + ' ' + material.lower()
      elif earrings  in title:
          return      'Серьги SOKOLOV ' + article + ' ' + material.lower()
      elif earring in title:
          return    'Серьга SOKOLOV ' + article + ' ' + material.lower()
      elif drop in title:
          return    'Подвеска SOKOLOV ' + article + ' ' + material.lower()
      elif necklace  in title:
          return    'Колье SOKOLOV ' + article + ' ' + material.lower()
      elif chain  in title:
          return     'Цепь SOKOLOV ' + article + ' ' + material.lower()
      elif piercing  in title:
          return     'Пирсинг SOKOLOV ' + article + ' ' + material.lower()
      elif necklace3  in title:
          return     'Подвеска SOKOLOV ' + article + ' ' + material.lower()    
      else:
          return  'SOKOLOV ' + title
    except:
      return "Изделие"


credentials = sokolovcredentials
credentials =  credentials.encode()
credentials = base64.b64encode(credentials)
credentials = credentials.decode()

r = requests.post('https://api.b2b.sokolov.net/ru-ru/login', headers={'Authorization':f'Basic {credentials}'} )
r= r.json()
access_token = r['access_token']

headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': f'Bearer {access_token}'
  
}


body = {
  "page": 1,
  "size": 240,
  "filter": {
        "and": [
            {
                "and": [
                    {
                        "material": "Золото"
                    }
                ]
            },
            {
                 
               
            }
        ]
    }

}
r = requests.post('https://api.b2b.sokolov.net/ru-ru/catalog/products', headers=headers, json=body )

r= r.json()
pagecount = r['meta']['page-count']

print(pagecount)

data = []
for i in range(1, pagecount+1):

  seconds = time.time()
  local_time = time.ctime(seconds)
  print("Local time:", local_time, 'page', i, 'of', pagecount)


  body = {
    "page": i,
    "size": 240,
    "filter": {
          "and": [
              {
                  "and": [
                      {
                          "material": "Золото"
                      }
                  ]
              },
              {
                  
                
              }
          ]
      }

  }



  r = requests.post('https://api.b2b.sokolov.net/ru-ru/catalog/products', headers=headers, json=body )
  items = r.json()

  with open(f'data.txt', 'w') as f:
    json.dump(items,f)

  #with open('data.txt', 'r') as outfile:
  #    items  = json.load(outfile)

  items = items['data']

  
  
  for each in items:
    
    brand = 'SOKOLOV'
    hassize = each['attributes']['has-sizes'] 
    title = each['attributes']['title']
    article = each['attributes']['article']
    material = each['attributes']['material']
    materialplating = each['attributes']['material-plating']
    probe  = each['attributes']['probe']
    category = each['attributes']['category'].replace('Кресты','Подвески').replace('Кольца обручальные','Кольца').replace('Пирсинги','Пирсинг').replace('Иконки','Подвески').replace('Шнуры декоративные','Колье').replace('Шармы','Подвески')
    if category == 'Печатки' :
      category = 'Кольца'
      male = 'Мужские'
    elif category == 'Цепи':
      male = 'Унисекс'
    elif category == 'Браслеты' :
      male = 'Унисекс' 
    else:
      male = 'Женские'

    if materialplating == 'Золочение':
      gilding = 'Да'
      ifgold = ' с позолотой'
    else:
      gilding = ''
      ifgold = ''    
    quantity = each['attributes']['balance']['quantity']
    production = each['attributes']['whom-production']
    imagelink = each['attributes']['photo']
    weight = each['attributes']['total-weight']
    try:

      entryprice = each['attributes']['trade-price']
      entryprice = round(entryprice*6)
      wholesaleprice = round((entryprice * 0.3 + entryprice),-2)
      price = round((entryprice * 0.6 + entryprice + 1500),-2)
      minprice = round((price - price*0.2),-2)
    except:
      print(article,' - There is no price here')
    
    insertslist = []  
    try:
      
      inserts = each['attributes']['inserts']
      for insert in inserts:
        insertslist.append(insert['name'])
      
      adds = addsclean(insertslist).replace('недраг','')  
      
    except:
      adds = ''
    
    if (hassize== True):
      sizes = each['attributes']['sizes']
      for each in sizes:
        size = each['size']
        sizecount = each['balance']['quantity']
        if int(sizecount) >1:
          s = 'ольцо'
          if (s in title):
              unit = 'р'
          else:
              unit = 'см'
          namesize = size.replace(',', '-')

          name = namer() +ifgold + f' {adds}' + f' {size}' + unit
          art2 = article+f'_{namesize}'

          sum = [name,art2,material,materialplating,gilding,adds,weight,size,sizecount,price,wholesaleprice,entryprice,minprice,imagelink,probe,brand,production,category,male]

            
          data.append(sum)
    
    else:
      size = ''
      name = namer() + ifgold + f' {adds}'
      sum = [name,article,material,materialplating,gilding,adds,weight,size,quantity,price,wholesaleprice,entryprice,minprice,imagelink,probe,brand,production,category,male]
      if int(quantity) > 1:  
        data.append(sum)

df = pd.DataFrame(data)

try:
  df.to_excel('sokolovapi - золото.xlsx')
except:
  df.to_excel('sokolovapiii - золото.xlsx')  