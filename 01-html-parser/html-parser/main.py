import requests
from bs4 import BeautifulSoup
import json


class WebsiteToJson:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.data = {}

    def fetch_page(self):
        """Fetch the webpage content."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, "html.parser")
        else:
            raise Exception(
                f"Failed to fetch page. HTTP status code: {response.status_code}"
            )

    def extract_data(self):
        """Extract data dynamically."""
        # Extract key information dynamically based on the website's structure

        # Product Title
        product_name = self.soup.find("h1", class_="heading-5 v-fw-regular").get_text(
            strip=True
        )

        # Product Description
        product_description_tag = self.soup.find("div", {"id": "product-description"})
        product_description = (
            product_description_tag.get_text(strip=True)
            if product_description_tag
            else "No description found"
        )

        # Images
        image_tags = self.soup.find_all("img", {"data-src": True})
        images = [img["data-src"] for img in image_tags]

        # Price
        price = self.extract_price()

        # Ratings
        rating_tag = self.soup.find("span", class_="ugc-average-rating")
        rating = float(rating_tag.get_text()) if rating_tag else 0.0

        # Reviews Count
        reviews_tag = self.soup.find("span", class_="ugc-review-count")
        total_reviews = int(reviews_tag.get_text().split()[0]) if reviews_tag else 0

        # Categories
        categories = [
            {"name": category.get_text(strip=True), "url": category.get("href", "#")}
            for category in self.soup.select(".breadcrumb li a")
        ]

        # Specifications (optional parsing logic)
        specs = self.extract_specifications()

        # Populate JSON structure
        self.data = {
            "success": True,
            "url": self.url,
            "result_count": 1,
            "detail": {
                "name": product_name,
                "brand": self.extract_brand(),
                "url": self.url,
                "images": images,
                "price": price,
                "list_price": None,  # Assume to be dynamically retrievable
                "currency": "USD",  # Hardcoded; modify for dynamic extraction
                "currency_symbol": "$",
                "product_id": self.extract_product_id(),
                "rating": rating,
                "total_reviews": total_reviews,
                "in_stock": True,  # Default value or dynamic based on availability
                "categories": categories,
                "variants": [],  # Dynamic variants (implement), if applicable
                "included_items": ["Product included in packaging"],  # Example data
                "product_features": self.extract_product_features(),
                "is_energy_star_certified": True,  # Example field; modify as necessary
                "model_no": "NS-DH35WH1",  # Example data
                "specifications": specs,
            },
            "remaining_credits": 756886,  # Example static field; modify to match your source
        }

    def extract_price(self):
        """Extract price from the page."""
        try:
            price_tag = self.soup.find("div", class_="priceView-customer-price")
            price = price_tag.find("span").get_text().replace("$", "").strip()
            return float(price)
        except AttributeError:
            return None

    def extract_brand(self):
        """Extract brand dynamically."""
        try:
            brand_tag = self.soup.find(text="Brand").find_next().get_text(strip=True)
            return brand_tag
        except AttributeError:
            return "Unknown"

    def extract_specifications(self):
        """Parse the specifications table."""
        specifications = []
        spec_rows = self.soup.select("table.specifications tr")
        for row in spec_rows:
            columns = row.find_all("td")
            if len(columns) == 2:
                specifications.append(
                    {
                        "type": None,
                        "name": columns[0].get_text(strip=True),
                        "value": columns[1].get_text(strip=True),
                    }
                )
        return specifications

    def extract_product_id(self):
        """Extract product ID."""
        try:
            product_id_tag = self.soup.find("div", {"data-sku-id": True})
            return product_id_tag["data-sku-id"]
        except TypeError:
            return None

    def extract_product_features(self):
        """Extract product features."""
        features_tag = self.soup.find("div", class_="feature-list")
        features = []
        if features_tag:
            feature_items = features_tag.find_all("li")
            for item in feature_items:
                feature_name = item.get_text(strip=True)
                features.append({"name": feature_name, "value": None})
        return features

    def to_json(self):
        """Convert the parsed data to JSON."""
        return json.dumps(self.data, indent=4, ensure_ascii=False)

    def save_json(self, filename="output.json"):
        """Save the JSON data to a file."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.to_json())

    def scrape_and_convert(self):
        """Orchestrator method to scrape and save JSON."""
        self.fetch_page()
        self.extract_data()
        self.save_json()
        print(f"JSON saved to 'output.json'.")


# Usage:
if __name__ == "__main__":
    url = "https://www.bestbuy.com/site/product/6385840.p"  # Example URL (change to dynamic)
    scraper = WebsiteToJson(url)
    scraper.scrape_and_convert()
