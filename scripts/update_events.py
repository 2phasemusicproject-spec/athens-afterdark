"""Fetch Athens electronic music listings from Ticketmaster Discovery API.
Requires TICKETMASTER_API_KEY environment variable. Never commit the key.
"""
import json, os, urllib.parse, urllib.request, datetime, pathlib, re
KEY=os.environ.get('TICKETMASTER_API_KEY','').strip()
if not KEY: raise SystemExit('Missing TICKETMASTER_API_KEY secret; events.json unchanged.')
ROOT=pathlib.Path(__file__).resolve().parents[1]
API='https://app.ticketmaster.com/discovery/v2/events.json'
now=datetime.datetime.now(datetime.timezone.utc)
start=now.strftime('%Y-%m-%dT%H:%M:%SZ')
end=(now+datetime.timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ')
results={}
# Multiple queries to cover genre/artist descriptions; API coverage varies by market.
for keyword in ('techno','house','electronic','trance','drum and bass','rave','DJ','dance music'):
    for page in range(2):
        params={'apikey':KEY,'city':'Athens','countryCode':'GR','keyword':keyword,'startDateTime':start,'endDateTime':end,'size':100,'page':page,'sort':'date,asc'}
        req=urllib.request.Request(API+'?'+urllib.parse.urlencode(params),headers={'User-Agent':'AthensAfterdark/2.0'})
        try:
            with urllib.request.urlopen(req,timeout=25) as resp: payload=json.load(resp)
        except Exception as exc:
            raise SystemExit(f'API request failed; keeping previous data: {exc}')
        batch=payload.get('_embedded',{}).get('events',[])
        for item in batch:
            venues=item.get('_embedded',{}).get('venues',[])
            venue=venues[0] if venues else {}
            city=venue.get('city',{}).get('name','')
            country=venue.get('country',{}).get('countryCode','')
            if country and country!='GR':continue
            if city and not re.search(r'athens|αθήν|αθην',city,re.I):continue
            dates=item.get('dates',{}).get('start',{})
            date=dates.get('dateTime')
            if not date:continue # do not invent event time
            link=item.get('url','')
            if not link.startswith('https://'):continue
            classifications=item.get('classifications',[])
            genre_text=' '.join(str(c.get('genre',{}).get('name',''))+' '+str(c.get('subGenre',{}).get('name','')) for c in classifications).lower()
            hay=(item.get('name','')+' '+genre_text+' '+keyword).lower()
            genre='Electronic'
            for needle,label in [('hard techno','Hard Techno'),('drum and bass','Drum & Bass'),('drum & bass','Drum & Bass'),('trance','Trance'),('techno','Techno'),('house','House'),('melodic','Melodic')]:
                if needle in hay:genre=label;break
            event={'id':'tm-'+str(item.get('id','')),'name':item.get('name',''),'date':date,'venue':venue.get('name','Athens'),'genre':genre,'artist':'','url':link,'source':'Ticketmaster'}
            if event['id']!='tm-' and event['name']:results[event['id']]=event
        if len(batch)<100:break
            from event_ai import filter_events

for event in results.values():
    event["city"] = "Athens"
    event["country"] = "GR"

results = {e["id"]: e for e in filter_events(results.values())}
output={'status':'configured','source':'Ticketmaster Discovery API','updatedAt':now.isoformat().replace('+00:00','Z'),'events':sorted(results.values(),key=lambda e:e['date'])}
(ROOT/'events.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Wrote {len(results)} listings to events.json')
