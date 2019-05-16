import scrapy
from mlbpbp.items import MlbpbpItem
 

class MlbSpider(scrapy.Spider):
    name = "baila"
    
    def start_requests(self):
        homeurl = [
            'http://www.espn.com/mlb/team/_/name/nyy/new-york-yankees'

        ]
        awayurl = ['http://www.espn.com/mlb/team/_/name/mil/milwaukee-brewers']
        for url in homeurl:
        	yield scrapy.Request(url=url, callback=self.homeparse)

        for url in awayurl:
        	yield scrapy.Request(url=url, callback = self.awayparse)

    def homeparse(self, response):
    	links = response.xpath('//@href').extract()
    	for item in links:
    		if 'splits' in item:
    			splitslink = item

    	splitslink = 'http://www.espn.com' + splitslink
    	# print(splitslink)
    	# print('yolo')
    	url = splitslink
    	x = response.css('div.game-meta > div ::text').extract()
    	y = response.css('div.game-info ::text').extract()
    	y = y[1:]
    	# print(x)
    	# print(y)
    	# print(len(y))
    	# print(len(x))
    	h = len(x)
    	gameresults = []
    	for i in range(h):
    		if x[i] == 'W' or x[i] == 'L':
    			gameresult = [x[i], x[i+1]]
    			gameresults.append(gameresult)

    	# print(gameresults)
    	# print(len(gameresults))
    	fullgames = []
    	for i in range(len(gameresults)):
    		if 'vs' not in y[i]:
    			fullgame = ['A', gameresults[i]]

    		if 'vs' in y[i]:
    			fullgame = ['H', gameresults[i]]

    		fullgames.append(fullgame)
    	homegames = []
    	awaygames = []
    	for i in range(len(fullgames)):
    		if fullgames[i][0] == 'H':
    			homegames.append(fullgames[i])

    		if fullgames[i][0] == 'A':
    			awaygames.append(fullgames[i])

    	# print(fullgames)
    	# print(len(homegames))
    	# print(len(awaygames))
    	l10wins = 0
 
    	l10winper = 0
    	l6hwins = 0
    	l6hwinper = 0
    	l6awins = 0
    	l6awinper = 0
    	l10scored = 0
    	l10allowed = 0
    	l6hscored = 0
    	l6hallowed = 0
    	l6ascored = 0
    	l6aallowed = 0
    	for i in range(10):
    		if fullgames[i][1][0] == 'W':
    			l10wins +=1
    			x = fullgames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[0])
    			runsallowed = int(y[1])
    			l10allowed += runsallowed
    			l10scored += runscored

    		if fullgames[i][1][0] == 'L':
    			x = fullgames[i][1][1]
    			y = x.split('-')

    			
    			runscored = int(y[1])
    			runsallowed = int(y[0])
    			l10scored +=runscored
    			l10allowed += runsallowed

    	l10runpergame = l10scored/10
    	l10allowedper = l10allowed/10
    	l10winper = l10wins/10

    	for i in range(6):
    		if homegames[i][1][0] == 'W':
    			l6hwins +=1
    			x = homegames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[0])
    			runsallowed = int(y[1])
    			l6hscored += runscored
    			l6hallowed += runsallowed

    		if homegames[i][1][0] == 'L':
    			x = homegames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[1])
    			runsallowed = int(y[0])
    			l6hscored += runscored
    			l6hallowed += runsallowed
    	l6hwinper = l6hwins/6
    	l6hrunper = l6hscored/6
    	l6hallowedper = l6hallowed/6

    	for i in range(6):
    		if awaygames[i][1][0] == 'W':
    			l6awins +=1
    			x = awaygames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[0])
    			runsallowed = int(y[1])
    			l6ascored += runscored
    			l6aallowed += runsallowed

    		if awaygames[i][1][0] == 'L':
    			x = awaygames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[1])
    			runsallowed = int(y[0])
    			l6ascored += runscored
    			l6aallowed += runsallowed
    	l6awinper = l6awins/6
    	l6arunper = l6ascored/6
    	l6aallowedper = l6aallowed/6



    	homeitem = MlbpbpItem()

    	#print(l8awinper)
    
    	print(l6hwinper)
    	print('above is the home teams last 8 at home win %')
    	print(l10winper)
    	print('above is the home teams last 10 games win %')
    	print(l10runpergame)
    	print('above is the home teams last 10 runs per game')
    	print(l10allowedper)
    	print('above is the home teams last 10 allowed per game')
    	print(l6hrunper)
    	print('above is the home teams runs per game in their last 8 home games')
    	print(l6hallowedper)
    	print('above is the home teams runs allowed per game in their last 8 home games')
    	# print(l6arunper)
    	# print(l6aallowedper)
    	homeitem['hlast10rec'] = l10winper
    	homeitem['hlast6hrec'] = l6hwinper
    	homeitem['hlast10rpg'] = l10runpergame
    	homeitem['hlast10rapg'] = l10allowedper
    	homeitem['hlast6hrpg'] = l6hrunper
    	homeitem['hlast6hrapg'] = l6hallowedper

    	request = scrapy.Request(url=url, callback=self.homesplits)
    	request.meta['item'] = homeitem
    	yield request




    def homesplits(self, response):
    	x = response.css('tr.Table2__tr.Table2__tr--sm.Table2__even ::text').extract()
    	# print(x)

    	totalgames = int(x[49])
    	totalwins = int(x[50])
    	averagerpg = int(x[53])/totalgames
    	homegames = int(x[63])
    	homewins = int(x[64])
    	averagehrpg = int(x[67])/homegames
    	awaygames = int(x[77])
    	awaywins = int(x[78])
    	averagearpg = int(x[81])/ awaygames
    	totalwinper = totalwins/totalgames
    	homewinper = homewins/homegames
    	awaywinper = awaywins/awaygames
    	print(averagerpg)
    	print('above is the home teams runs per game whole season')
    	print(averagehrpg)
    	print('above is the ohme teams run per game for all their home teams')
    	print(totalwinper)
    	print('above is the home teams winning percentage on the season')
    	print(homewinper)
    	print('above is the home teams winning percentage at home on the season')
    	
    	homeitem = response.meta['item']
    	homeitem ['hgenrpg'] = averagerpg
    	homeitem['hgenhrpg'] = averagehrpg
    	homeitem ['hgenrec'] = totalwinper
    	homeitem['hgenhrec'] = homewinper

    	links = response.xpath('//@href').extract()
    	for link in links:
    		if 'pitching' in link:
    			newlink = link

    	pitchinglink = 'http://www.espn.com' + newlink
    	request = scrapy.Request(url=pitchinglink, callback=self.homepitching)
    	request.meta['item'] = homeitem
    	yield request

    def homepitching(self, response):
    	x = response.css('tr.Table2__tr.Table2__tr--sm.Table2__even ::text').extract()
    	totalera = float(x[45])
    	homera = float(x[59])
    	awayera = float(x[73])
    	print(totalera)
    	print('above is the home teams average runs allowed on the year')
    	print(homera)
    	print('above is the home teams era at home on the year')
    	newitem = response.meta['item']
    	newitem ['hgenera'] = totalera
    	newitem['hgenhera'] = homera
    	

    	return newitem
    def awayparse(self, response):
    	links = response.xpath('//@href').extract()
    	for item in links:
    		if 'splits' in item:
    			splitslink = item

    	splitslink = 'http://www.espn.com' + splitslink
    	# print(splitslink)
    	# print('yolo')
    	url = splitslink
    	x = response.css('div.game-meta > div ::text').extract()
    	y = response.css('div.game-info ::text').extract()
    	y = y[1:]
    	# print(x)
    	# print(y)
    	# print(len(y))
    	# print(len(x))
    	h = len(x)
    	gameresults = []
    	for i in range(h):
    		if x[i] == 'W' or x[i] == 'L':
    			gameresult = [x[i], x[i+1]]
    			gameresults.append(gameresult)

    	# print(gameresults)
    	# print(len(gameresults))
    	fullgames = []
    	for i in range(len(gameresults)):
    		if 'vs' not in y[i]:
    			fullgame = ['A', gameresults[i]]

    		if 'vs' in y[i]:
    			fullgame = ['H', gameresults[i]]

    		fullgames.append(fullgame)
    	homegames = []
    	awaygames = []
    	for i in range(len(fullgames)):
    		if fullgames[i][0] == 'H':
    			homegames.append(fullgames[i])

    		if fullgames[i][0] == 'A':
    			awaygames.append(fullgames[i])

    	# print(fullgames)
    	# print(len(homegames))
    	# print(len(awaygames))
    	l10wins = 0
 
    	l10winper = 0
    	l6hwins = 0
    	l6hwinper = 0
    	l6awins = 0
    	l6awinper = 0
    	l10scored = 0
    	l10allowed = 0
    	l6hscored = 0
    	l6hallowed = 0
    	l6ascored = 0
    	l6aallowed = 0
    	for i in range(10):
    		if fullgames[i][1][0] == 'W':
    			l10wins +=1
    			x = fullgames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[0])
    			runsallowed = int(y[1])
    			l10allowed += runsallowed
    			l10scored += runscored

    		if fullgames[i][1][0] == 'L':
    			x = fullgames[i][1][1]
    			y = x.split('-')

    			
    			runscored = int(y[1])
    			runsallowed = int(y[0])
    			l10scored +=runscored
    			l10allowed += runsallowed

    	l10runpergame = l10scored/10
    	l10allowedper = l10allowed/10
    	l10winper = l10wins/10

    	for i in range(6):
    		if homegames[i][1][0] == 'W':
    			l6hwins +=1
    			x = homegames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[0])
    			runsallowed = int(y[1])
    			l6hscored += runscored
    			l6hallowed += runsallowed

    		if homegames[i][1][0] == 'L':
    			x = homegames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[1])
    			runsallowed = int(y[0])
    			l6hscored += runscored
    			l6hallowed += runsallowed
    	l6hwinper = l6hwins/6
    	l6hrunper = l6hscored/6
    	l6hallowedper = l6hallowed/6

    	for i in range(6):
    		if awaygames[i][1][0] == 'W':
    			l6awins +=1
    			x = awaygames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[0])
    			runsallowed = int(y[1])
    			l6ascored += runscored
    			l6aallowed += runsallowed

    		if awaygames[i][1][0] == 'L':
    			x = awaygames[i][1][1]
    			y = x.split('-')
    			runscored = int(y[1])
    			runsallowed = int(y[0])
    			l6ascored += runscored
    			l6aallowed += runsallowed
    	l6awinper = l6awins/6
    	l6arunper = l6ascored/6
    	l6aallowedper = l6aallowed/6






    	print(l6awinper)
    	print('above is the away teams last 6 winning percentage on the road')
    	# print(l8hwinper)
    	print(l10winper)
    	print('above is the away teams winning percentage in their last 10 games')
    	print(l10runpergame)
    	print('above is the away teams average runs per game in their last 10')
    	print(l10allowedper)
    	print('above is the away teams average runs allowed in their last 10 games')
    	#print(l8hrunper)
    	# print(l8hallowedper)

    	print(l6arunper)
    	print('above is the away teams average runs per game in their last 6 away')
    	print(l6aallowedper)
    	print('above is the away teams average runs allowed in their last 6')
    	# for url in urls:
    	# 	yield scrapy.Request(url=url, callback=self.awaysplits)
    	awayitem = MlbpbpItem()
    	awayitem['alast10rec'] = l10winper
    	awayitem['alast6arec'] = l6awinper
    	awayitem['alast10rpg'] = l10runpergame
    	awayitem['alast10rapg'] = l10allowedper
    	awayitem['alast6arpg'] = l6arunper
    	awayitem['alast6arapg'] = l6aallowedper

    	request = scrapy.Request(url=url, callback=self.awaysplits)
    	request.meta['item'] = awayitem
    	yield request

    def awaysplits(self, response):
    	x = response.css('tr.Table2__tr.Table2__tr--sm.Table2__even ::text').extract()
    	# print(x)

    	totalgames = int(x[49])
    	totalwins = int(x[50])
    	averagerpg = int(x[53])/totalgames
    	homegames = int(x[63])
    	homewins = int(x[64])
    	averagehrpg = int(x[67])/homegames
    	awaygames = int(x[77])
    	awaywins = int(x[78])
    	averagearpg = int(x[81])/ awaygames
    	totalwinper = totalwins/totalgames
    	homewinper = homewins/homegames
    	awaywinper = awaywins/awaygames
    	print(averagerpg)
    	print('above is the away teams average runs per game on the year')

    	print(averagearpg)
    	print('above is the away teams run per game for all their away games')
    	print(totalwinper)
    	print('above is the away teams winning percentage on the season')
    	print(awaywinper)
    	print('above is the away teams winning percentage on the raod on the season')

    	links = response.xpath('//@href').extract()
    	for link in links:
    		if 'pitching' in link:
    			newlink = link

    	away = response.meta['item']
    	away ['agenrpg'] = averagerpg
    	away['agenarpg'] = averagearpg
    	away ['agenrec'] = totalwinper
    	away['agenarec'] = awaywinper
    	pitchinglink = 'http://www.espn.com' + newlink
    	request = scrapy.Request(url=pitchinglink, callback=self.awaypitching)
    	request.meta['item'] = away
    	yield request

    def awaypitching(self, response):
    	x = response.css('tr.Table2__tr.Table2__tr--sm.Table2__even ::text').extract()
    	totalera = float(x[45])
    	homera = float(x[59])
    	awayera = float(x[73])
    	print(totalera)
    	print('above is the away teams era on the year')
    	print(awayera)
    	print('above is the away teams era on the road on the year')


    	newitem = response.meta['item']
    	newitem ['agenera'] = totalera
    	newitem['agenaera'] = awayera
    	

    	return newitem

    	

