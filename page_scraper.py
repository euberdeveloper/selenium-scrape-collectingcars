from bs4 import BeautifulSoup
import re
import time

def extract_between(text, start_pattern, end_marker):
    pattern = re.compile(start_pattern + '(.*?)' + re.escape(end_marker), re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def extract_with_multiple_markers(content, markers, end_marker):
    for start_marker in markers:
        extracted_content = extract_between(content, start_marker, end_marker)
        if extracted_content not in ["Not found", ""]:
            return extracted_content
    return "Not found"

def extract_image_urls_from_gallery(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Extract src attribute from each tag, applying multiple filters
    img_urls = [
        img['src'].split('?w=')[0] for img in img_tags
        if 'src' in img.attrs
           and not img['src'].startswith('data:image/svg+xml;base64')
           and 'placeholder' not in img['src']
           and 'assets/img' not in img['src']
    ]

    # Concatenate URLs into a single string
    return ';'.join(img_urls) if img_urls else "Not found"

def scrape_vehicle_data(driver):
    page_source = driver.page_source
    if not page_source:
        print(f"No page source available for URL")
        return None
    
    icon_lot_value = extract_between(page_source, '<li class="capitaliseWords"><span class="overviewList__icon"><img src="/assets/img/icon-lot.svg"></span>',
                                     '</li>')
    canonical_link = extract_between(page_source,'<link xmlns:php=\"http://php.net/xsl\" rel=\"canonical\" href=\"','\">')
    main_photo = extract_between(page_source, '<meta property=\"og:image\" itemprop=\"image\" content=\"', '\"')
    carfax_vin = extract_between(page_source, '<div class=\"carfax-snapshot-embedded carfax-panel\" data-vin=\"','\"')
    image_urls = extract_image_urls_from_gallery(page_source)
    current_bid = extract_between(page_source, '<div class=\"listing__statPrice\">','</div>')
    bid_label = extract_between(page_source, '<div class=\"listing__statBids\">', '</div>')

    fine_asta_status = extract_with_multiple_markers(page_source, ['data-auction-stage-end=\"',
                                                                    '<div class=\"listing__statLabel\">'],
                                       '\" data-auction-auction-end=')
    SaleStatus = extract_between(page_source, '<div class=\"listing__statLabel\">', '</div>')
    title = extract_between(page_source, '<div class=\"detailsPage__title\"><h1>', '</h1>')
    description = extract_between(page_source, '<section data-language=\"en\" class=\"description\">','</section>')
    country_seller = extract_between(page_source, '<span class=\"overviewList__icon overviewList__icon--flag">',
                                     '</li>')

    km = extract_between(page_source, '<img src=\"/assets/img/icon-mileage.svg\"></span>','</li>')
    transmission = extract_between(page_source, '<img src=\"/assets/img/icon-transmission.svg\"></span>', '</li>')
    driveside = extract_between(page_source, '<img src=\"/assets/img/icon-direction.svg\"></span>', '</li>')
    est_color = extract_between(page_source, '<img src=\"/assets/img/icon-paint.svg\"></span>', '</li>')
    int_color = extract_between(page_source, '<img src=\"/assets/img/icon-interior.svg\"></span>', '</li>')
    cilindrata = extract_between(page_source, '<img src=\"/assets/img/icon-engine.svg\"></span>', '</li>')
    lot_n = extract_between(page_source, '<img src=\"/assets/img/icon-lot.svg\"></span>Lot #', '</li>')
    seller_type = extract_between(page_source, '<img src=\"/assets/img/icon-private-sale.svg\"></span>', '</li>')
    seller_country = extract_between(page_source, '<span class=\"overviewList__icon overviewList__icon--flag\">',
                                     '</li>')
    seller_name = extract_between(page_source, '<span class="vendor-nickname">', '</li>')
    currency = extract_between(page_source, '<li class="capitaliseWords">Currency:', '</li>')
    first_registration = extract_between(page_source, '<li class="capitaliseWords">Date of First Registration:', '</li>')

    # Apply replacements
    description = description.replace("&nbsp;", " ")
    description = description.replace('<div class="description__content"><p></p><p><strong>', " ")
    description = description.replace('</li><li>', " ")
    description = description.replace('</strong> </p><ul><li>', ": ")
    description = description.replace('</p><p><strong>', " ")
    description = description.replace('</strong> </p><p>', ": ")
    description = description.replace('</li></ul><p><strong>', " ")
    description = description.replace('</strong> </p><p></p></div>', ".")
    description = description.replace('</strong>  </p><ul><li>', ": ")
    description = description.replace('</strong>  </p><p>', ": ")
    description = description.replace('</strong> <strong> </strong>', " ")
    description = description.replace('  ', " ")
    description = description.replace('  ', " ")
    description = description.replace('\\x{202F}', " ")
    description = re.sub(r' +', r' ', description)
    description = description.replace('</strong>  </p><ul><li>', ": ")
    description = description.replace('</strong>  </p><p>', ": ")
    icon_lot_value = icon_lot_value.replace('Lot #', "")
    main_photo = main_photo.replace('&amp;', "&")
    country_seller = re.sub(r'.*</span>', r'', country_seller)
    fine_asta_status = re.sub(r' (\d+):(\d+):(\d+)', r'', fine_asta_status)
    description = re.sub(r'</strong><span style="color: (.*?);">', r'', description)
    description = re.sub(r'</span></p><p><strong style="color: (.*?)">', r' ', description)
    description = re.sub(r'</strong> </p><iframe class="ql-video"(.*)', r'', description)
    description = re.sub(r'<.*?>', r'', description)
    description = re.sub(r' +', r' ', description)
    description = re.sub(r'^ ', r'', description)
    description = re.sub(r'Bidders should note that for (.*)', r'', description)
    description = re.sub(r' +$', r'', description)

    seller_type = re.sub(r'\&nbsp;Sale', r'', seller_type)
    seller_country = re.sub(r'.*</span>', r'', seller_country)
    seller_name = re.sub(r'.*</span>', r'', seller_name)

    return {
        'Maison': "CollectingCar",
        'Event_ref': "N/A",
        'PageUrl': canonical_link,
        'PhotoUrl': main_photo,
        'Lotto': lot_n,
        'Title': title,
        'Targa': first_registration,
        'Chassis': carfax_vin,
        'Engine': "N/A",
        'Body': "N/A",
        'RearFrame': "N/A",
        'Crankcase': "N/A",
        'RiferAuction': "N/A",
        'km': km,
        'cilindrata': cilindrata,
        'TipoCambio': transmission,
        'ColorEst': est_color,
        'ColorInt': int_color,
        'TipoCarrozz': "N/A",
        'val_min': "N/A",
        'val_max': "N/A",
        'Price': current_bid,
        'PriceStatus': SaleStatus,
        'PriceReserve': "N/A",
        'BidStart': "N/A",
        'BidEnd': fine_asta_status,
        'Subtitle': "N/A",
        'Year': "N/A",
        'Brand': "N/A",
        'Model': "N/A",
        'ModelType': "N/A",
        'Cilindri': "N/A",
        'Eng_Tecnico': "N/A",
        'Eng_Note': "N/A",
        'Eng_Veicolo': description,
        'GalleryPhoto': image_urls,
        'Bids': bid_label,
        'current_bid_value': "N/A",
        'CountrySeller': country_seller,
        'seller_type': seller_type,
        'seller_country': seller_country,
        'seller_name': seller_name,
        'driveside': driveside,
        'currency': currency,
    }

def scrape_page(driver, index: int):
    global scraped_results
    scraped_data = scrape_vehicle_data(driver)  
    print(f"[{index}] Scraped data")  
    return scraped_data

def scrape_url(driver, url: str, index: int):
    print(f"[{index}] Going to page and waiting 5 secs")
    driver.get(url)
    time.sleep(10)
    print(f"[{index}] Scraping page")
    scraped_data = scrape_page(driver, index)
    print(f"[{index}] Done")
    return scraped_data