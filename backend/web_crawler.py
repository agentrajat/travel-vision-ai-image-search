from selenium import webdriver
from selenium.webdriver.common.by import By

import time

class CustomWebCrawler:
    def __init__(
            self,
            base_url="<<website_url>>", 
            group_limit=20,
            photos_per_group=100,
            photo_limit=None
        ):
        self.driver = webdriver.Firefox()
        self.base_url = base_url
        self.group_limit = group_limit
        self.photos_per_group = photos_per_group
        self.photo_limit = photo_limit

        self.groups = []
        self.scrap_count = 0
        self.label_set = set()

    def close(self):
        self.driver.close()

    def load_page(self, url):
        self.driver.get(url)
        
        self.driver.implicitly_wait(3)

        # Handle cookie consent
        defaultpreferencemanager = self.driver.find_elements(By.CLASS_NAME, "truste_popframe")
        if len(defaultpreferencemanager) > 0:
            print("Found defaultpreferencemanager")
            self.driver.switch_to.frame(defaultpreferencemanager[0])
            reject_btn = self.driver.find_element(By.CLASS_NAME, "rejectAll")
            reject_btn.click()

            self.driver.implicitly_wait(3)
            close_btn = self.driver.find_element(By.CLASS_NAME, "close")
            close_btn.click()
            self.driver.implicitly_wait(1)
            self.driver.switch_to.default_content()
        
        # Scroll to bottom of page
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Not required as next page links are visible

    def scrap_groups(self, keyword):
        self.load_page(self.base_url + "/search/groups/?text=" + keyword)

        anchors = self.driver.find_elements(By.TAG_NAME, "a")
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if href is None:
                continue

            if href.endswith("/pool"):
                self.groups.append(href)

                if self.group_limit is not None and len(self.groups) >= self.group_limit:
                    break
    

    def scrap_photos(self, group_link):

        page_link = group_link
        page = 1
        photo_count = 0

        while (page_link is not None):
            print(f"Searching photos in {group_link} - Page {page}")
            
            title = None

            self.load_page(page_link)

            # Find group title
            title_container = self.driver.find_elements(By.CLASS_NAME, "title-container")
            if len(title_container) > 0:
                # Text content of a tag inside title-container
                title = title_container[0].find_element(By.TAG_NAME, "a").text


            # Find Photos
            # Find divs with class photo-list-photo-container
            containers = self.driver.find_elements(By.CLASS_NAME, "photo-list-photo-container")
            print(f"Found {len(containers)} photos")

            for container in containers:

                img = container.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src")

                a_tags = container.find_elements(By.TAG_NAME, "a")
                for a_tag in a_tags:
                    role = a_tag.get_attribute("role")
                    if role == "heading":
                        aria_label = a_tag.get_attribute("aria-label")
                        if aria_label in self.label_set:
                            print(f"Skipping duplicate photo: {aria_label}")
                            continue

                        href = a_tag.get_attribute("href")

                        photo_count += 1
                        self.scrap_count += 1

                        self.label_set.add(aria_label)
                        # print(f"Total count: {self.scrap_count} - Group Count: {photo_count}")

                        yield {
                            "group": title,
                            "page": page,
                            "label": aria_label,
                            "link": href,
                            "image_src": src,
                            "scrap_time": time.time()
                        }

                        if self.photo_limit is not None and self.scrap_count >= self.photo_limit:
                            print("Total photo limit reached")
                            return
                        
                        if self.photos_per_group is not None and photo_count >= self.photos_per_group:
                            print("Group photo limit reached")
                            return

                        break

            print(f"Total count: {self.scrap_count} - Group Count: {photo_count}")
            # Find next page link
            # view pagination-view class
            pagination = self.driver.find_elements(By.CLASS_NAME, "pagination-view")
            page_link = None

            if len(pagination) > 0:
                print("Found pagination")
                anchors = pagination[0].find_elements(By.TAG_NAME, "a")
                for anchor in anchors:
                    rel = anchor.get_attribute("rel")
                    if rel == "next":
                        page_link = anchor.get_attribute("href")
                        page += 1
                        print(f"Next page link: {page_link}")
                        break
                    
        print("Scrapped all photos in this group or reached limit")


    def crawl(self, keyword):
        """
        Crawl groups for photos with the given keyword
        """

        self.scrap_groups(keyword)
        print(f"Found {len(self.groups)} groups")

        for group_link in self.groups:
            try:
                for photo in self.scrap_photos(group_link):
                    yield photo
            except:
                print(f"Error scrapping {group_link} - Skipping")

            if self.photo_limit is not None and self.scrap_count >= self.photo_limit:
                print("Total photo limit reached - Stopping scrapping")
                break
        
        print(f"Scrapped {self.scrap_count} photos")


# if __name__ == "__main__":

#     scrapper = CustomWebCrawler(photo_limit=40, photos_per_group=20)
#     for photo in scrapper.crawl("world"):
#         print(photo)
#     scrapper.close()