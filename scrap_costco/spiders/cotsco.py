from scrapy.spiders import SitemapSpider
from sbk_scraping.parser.factories import ParserFactory
from sbk_scraping.utils import load_config_file
import scrapy
#  from scrapy.crawler import CrawlerProcess
from scrap_costco.utils import get_logger


logger = get_logger(__name__)


class DeptosSpider(scrapy.Spider):
    name = 'deptos'
    start_urls = ['https://www.costco.com.mx']

    def __init__(self, *args, **kwargs):
        super(DeptosSpider, self).__init__(*args, **kwargs)

        self.factory = ParserFactory.build_from_config(
            load_config_file('parsers.yaml')
        )

        self.parser = self.factory.build_parser(
            parser_id='departments'
        )

    def parse(self, response):
        deptos_dict = self.parser.parse(data=response.text)
        deptos_list = deptos_dict["deptos"]
        departments_clean = []

        for depto in deptos_list:
            no_url = "javascript:void(0)"
            if (str(depto) != no_url):
                departments_clean.append(depto)
                print(depto)
        print(len(departments_clean))
        #  print(departments_clean)


class DeptosMapSpider(SitemapSpider):
    name = 'map_depto'
    sitemap_urls = ['https://www.costco.com.mx/robots.txt']
    sitemap_rules = [
        ('/Joyeria-y-Relojes/Aretes/Aretes-de-Perlas', 'department'),
        ('/Joyeria-y-Relojes/Aretes', 'department_landing')
    ]
    url_list = []
    url_list_2 = []
    sitemap_follow = ['/sitemap_mexico_category',
                      '/sitemap_mexico_categorylanding']

    def department(self, response):
        self.url_list.append(response.url)
        logger.info('LA URL DEL DEPTO ES: ', response.url)
        print(len(self.url_list))

    def department_landing(self, response):
        self.url_list_2.append(response.url)
        logger.info('URL LANDING DEPTO: ', response.url)
        print(len(self.url_list_2))


class UrlsProductSpider(SitemapSpider):
    name = 'url_depto'
    sitemap_urls = ['https://www.costco.com.mx/robots.txt']
    sitemap_rules = [
        ('/Joyeria-y-Relojes/Aretes/Aretes-de-Perlas/', 'urls_products')
    ]
    sitemap_follow = ['/sitemap_mexico_product']
    url_list = []

    def urls_products(self, response):
        self.url_list.append(response.url)
        logger.info('LA URL DEL PRODUCTO ES: ', response.url)
        print(len(self.url_list))


class ProductInfoSpider(SitemapSpider):
    name = 'products'
    sitemap_urls = ['https://www.costco.com.mx/robots.txt']
    sitemap_rules = [
        ('/Joyeria-y-Relojes/Anillos/Anillos-de-Oro/', 'products_info'),
    ]
    sitemap_follow = ['/sitemap_mexico_product']

    def __init__(self, *args, **kwargs):
        super(ProductInfoSpider, self).__init__(*args, **kwargs)

        self.factory = ParserFactory.build_from_config(
            load_config_file('parsers.yaml')
        )

        self.parser = self.factory.build_parser(
            parser_id='costco_products'
        )

    def products_info(self, response):
        products_list = []
        product = self.parser.parse(data=response.text)
        products_list.append(product)
        print(product)
        print(len(products_list))


# ·········································································

#  deptos
#  map_depto
#  products
#  url_depto

#  process = CrawlerProcess()
#  process.crawl(UrlsProductSpider)
#  process.crawl(DeptosSpider)
#  process.crawl(ProductInfoSpider)
#  process.start


#  class CotscoSpider(SitemapSpider):
    #  name = 'cotsco'
    #  sitemap_urls = ['https://www.costco.com.mx/robots.txt']
    #  sitemap_rules = [
        #  ('/Joyeria-y-Relojes/Anillos/Anillos-de-Oro/', 'products_info'),
    #  ]
    #  sitemap_follow = ['/sitemap_mexico_product']
#
    #  products_list = []
    #  factory = ParserFactory.build_from_config(load_config_file('parsers.yaml'))
#
    #  def products_info(self, response):
        #  parser = self.factory.build_parser(
            #  data=response.text, parser_id="costco_products")
#
        #  product = parser.parse()
        #  self.products_list.append(product)
        #  print(product)
        #  print(len(self.products_list))
        #  print('FROM SPIDER 1')
#


#  from dataclasses import dataclass
#  import scrapy
#  from scrapy.http import Response


#  class MasterSpider(scrapy.Spider):
    #  name_list = []
    #  price_list = []
    #  code_list = []
    #  offert_list = []
#
    #  factory = ParserFactory.build_from_config(load_config_file('parsers.yaml'))
#
    #  srchex_name = factory.get_srchex(parser_id='First', target_id='product_name')
    #  srchex_price = factory.get_srchex(parser_id='First', target_id='product_price')
    #  srchex_code = factory.get_srchex(parser_id='First', target_id='product_code')
    #  srchex_offprice = factory.get_srchex(parser_id='First', target_id='price_offert')
#
    #  def definition(self, response):
        #  product_name = response.xpath(srchex_name).extract()
        #  product_price = response.xpath(srchex_price).extract()
        #  product_code = response.xpath(srchex_code).extract()
        #  offert_price = response.xpath(srchex_offprice).extract()
