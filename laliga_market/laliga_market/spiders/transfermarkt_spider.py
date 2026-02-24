import scrapy

class TransfermarktSpider(scrapy.Spider):
    name = "transfermarkt"
    
    custom_settings = {
            'ROBOTSTXT_OBEY': False,
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'DOWNLOAD_DELAY': 2,
        }
 
    start_urls = ["https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/plus/?saison_id=2023"]

   
    def parse(self, response):
        self.logger.info("Iniciando extracción de datos de la tabla de clubes...")
        
        filas = response.css('#yw1 table.items tbody tr')
        
        for fila in filas:

            celdas = fila.css('td')
            

            nombre = fila.css('td.hauptlink.no-border-links a::text').get()
            

            valor_total_raw = fila.css('td.rechts a::text').get()

       
            if nombre and valor_total_raw:
              
                squad = celdas[2].css('a::text').get() or celdas[2].css('::text').get()
                

                edad = celdas[3].css('::text').get()

      
                yield self.limpiar_datos(nombre, valor_total_raw, squad, edad)


    def limpiar_datos(self, nombre, valor, squad, edad):
        
        equipo = nombre.strip()
        
        v = valor.replace('€', '').strip()
        if 'bn' in v:
            v_num = float(v.replace('bn', '')) * 1000
        elif 'm' in v:
            v_num = float(v.replace('m', ''))
        else:
            v_num = 0.0


        return {
            'team': equipo,
            'valor_total_m': v_num,
            'plantilla': int(squad.strip()) if squad else 0,
            'edad_media': float(edad.strip()) if edad else 0.0
        } 