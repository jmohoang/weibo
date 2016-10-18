import csv
import xlsxwriter

def UnicodeDictReader (utf8_data):
        csv_reader = csv.DictReader(utf8_data)
        for row in csv_reader:
                try:
                        yield {key: unicode(value, 'utf-8') for key, value, in row.iteritems()}
                except UnicodeDecodeError:
                        pass
                
"""Yields weibo blogs"""
def reader():         
        with open("week1.csv") as fp:
                reader = UnicodeDictReader(fp)
                count = 0
                for row in reader:
                        yield(row)
                        
                        """count += 1
                        #print(row["created_at"].split()[1].split(":")) 
                        print(row)
                        if count >= 1:
                                break"""
                        
        """                
        with open("week2.csv") as fp:
                        reader = UnicodeDictReader(fp)
                        count = 0
                        for row in reader:
                                yield(row)  """       
                        
#reader()

"""Yields messages that are retwets """
def remessage():
        for msg in reader():
                if msg["retweeted_uid"] != '':
                        yield msg
                        
"""Calculates the count of retweets. """  
"""From this function, when we put the count to it we ficgure out that we have 
week1 -> 182053
week1 + week2 -> 467 725"""
def count (): 
        count = 0 
        for msg in remessage():
                if len(msg["retweeted_uid"]) >1:
                        count += 1
        print count
#count()

"""Calculates how many retweets a blog has"""
def retweetFreq():
        textDict = {}
        for msg in remessage():
                if msg["text"] in textDict.keys(): 
                        textDict[msg["text"]] = textDict[msg["text"]] + 1
                else:
                        textDict[msg["text"]] = 1
        print (len(textDict))
        return textDict 
        
#retweetFreq()

"""Frequency of retweets VS hour"""
def plotRetweetVsHour (): 
        three, six, nine, twelve, fifteen, eighteen, twentyone, twentyfour = (0,0,0,0,0,0,0,0)
        
        for message in remessage():
                hour = int(message["created_at"].split()[1].split(":")[0])
                if hour < 3: 
                        three += 1
                elif (hour >= 3 and hour < 6): 
                        six += 1
                elif (hour >= 6 and hour < 9) : 
                        nine += 1
                elif (hour >= 9 and hour < 12) : 
                        twelve += 1 
                elif (hour >= 12 and hour < 15) : 
                        fifteen += 1
                elif (hour >= 15 and hour < 18) : 
                        eighteen += 1
                elif (hour >= 18 and hour < 21) : 
                        twentyone += 1
                else: 
                        twentyfour += 1 
                
        #Writing the information in an excel file. 
        workbook = xlsxwriter.Workbook('plotRetweetVsHour.xls')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Hour")
        worksheet.write (0, 1, "Frequencies")
        
        worksheet.write (1, 0, "Three")
        worksheet.write (1, 1, three)
        worksheet.write (2, 0, "Six")
        worksheet.write (2, 1, six)
        worksheet.write (3, 0, "Nine")
        worksheet.write (3, 1, nine)
        worksheet.write (4, 0, "Twelve")
        worksheet.write (4, 1, twelve)
        worksheet.write (5, 0, "Fifteen")
        worksheet.write (5, 1, fifteen)
        worksheet.write (6, 0, "Eighteen")
        worksheet.write (6, 1, eighteen)
        worksheet.write (7, 0, "Twent-yone")
        worksheet.write (7, 1, twentyone)
        worksheet.write (8, 0, "Twenty-four")
        worksheet.write (8, 1, twentyfour)        
        
        workbook.close()
        
        #Test of whether the function gets all the data. 
        total = 0
        total += (three + six + nine + twelve + fifteen + eighteen + twentyone + twentyfour)
        #print total 
        
#plotRetweetVsHour ()
                

"""This function measures the importance of when the original time of the tweet 
to the number of retweets
Counts how many time a retweet is rewteeted. """  
def daytime (): 
        textDict = {} # dictionary { : []}
        count = 0 
        for msg in remessage():
                count += 1 
                if count <= 100000: 
                        if msg["retweeted_status_mid"] in textDict:
                                textInfo = textDict[msg["retweeted_status_mid"]]
                                textInfo[2] += 1
                                textDict[msg["retweeted_status_mid"]] = textInfo
                        else:
                                textInfo = []
                                textInfo.append(msg["retweeted_uid"])
                                hour = msg["created_at"].split()[1].split(":")[0]
                                textInfo.append(hour)
                                textInfo.append(1)
                                textDict[msg["retweeted_status_mid"]] = textInfo
                else: 
                        return textDict
                        
        return textDict
#daytime()


        