#
#
#  class DeptoSpider(SitemapSpider):
    #  name = 'depto'
    #  sitemap_urls = ['https://www.costco.com.mx/robots.txt']
    #  sitemap_rules = [
        #  ('/Joyeria-y-Relojes/Aretes/Aretes-de-Perlas/', 'products_info_2')
    #  ]
    #  sitemap_follow = ['/sitemap_mexico_product']
#
    #  products_list_2 = []
    #  factory = ParserFactory.build_from_config(load_config_file('parsers.yaml'))
#
    #  def products_info_2(self, response):
        #  parser = self.factory.build_parser(data=response.text, parser_id="First")
        #  product = parser.parse()
        #  self.products_list_2.append(product)
        #  print(product)
        #  print(len(self.products_list_2))
        #  print('FROM SPIDER 2')


#  class DeptoSpider(SitemapSpider):
    #  name = 'depto'
    #  sitemap_urls = ['https://www.costco.com.mx/robots.txt']
    #  sitemap_rules = [
        #  ('/Joyeria-y-Relojes/Anillos/Anillos-de-Piedras-Semipreciosas/', 'products')
    #  ]
    #  sitemap_follow = ['/sitemap_mexico_product']
#
    #  def products(self, response):
        #  print('FROM SPIDER 2')
        #  MasterSpider.name_list.append(MasterSpider.definition.product_name)
        #  MasterSpider.price_list.append(MasterSpider.definition.product_price)
        #  MasterSpider.code_list.append(MasterSpider.definition.product_code)
        #  MasterSpider.offert_list.append(MasterSpider.definition.offert_price)
#
        #  print(len(MasterSpider.name_list))



    #  def parse(self, response):
        #  for link in self.products:
            #  self.names_list.append(name)
            #  print(link)
        #  print(name)
        #  print(self.names_list)

    #  factory = ParserFactory.build_from_config(
        #  load_config_file('parsers.yaml'))

    #  parser = factory.build_parser(data=response.text, parser_id="First")


        #  yield{
            #  'Name': response.xpath('.//*[@class="product-name"]/text()').get(),
            #  'Product price': response.xpath('.//*[@class="product-price-amount"]//span/text()').get(),
            #  'Product code': response.xpath('.//*[@class="product-code"]//span/text()').get(),
            #  'Price in offer':  response.xpath('.//*[@class="you-pay-value"]/text()').get()
        #  }




        #  parser = self.factory.build_parser(data=response.text, parser_id="First")
        #  dic = parser.parse
        #  yield {dic}

        #  ('/Joyeria-y-Relojes/Anillos/Anillos-de-Oro/', 'product_price'),
        #  ('/Joyeria-y-Relojes/Anillos/Anillos-de-Oro/', 'product_code'),
        #  ('/Joyeria-y-Relojes/Anillos/Anillos-de-Oro/', 'offert_price')
    

    #  def product_price(self, response):
        #  yield{
            #  'Product price': response.xpath(
                #  './/*[@class="product-price-amount"]//span/text()'
            #  ).get()
        #  }
#
    #  def product_code(self, response):
        #  yield{
            #  'Product code': response.xpath(
                #  './/*[@class="product-code"]//span/text()').get()
        #  }
#
    #  def offert_price(self, response):
        #  yield{
            #  'Price in offer':  response.xpath(
                #  './/*[@class="you-pay-value"]/text()').get()
        #  }

#
#
                    #  'https://www.costco.com.mx/sitemap.xml',
                    #  'https://www.costco.com.mx/sitemap_mexico_product.xml'



#  import scrapy
#  from scrapy.http import Request
#  from sbk_scraping.parser.factories import ParserFactory
#  from sbk_scraping.utils import load_config_file
#
#
#  class CotscoSpider(scrapy.Spider):
    #  name = 'cotsco'
    #  allowed_domains = ['costco.com.mx']
    #  start_urls = ['http://costco.com.mx/']
#
    #  def parse(self, response):
        #  departamentos = []
        #  departamentos_all = response.xpath(
            #  './/*[@class="topmenu"]/ul/li/a[text()]/@href').extract()
        #  for depto in departamentos_all:
            #  no_url = "javascript:void(0)"
            #  if (str(depto) != no_url):
                #  departamentos.append(depto)
#
        #  print('Numero de departamentos: ', len(departamentos))
#
        #  for departamento in departamentos:
            #  absolute_url = response.urljoin(departamento)
            #  yield Request(absolute_url, callback=self.parse_product)
#


    #  def parse_product(self,response):
#
        #  nombre_producto = response.xpath('.//*[@class="product-name"]/text()').extract_first()
        #  precio_producto = response.xpath('.//*[@class="product-price-amount"]//span/text()').extract_first()
        #  codigo_producto = response.xpath('.//*[@class="product-code"]//span/text()').extract_first()

        #  yield {'nombre_producto': nombre_producto,
               #  'precio_producto': precio_producto,
               #  'codigo_producto': codigo_producto}
#
        #  factory = ParserFactory.build_from_config(
            #  load_config_file('parsers.yaml'))
        #  srchex = factory.get_srchex(parser_id='First', target_id='deptos')
        #  response.body.decode(response.encoding)
        #  body = response.text
        #  parser = factory.build_parser(data=body, parser_id="First")
        #  departamentos_all = response.xpath(srchex).extract()
        #  print(departamentos_all)
