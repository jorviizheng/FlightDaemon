# coding=utf-8

'''
import os
import sys
current_path = os.getcwd()
base_path = os.path.abspath(os.path.join(current_path, "../../"))
sys.path.append(base_path)
'''
 

from Spider import Spider
import lxml.html.soupparser 
import json
from tools import LogUtil
import traceback 


class Qunar(Spider):
    
    def __init__(self, config):
        Spider.__init__(self, config)
        
    
    def parseRealtimeInfo(self, flight):
        doc = lxml.html.soupparser.fromstring(self.content)
        content = doc.xpath("//div[@class='search_result']/dl[@class='state_detail']//span[@class='sd_2']/b/text()")
             
        estimate_time = content[1].split('-')
        if len(estimate_time) == 2:
            if estimate_time[0].strip() != "":
                flight['estimate_takeoff_time'] = estimate_time[0].strip()
            if estimate_time[1].strip() != "":
                flight['estimate_arrival_time'] = estimate_time[1].strip()
        
        flight['flight_state'] = u"计划航班"
        actual_time = content[2].split('-')
        if len(actual_time) == 2:
            if actual_time[0].strip() != "":
                flight['actual_takeoff_time'] = actual_time[0].strip()
                flight['flight_state'] = u"已经起飞"
            if actual_time[1].strip() != "":
                flight['actual_arrival_time'] = actual_time[1].strip()
                flight['flight_state'] = u"已经到达"
                flight['full_info'] = 1
            
       
    def getFlightRealTimeInfo(self, flight):
        try:
            self.url = "http://flight.qunar.com/schedule/fquery.jsp?flightCode=%s&d=%s&a=%s" % (flight['flight_no'], flight['takeoff_airport'], flight['arrival_airport'])
            if self.fetch() == 0:
                self.parseRealtimeInfo(flight)
            else:
                return None
            
            return 0
        except:
            msg = traceback.format_exc()
            self.logger.error(msg)
            
            return None
                   
    
    '''            
    def parseFixInfo(self, takeoff_city, arrival_city):
        doc = lxml.html.soupparser.fromstring(self.content)
        rows = doc.xpath("//div[@class='result_content']/ul/li")
        self.ret_val = []
        mileage = doc.xpath("//div[@class='search_result']/p/em/text()")[0]
        for row in rows:
            flight_info = {}
            
            flight_info['flight_no'] = row.xpath("span[@class='c1']/span[@class='title']/b/a/text()")[0]
            flight_info['company'] = flight_info['flight_no'][:2]
            flight_info['schedule_takeoff_time'] = row.xpath("span[@class='c2']/text()")[0]
            flight_info['schedule_arrival_time'] = row.xpath("span[@class='c2']/em/text()")[0]
            flight_info['takeoff_city'] = takeoff_city
            flight_info['arrival_city'] = arrival_city
            
            temp_text = row.xpath("span[@class='c3']/text()")[0]
            find_index = temp_text.find('T')
            if find_index != -1:
                flight_info['takeoff_airport'] = temp_text[:find_index]
                flight_info['takeoff_airport_building'] = temp_text[find_index:]
            else:
                flight_info['takeoff_airport'] = temp_text
                flight_info['takeoff_airport_building'] = ""
                
            temp_text = row.xpath("span[@class='c3']/text()")[1]
            find_index = temp_text.find('T')
            if find_index != -1:
                flight_info['arrival_airport'] = temp_text[:find_index]
                flight_info['arrival_airport_building'] = temp_text[find_index:]
            else:
                flight_info['arrival_airport'] = temp_text
                flight_info['arrival_airport_building'] = ""
                
            flight_info['plane_model'] = row.xpath("span[@class='c1']/span[@class='title']/text()")[1]
            flight_info['mileage'] = mileage
            flight_info['stopover'] = row.xpath("span[@class='c6']/text()")[0]
            flight_info['schedule'] = json.dumps(row.xpath("span[@class='c5']/span[@class='circular_blue']/text()"))
            
            href = row.xpath("span[@class='c1']/span[@class='title']/b/a/@href")[0]
            flight_info['takeoff_airport_short'] = href[href.find("&d=") + 3 : href.find("&d=") + 6]
            flight_info['arrival_airport_short'] = href[href.find("&a=") + 3 : href.find("&a=") + 6]
            
            #print flight_info['takeoff_airport_short']
            #print flight_info['arrival_airport_short']
            
            self.ret_val.append(flight_info)

    
    def getFlightFixInfoByAirline(self, takeoff_city, arrival_city):
        self.url = "http://flight.qunar.com/schedule/fsearch_list.jsp?departure=%s&arrival=%s" % (takeoff_city, arrival_city)
        #self.content = open("fsearch_list.jsp.html")
        self.logger.info("fetch %s" % (self.url))
        self.fetch()
        self.parseFixInfo(takeoff_city, arrival_city)
    

    def parseAirline(self):
        doc = lxml.html.soupparser.fromstring(self.content)
        airlines = doc.xpath("//ul[@class='apl_citylist fix']/li")
        
        self.ret_val = []
        for airline in airlines:
            self.ret_val.append(airline.text_content().strip())
        

    def getAirline(self, city):
        self.url = "http://flight.qunar.com/schedule/alph_order.jsp?city=%s" % (city)
        self.fetch()
        self.parseAirline()
        
        return self.ret_val
    
    
    
        
        return self.ret_val
    '''
    
    
if __name__ == '__main__':     
    q = Qunar(None)
    
    flights = q.getFlightRealTimeInfo('ZH8091', 'KMG', 'CTU', '2011-10-21')
    print len(flights)
    for flight in flights:
        print flight
    

    