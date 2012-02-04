# -*- coding: utf-8 -*-
'''
filedesc: default controller file
'''
from noodles.http import Response,Redirect
from noodles.templates import render_to_string

import yaml
cfg = yaml.load(open('config.yaml','r').read())

import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re,hashlib,time,datetime




scopes = [
    'https://spreadsheets.google.com/feeds/']
secure=False
session=True

#this is where we store user sessions
usessions={}

#this is used for quicker debugging
TALKOUT=True

def index(request):
    scook = request.cookies.get(cfg['cookie']['name'])
    resp = Response()
    #initialize a new session if we have to
    if not scook or scook not in usessions:
        print 'initializing cookie'
        sessm = hashlib.md5()
        sessm.update(str(time.time())+cfg['cookie']['salt'])
        sessval = sessm.hexdigest()
        resp.set_cookie(cfg['cookie']['name'],sessval)
        usessions[sessval]={'created':datetime.datetime.now()}
    else:
        sessval = scook
    sess = usessions[sessval]
    #initialize our gd_client object if we don't have one
    if 'gd_client' not in sess and TALKOUT:
        print 'initializing gd client'
        gd_client = gdata.spreadsheet.service.SpreadsheetsService()    
        single_use_token = gdata.auth.extract_auth_sub_token_from_url(request.url)
        nxt = cfg['host']

        rdu  = gdata.service.GenerateAuthSubRequestUrl(cfg['host'], scopes, secure=secure, session=session)    
        rd = Redirect(rdu)
        if not single_use_token:
            print 'redirecting to %s'%rdu
            return rd
        else:
            print ('using token %s'%single_use_token)
            try:
                gd_client.UpgradeToSessionToken(single_use_token)
            except gdata.service.TokenUpgradeFailed,uf:
                print 'failed upgrade - %s'%uf
                return rd
        sess['gd_client']=gd_client
    else:
        print 'using existing gd client'
        if TALKOUT:
            gd_client = sess['gd_client']
        else:
            gd_client = None #simulation mode

    spread_id = cfg['document']['spread_id']
    worksheet_id = cfg['document']['worksheet_id']
    #feed = gd_client.GetWorksheetsFeed(str_spread_id)
    # worksheet = feed.entry[0]
    # worksheet_id_parts = worksheet.id.text.split('/')
    # worksheet_id = worksheet_id_parts[len(worksheet_id_parts) - 1]
    errs={} 
    p={} ; pout = {}
    written=False
    if request.method=='POST':
        p = dict(request.params) ; pout = dict(request.params)
        
        #validate our input
        if not p.get('to'): errs['to']='No recipient specified'
        if not p.get('amt'): errs['amt']='No amount specified'
        if not re.compile('^([0-9\.]+)$').search(p.get('amt')): errs['amt']='Amount must be a number'
        if not p.get('method'): errs['method']='No method specified'
        if p.get('method') not in cfg['methods']: errs['method']='Invalid method'
        if not p.get('currency'): errs['currency']='No currency specified'
        if p.get('currency') not in cfg['currencies']: errs['currency']='Invalid currency'
        if not p.get('when'): errs['when']='No date specified'
        if p.get('when'):
            try:
                when = datetime.datetime.strptime(p.get('when'), "%Y-%m-%dT%H:%MZ" )
            except:
                errs['when']='Could not parse ISO date'
            pout['when']=when.strftime('%m/%d/%Y %H:%M')
        #if we pass validation, let's write!
        if not len(errs):
            out_arr=dict(pout)
            del out_arr['enter']

            if TALKOUT:
                print 'writing %s to spread %s, worksheet %s'%(out_arr,spread_id,worksheet_id)
                entry = gd_client.InsertRow(out_arr , spread_id, worksheet_id)
                written=True
                p={}
    def vl(fn):
        return p.get(fn) or ''
    rstr= render_to_string('/index.html',{'lists':{'currencies':cfg['currencies'],'methods':cfg['methods']}
                                          ,'tags':cfg['tags']
                                          ,'origins':cfg['origins']
                                          ,'recievers':cfg['recievers']
                                          ,'errs':errs
                                          ,'f':pout
                                          ,'vl':vl
                                          ,'written':written})
    resp.body = rstr
    return resp
