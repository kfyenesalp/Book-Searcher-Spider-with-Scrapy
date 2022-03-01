import scrapy
import time

all_list = []
value_list = []
class QuotesSpider(scrapy.Spider):
    name = "findbook"
    def start_requests(self):
        book_name = str(input("Kitap Adı Giriniz:")) 
        drAndIdefix = book_name.replace(" ", "%20")
        drAndIdefix = drAndIdefix.replace("'", "%27")
        bkm = book_name.replace(" ", "+")
        bkm = bkm.replace("'","%27")
        kitap_sec = bkm.lower()
        kitap_sec = bkm.replace("ö","%D6")
        kitap_sec = bkm.replace("ü","%FC")
        kitap_sec = bkm.replace("ı","%FD")
        kitap_sec = bkm.replace("ğ","%F0")
        urls = [
            'https://www.dr.com.tr/search?q={}&redirect=search'.format(drAndIdefix),
            'https://www.idefix.com/Search?q={}&redirect=search'.format(drAndIdefix),
            "https://www.kitapsec.com/Arama/index.php?a={}".format(kitap_sec),
            "https://www.kitapci.com.tr/arama?q={}".format(bkm),
            "https://www.aperatifkitap.com/ara/?search_performed=Y&q={}".format(bkm),
            "https://www.kitaplarsepette.com/Arama?1&kelime={}".format(drAndIdefix),
        ]
        for url in urls:
            if "www.dr.com.tr" in url:
                yield scrapy.Request(url=url, callback=self.DRparse)
            elif "www.idefix.com" in url:
                yield scrapy.Request(url=url, callback=self.IdefixParse)  
            elif "www.kitapsec.com" in url:
                yield scrapy.Request(url = url,callback = self.KitapSecParse)
            elif "www.kitapci.com" in url:
                yield scrapy.Request(url = url, callback = self.KitapciParse)
            elif "www.aperatifkitap.com" in url:
                yield scrapy.Request(url = url, callback = self.AperatifParse)
            elif "www.kitaplarsepette.com" in url:
                yield scrapy.Request(url = url, callback = self.SepetParse)    

    def DRparse(self, response):
        try:
            book_names = response.css("div.prd-content-wrapper a::text").extract()
            book_values = response.css("div.prd-price::text").extract()
            book_links = response.css("div.prd-content-wrapper a::attr(href)").extract()
            if book_names and book_values is not None:
                n = 0
                v = 0
                for book in range(3):
                    book_names[n] = book_names[n].replace("\n","")
                    book_values[v] = book_values[v].replace("\n","")
                    book_values[v] = book_values[v].replace(" ","")
                    book_values[v] = book_values[v].replace("TL","")
                    all_list.append("D&R\nKitap Adı : {}".format(book_names[n]))
                    all_list.append("Link : https://www.dr.com.tr{}".format(book_links[n]))
                    all_list.append(book_values[v])
                    value_list.append(book_values[v])  
                    n += 3
                    v += 1
        except:
            None          

    def IdefixParse(self,response):
        for i in range(1,4):
                try:
                    idefix_book_name = response.xpath("//*[@id='facetProducts']/div[{}]/div/div/div[1]/div/div[3]/a/text()".format(i)).extract()
                    idefix_book_value = response.xpath("/html/body/div[1]/div[1]/div/main/div[3]/div[1]/div[{}]/div/div/div[1]/div/div[7]/span/text()".format(i)).extract()
                    idefix_book_link = response.xpath("/html/body/div[1]/div[1]/div/main/div[3]/div[1]/div[{}]/div/div/div[1]/div/div[3]/a".format(i)).attrib['href']     
                    idefix_book_value[0] = idefix_book_value[0].replace("TL","")
                    idefix_book_value[0] = idefix_book_value[0].replace(" ","")
                    all_list.append("İdefix\nKitap Adı : {}".format(idefix_book_name[0]))
                    all_list.append("Link : https://www.idefix.com{}".format(idefix_book_link))
                    all_list.append(idefix_book_value[0])
                    value_list.append(idefix_book_value[0])
                except:
                    break
                   
   
    def KitapSecParse(self,response):
        book_name = response.css("div.Ks_UrunSatir a span::text").extract()
        book_value = response.css("div.Ks_UrunSatir span.fiyat font::text").extract()
        book_link = response.css("div.Ks_UrunSatir a::attr(href)").extract()
        n = 1
        v = 1
        l = 3
        if book_name and book_value and book_link is not None:
            for book in range(3):
                try:
                    book_value[v] = book_value[v].replace("TL","")
                    book_value[v] = book_value[v].replace(" ","")        
                    all_list.append("Kitap Seç\nKitap Adı : {}".format(book_name[n]))
                    all_list.append("Link : {}".format(book_link[l]))
                    all_list.append(book_value[v])
                    value_list.append(book_value[v])
                    n += 3
                    v += 2
                    l += 6
                except:
                    break        
                

    def KitapciParse(self,response):
        for i in range(1,4):
            try:
                book_name = response.xpath("/html/body/div[3]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div[{}]/div/div/div[2]/div/a/text()".format(i)).extract()
                book_value = response.xpath("/html/body/div[3]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div[{}]/div/div/div[2]/div/div/div/div/div/div[2]/div/text()".format(i)).extract()
                book_link = response.xpath("/html/body/div[3]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div[{}]/div/div/div[2]/div/a".format(i)).attrib['href']  
                if book_name and book_value and book_link is not None:
                    book_name[0] = book_name[0].replace("\n","")
                    book_value[0] = book_value[0].replace("\n","")
                    book_value[0] = book_value[0].replace("TL","")
                    all_list.append("Kitapçı.com\nKitap Adı : {}".format(book_name[0]))
                    all_list.append("Link : https://www.kitapci.com.tr{}".format(book_link))
                    all_list.append(book_value[0])
                    value_list.append(book_value[0]) 
            except:
                break        

    def AperatifParse(self,response):
        for i in range(1,4):
            try:
                book_name = response.xpath("//*[@id='products_search_pagination_contents']/div[{}]/div/form/div/div[3]/a/text()".format(i)).extract()
                book_value = response.xpath("//*[@id='products_search_pagination_contents']/div[{}]/div/form/div/div[4]/div[1]/div[2]/span/span/text()".format(i)).extract()
                book_link = response.xpath("/html/body/div/div[4]/div[3]/div/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div[{}]/div/form/div/div[1]/a".format(i)).attrib['href']
                if book_name and book_value and book_link is not None:
                    book_value[0] = book_value[0].replace(" ", "")
                    book_value[0] = book_value[0].replace("TL","")
                    all_list.append("Aperatif Kitap\nKitap Adı : {}".format(book_name[0]))
                    all_list.append("Link : https://www.aperatifkitap.com{}".format(book_link))
                    all_list.append(book_value[0])
                    value_list.append(book_value[0])
            except:
                break        

    def SepetParse(self,response):
        for i in range(1,4):
            try:
                book_name = response.xpath("//*[@id='ProductPageProductList']/div[{}]/div/div[2]/div[2]/a/text()".format(i)).extract()
                book_value = response.xpath("//*[@id='ProductPageProductList']/div[{}]/div/div[2]/div[5]/div[1]/span/text()".format(i)).extract()
                book_link = response.css("div.productName.detailUrl a::attr(href)").extract()
                book_value[0] = book_value[0].replace("\n","")
                book_value[0] = book_value[0].replace("₺","")
                book_value[0] = book_value[0].replace(" ","")
                if book_name and book_value and book_link is not None:  
                    all_list.append("Kitaplar Sepette \nKitap Adı : {}".format(book_name[0]))
                    all_list.append("Link : https://www.kitaplarsepette.com{}".format(book_link[i-1]))
                    all_list.append(book_value[0]) 
                    value_list.append(book_value[0])
            except:
                break
        time.sleep(7)
        file = open("Books.txt","w",encoding="UTF-8")
        value_list.sort()
        writtens_list = []
        for i in range(len(value_list)):
            for k in range(len(all_list)):
                if value_list[i] == all_list[k] and str(value_list[i]) != "0,00" and all_list[k-2] not in writtens_list:
                    file.write("************************************\n")
                    file.write("{}\n".format(all_list[k-2]))
                    file.write("Fiyat : {} TL\n".format(value_list[i]))
                    file.write("{}\n".format(all_list[k-1]))
                    file.write("************************************\n")
                    writtens_list.append(all_list[k-2])           
        

        

              
           