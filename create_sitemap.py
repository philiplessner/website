import xml.etree.ElementTree as ET

def create_sitemap(urls, sitemap_filename="sitemap.xml"):
    """
    Creates an XML sitemap file with provided URLs. 
    
    Args:
        urls (list): List of URLs to include in the sitemap. 
        sitemap_filename (str, optional): Name of the output XML file. Defaults to "sitemap.xml".
    """
    
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url in urls:
        url_element = ET.SubElement(root, "url")
        ET.SubElement(url_element, "loc").text = url
        # Optionally add other elements like lastmod, changefreq, priority
        # ET.SubElement(url_element, "lastmod").text = "2023-12-12" 
        # ET.SubElement(url_element, "changefreq").text = "daily"
        # ET.SubElement(url_element, "priority").text = "0.8" 
    
    tree = ET.ElementTree(root)
    tree.write(sitemap_filename, encoding="utf-8", xml_declaration=True) 

    
if __name__ == "__main__":
    urls = ["https://www.philiplessner.com/", 
            "https://www.philiplessner.com/blog",
            "https://www.philiplessner.com/aboutme",]
    create_sitemap(urls, sitemap_filename="./app/static/sitemap.xml")