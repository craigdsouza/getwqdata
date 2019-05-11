import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class habList(scrapy.Spider):
    name = "habList"
    #start_urls = ['https://indiawater.gov.in/IMISReports/NRDWPMain.aspx']
    start_urls = ['https://indiawater.gov.in/IMISReports/IMISReportLogin.aspx']
    
    def parse(self,response):
        viewstate = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
        viewstategen = response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        eventvalidation = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()
    
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                '__EVENTTARGET':'',
                '__EVENTARGUMENT':'',
                '__VIEWSTATE':viewstate,
                '__VIEWSTATEGENERATOR':viewstategen,
                '__EVENTVALIDATION':eventvalidation,
                'txtUsername':'',
                'txtPassword':'',
                'Btnlogin':'Log in',
                'txtSaltedHash':''},
            callback=self.homeToHabList
        )
    
    def homeToHabList(self,response):
        habLink = response.xpath('//*[@id="rpt_ctl01_rptinner_ctl01_aa"]/@href').get()
        if habLink is not None:
            yield response.follow(habLink, callback=self.habListHome)
        return 
            
    def habListHome(self,response):
#         # save html
#         filename = "habTableIndia.html"
#         with open(filename, 'wb') as f:
#             f.write(response.body)
        
        # parse hidden values
        viewstate1 = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
        viewstategen1 = response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        eventvalidation1 = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()
        #chosenYr = response.xpath('//*[@id="ctl00_ContentPlaceHolder_ddfinyear"]/option[11]/text()').extract_first()     # vulnerable to change
        stateCodes = response.xpath('//*[@id="ctl00_ContentPlaceHolder_ddState"]/option/@value').extract()
        stateNames = response.xpath('//*[@id="ctl00_ContentPlaceHolder_ddState"]/option/text()').extract()
        
        #print('viewstate\n',viewstate)
        #print('viewstategen\n',viewstategen)
        #print('eventvalidation\n',eventvalidation)

        #print('chosenYr\n',chosenYr)
        print('state Codes\n',stateCodes[27],'\n',type(stateCodes[27]))
        print('state Names\n',stateNames[27],'\n',type(stateNames[27]))

        scriptManagers = ['ctl00$upPnl|ctl00$ContentPlaceHolder$ddState','ctl00$upPnl|ctl00$ContentPlaceHolder$dddistrict','ctl00$upPnl|ctl00$ContentPlaceHolder$ddblock']
        eventTargets = ['ctl00$ContentPlaceHolder$ddfinyear', 'ctl00$ContentPlaceHolder$ddState', 'ctl00$ContentPlaceHolder$dddistrict', 'ctl00$ContentPlaceHolder$ddblock']
        year = ['2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19']
        
        # change form params
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'ctl00$ScriptManager1': scriptManagers[0],
                '__EVENTTARGET' : eventTargets[1],
                '__EVENTARGUMENT' : '',
                '__VIEWSTATE' : viewstate1,
                '__VIEWSTATEGENERATOR' : viewstategen1,
                '__EVENTVALIDATION' : eventvalidation1,
                'ctl00$ddLanguage': '',
#                 'ctl00$ContentPlaceHolder$ddfinyear': year[9],
                'ctl00$ContentPlaceHolder$ddState': stateCodes[27],
#                 'ctl00$ContentPlaceHolder$dddistrict': '-1',
#                 'ctl00$ContentPlaceHolder$ddblock': '-1',
#                 'ctl00$ContentPlaceHolder$ddCat': 'All',
                '__ASYNCPOST': 'true'
                },
            callback=self.homeTohabListState
        )
    
    
    def homeTohabListState(self,response):
        open_in_browser(response)
#         # save html
#         filename = "habDropDownTelangana.html"
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         stateNames = response.xpath('//*[@id="ctl00_ContentPlaceHolder_ddState"]/option/text()').extract()
#         districtNames = response.xpath('//*[@id="ctl00_ContentPlaceHolder_dddistrict"]/option/text()').extract()
#         print('list of states\n',stateNames)
#         print('list of districts\n',districtNames)    



#     def check_login(self,response):
#         # check login success before going on
#         if b"authentication failed" in response.body:
#             self.logger.error("Login failed")
#             return
#         else:
#             self.logger.error("Login success")
#             open_in_browser(response)
#             return        
#         # continue scraping within authenticated session