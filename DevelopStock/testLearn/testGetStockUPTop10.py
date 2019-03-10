
       # stockHsUp ="http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_up%s"
        # content =self.urlOpenContent(stockHsUp,'1')

        # soup = BeautifulSoup(content,features="lxml")
        # print(soup.p.text)
        # retContent = soup.p.text
        # retContent =retContent.replace('symbol','"symbol"')
        # retContent =retContent.replace('code','"code"')
        # retContent =retContent.replace('name','"name"')
        # retContent =retContent.replace('trade','"trade"')
        # retContent =retContent.replace('pricechange','"pricechange"')
        # retContent =retContent.replace('changepercent','"AA"')#?
        # retContent =retContent.replace('buy','"buy"')
        # retContent =retContent.replace('sell','"sell"')
        # retContent =retContent.replace('settlement','"settlement"')
        # retContent =retContent.replace('open','"open"')
        # retContent =retContent.replace('high','"high"')
        # retContent =retContent.replace('low','"low"')
        # retContent =retContent.replace('volume','"volume"')
        # retContent =retContent.replace('amount','"amount"')
        # retContent =retContent.replace('ticktime','"ticktime"')
        # retContent =retContent.replace('per','"per"')#
        # retContent =retContent.replace('pb','"pb"')
        # retContent =retContent.replace('mktcap','"mktcap"')
        # retContent =retContent.replace('nmc','"nmc"')
        # retContent =retContent.replace('turnoverratio','"turnoverratio"')
        # retContent =retContent.replace('"AA"','"changepercent"')
        # text = json.loads(retContent)
        # pd.DataFrame(text)
        # print(text)   