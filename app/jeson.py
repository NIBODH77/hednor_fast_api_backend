# # # # # # # # # # import json
# # # # # # # # # # import random
# # # # # # # # # # from typing import List, Dict
# # # # # # # # # # from pathlib import Path

# # # # # # # # # # # Configuration
# # # # # # # # # # INPUT_FILE = Path(r"C:\Users\PRABODH AWASTHI\Documents\biilpaymentfastapi\hednor_fastapi\app\tree_output.txt")
# # # # # # # # # # OUTPUT_FILE = Path(r"C:\Users\PRABODH AWASTHI\Documents\biilpaymentfastapi\hednor_fastapi\app\dummy_products.json")

# # # # # # # # # # class CategoryParser:
# # # # # # # # # #     def __init__(self, file_path: Path):
# # # # # # # # # #         self.file_path = file_path
# # # # # # # # # #         self.categories = []
        
# # # # # # # # # #     def parse_categories(self) -> List[str]:
# # # # # # # # # #         """Parse the tree structure text file to extract all category paths"""
# # # # # # # # # #         with open(self.file_path, 'r', encoding='utf-8') as f:
# # # # # # # # # #             lines = f.readlines()
        
# # # # # # # # # #         categories = []
# # # # # # # # # #         current_path = []
        
# # # # # # # # # #         for line in lines:
# # # # # # # # # #             line = line.strip()
# # # # # # # # # #             if not line:
# # # # # # # # # #                 continue
                
# # # # # # # # # #             # Determine depth by counting leading spaces/tabs
# # # # # # # # # #             depth = len(line) - len(line.lstrip())
# # # # # # # # # #             indent = depth // 4  # Assuming 4 spaces per level
            
# # # # # # # # # #             # Update current path based on depth
# # # # # # # # # #             current_path = current_path[:indent]
# # # # # # # # # #             category_name = line.strip()
# # # # # # # # # #             current_path.append(category_name)
            
# # # # # # # # # #             # Add full path to categories
# # # # # # # # # #             categories.append(" > ".join(current_path))
        
# # # # # # # # # #         self.categories = categories
# # # # # # # # # #         return categories

# # # # # # # # # # class ProductGenerator:
# # # # # # # # # #     def __init__(self, categories: List[str]):
# # # # # # # # # #         self.categories = categories
# # # # # # # # # #         self.brands = ["Nike", "Adidas", "Sony", "Samsung", "Apple", "Dell", "HP", "Lenovo"]
# # # # # # # # # #         self.colors = ["Red", "Blue", "Black", "White", "Silver", "Gold"]
# # # # # # # # # #         self.adjectives = ["Premium", "Pro", "Lite", "Max", "Ultra", "Smart"]
        
# # # # # # # # # #     def generate_product(self, product_id: int) -> Dict:
# # # # # # # # # #         """Generate a single product with random attributes"""
# # # # # # # # # #         category = random.choice(self.categories)
# # # # # # # # # #         last_category = category.split(" > ")[-1]
        
# # # # # # # # # #         return {
# # # # # # # # # #             "id": product_id,
# # # # # # # # # #             "name": self._generate_product_name(last_category),
# # # # # # # # # #             "category": category,
# # # # # # # # # #             "price": round(random.uniform(10, 1000), 2),
# # # # # # # # # #             "stock": random.randint(0, 100),
# # # # # # # # # #             "rating": round(random.uniform(1, 5), 1),
# # # # # # # # # #             "specs": self._generate_specs(),
# # # # # # # # # #             "description": self._generate_description(last_category),
# # # # # # # # # #             "images": self._generate_images()
# # # # # # # # # #         }
    
# # # # # # # # # #     def _generate_product_name(self, category: str) -> str:
# # # # # # # # # #         """Generate a product name based on category"""
# # # # # # # # # #         patterns = [
# # # # # # # # # #             f"{random.choice(self.brands)} {category} {random.choice(self.adjectives)}",
# # # # # # # # # #             f"{random.choice(self.adjectives)} {category} by {random.choice(self.brands)}",
# # # # # # # # # #             f"{random.choice(self.colors)} {category} {random.randint(100, 999)}"
# # # # # # # # # #         ]
# # # # # # # # # #         return random.choice(patterns)
    
# # # # # # # # # #     def _generate_specs(self) -> Dict:
# # # # # # # # # #         """Generate product specifications"""
# # # # # # # # # #         return {
# # # # # # # # # #             "color": random.choice(self.colors),
# # # # # # # # # #             "weight": f"{random.uniform(0.1, 5.0):.1f} kg",
# # # # # # # # # #             "dimensions": {
# # # # # # # # # #                 "length": random.randint(1, 50),
# # # # # # # # # #                 "width": random.randint(1, 30),
# # # # # # # # # #                 "height": random.randint(1, 20)
# # # # # # # # # #             },
# # # # # # # # # #             "warranty": f"{random.choice([1, 2, 3])} year(s)"
# # # # # # # # # #         }
    
# # # # # # # # # #     def _generate_description(self, category: str) -> str:
# # # # # # # # # #         """Generate product description"""
# # # # # # # # # #         descriptors = [
# # # # # # # # # #             f"High-quality {category} designed for professional use.",
# # # # # # # # # #             f"Premium {category} with advanced features.",
# # # # # # # # # #             f"Latest model {category} with improved performance.",
# # # # # # # # # #             f"Eco-friendly {category} made from sustainable materials."
# # # # # # # # # #         ]
# # # # # # # # # #         return random.choice(descriptors)
    
# # # # # # # # # #     def _generate_images(self) -> List[str]:
# # # # # # # # # #         """Generate dummy image URLs"""
# # # # # # # # # #         base_url = "https://example.com/images/products"
# # # # # # # # # #         return [
# # # # # # # # # #             f"{base_url}/img{random.randint(1, 100)}.jpg",
# # # # # # # # # #             f"{base_url}/img{random.randint(1, 100)}.jpg"
# # # # # # # # # #         ]
    
# # # # # # # # # #     def generate_products(self, count: int = 100) -> List[Dict]:
# # # # # # # # # #         """Generate multiple products"""
# # # # # # # # # #         return [self.generate_product(i+1) for i in range(count)]

# # # # # # # # # # def main():
# # # # # # # # # #     # Step 1: Parse the category tree
# # # # # # # # # #     print("Parsing category tree...")
# # # # # # # # # #     parser = CategoryParser(INPUT_FILE)
# # # # # # # # # #     categories = parser.parse_categories()
# # # # # # # # # #     print(f"Found {len(categories)} categories")
    
# # # # # # # # # #     # Step 2: Generate dummy products
# # # # # # # # # #     print("Generating dummy products...")
# # # # # # # # # #     generator = ProductGenerator(categories)
# # # # # # # # # #     products = generator.generate_products(100)
    
# # # # # # # # # #     # Step 3: Save to JSON
# # # # # # # # # #     output_data = {
# # # # # # # # # #         "metadata": {
# # # # # # # # # #             "generated_on": "2023-11-15",
# # # # # # # # # #             "total_products": len(products),
# # # # # # # # # #             "categories_used": len(set(p['category'] for p in products))
# # # # # # # # # #         },
# # # # # # # # # #         "products": products
# # # # # # # # # #     }
    
# # # # # # # # # #     with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
# # # # # # # # # #         json.dump(output_data, f, indent=2, ensure_ascii=False)
    
# # # # # # # # # #     print(f"Successfully generated {len(products)} products in {OUTPUT_FILE}")
    
# # # # # # # # # #     # Print sample
# # # # # # # # # #     print("\nSample product:")
# # # # # # # # # #     print(json.dumps(products[0], indent=2))

# # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # #     main()



# # # # # # # # # import json
# # # # # # # # # import os
# # # # # # # # # from pathlib import Path

# # # # # # # # # def split_json(input_file, products_output, categories_output):
# # # # # # # # #     """
# # # # # # # # #     Split the original JSON data into products and categories files
# # # # # # # # #     """
# # # # # # # # #     try:
# # # # # # # # #         # Convert paths to absolute paths
# # # # # # # # #         input_file = Path(input_file).absolute()
# # # # # # # # #         products_output = Path(products_output).absolute()
# # # # # # # # #         categories_output = Path(categories_output).absolute()
        
# # # # # # # # #         print(f"Looking for input file at: {input_file}")
        
# # # # # # # # #         if not input_file.exists():
# # # # # # # # #             raise FileNotFoundError(f"Input file not found at {input_file}")

# # # # # # # # #         with open(input_file, 'r', encoding='utf-8') as f:
# # # # # # # # #             data = json.load(f)

# # # # # # # # #         # Extract products and categories
# # # # # # # # #         products = data.get('products', [])
# # # # # # # # #         categories = list(set(p['category'] for p in products if 'category' in p))

# # # # # # # # #         # Save products
# # # # # # # # #         with open(products_output, 'w', encoding='utf-8') as f:
# # # # # # # # #             json.dump(products, f, indent=2, ensure_ascii=False)
# # # # # # # # #         print(f"Saved {len(products)} products to {products_output}")

# # # # # # # # #         # Save categories
# # # # # # # # #         with open(categories_output, 'w', encoding='utf-8') as f:
# # # # # # # # #             json.dump(categories, f, indent=2, ensure_ascii=False)
# # # # # # # # #         print(f"Saved {len(categories)} categories to {categories_output}")

# # # # # # # # #     except FileNotFoundError as e:
# # # # # # # # #         print(f"[ERROR] {str(e)}")
# # # # # # # # #         print("Please check the input file path and try again.")
# # # # # # # # #     except Exception as e:
# # # # # # # # #         print(f"[ERROR] An unexpected error occurred: {str(e)}")

# # # # # # # # # if __name__ == "__main__":
# # # # # # # # #     # Define file paths - adjust these to match your actual file locations
# # # # # # # # #     base_dir = Path(r"C:\Users\PRABODH AWASTHI\Documents\biilpaymentfastapi\hednor_fastapi\app")
    
# # # # # # # # #     input_json = base_dir / "tree_output.json"  # Changed from original_data.json
# # # # # # # # #     products_output = base_dir / "products.json"
# # # # # # # # #     categories_output = base_dir / "categories.json"
    
# # # # # # # # #     # Create the files if they don't exist
# # # # # # # # #     for file in [input_json, products_output, categories_output]:
# # # # # # # # #         file.parent.mkdir(parents=True, exist_ok=True)
# # # # # # # # #         file.touch(exist_ok=True)
    
# # # # # # # # #     split_json(input_json, products_output, categories_output)


# # # # # # # # import json
# # # # # # # # import random
# # # # # # # # from pathlib import Path
# # # # # # # # from typing import List, Dict

# # # # # # # # # Configuration
# # # # # # # # INPUT_FILE = Path(r"C:\Users\PRABODH AWASTHI\Documents\biilpaymentfastapi\hednor_fastapi\app\tree_output.txt")
# # # # # # # # OUTPUT_FILE = Path(r"C:\Users\PRABODH AWASTHI\Documents\biilpaymentfastapi\hednor_fastapi\app\dummy_products.json")

# # # # # # # # def read_tree_file(file_path: Path) -> List[str]:
# # # # # # # #     """Read and parse the tree structure text file"""
# # # # # # # #     try:
# # # # # # # #         with open(file_path, 'r', encoding='utf-8') as f:
# # # # # # # #             lines = [line.strip() for line in f.readlines() if line.strip()]
        
# # # # # # # #         if not lines:
# # # # # # # #             raise ValueError("File is empty")
            
# # # # # # # #         return lines
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"[ERROR] Failed to read input file: {str(e)}")
# # # # # # # #         return []

# # # # # # # # def parse_categories(lines: List[str]) -> List[str]:
# # # # # # # #     """Parse the tree structure to extract category paths"""
# # # # # # # #     categories = []
# # # # # # # #     current_path = []
    
# # # # # # # #     for line in lines:
# # # # # # # #         # Count leading spaces to determine depth
# # # # # # # #         depth = len(line) - len(line.lstrip())
# # # # # # # #         indent = depth // 4  # Assuming 4 spaces per level
        
# # # # # # # #         # Update current path based on depth
# # # # # # # #         current_path = current_path[:indent]
# # # # # # # #         category_name = line.strip()
# # # # # # # #         current_path.append(category_name)
        
# # # # # # # #         # Add full path to categories
# # # # # # # #         categories.append(" > ".join(current_path))
    
# # # # # # # #     return categories

# # # # # # # # def generate_dummy_products(categories: List[str], count: int = 100) -> List[Dict]:
# # # # # # # #     """Generate realistic dummy product data"""
# # # # # # # #     brands = ["Nike", "Adidas", "Sony", "Samsung", "Apple", "Dell"]
# # # # # # # #     colors = ["Red", "Blue", "Black", "White", "Silver"]
# # # # # # # #     adjectives = ["Pro", "Max", "Lite", "Premium", "Smart"]
    
# # # # # # # #     products = []
# # # # # # # #     for i in range(count):
# # # # # # # #         category = random.choice(categories)
# # # # # # # #         last_part = category.split(" > ")[-1]
        
# # # # # # # #         product = {
# # # # # # # #             "id": i + 1,
# # # # # # # #             "name": f"{random.choice(brands)} {last_part} {random.choice(adjectives)}",
# # # # # # # #             "category": category,
# # # # # # # #             "price": round(random.uniform(10, 1000), 2),
# # # # # # # #             "stock": random.randint(0, 100),
# # # # # # # #             "rating": round(random.uniform(1, 5), 1),
# # # # # # # #             "specs": {
# # # # # # # #                 "color": random.choice(colors),
# # # # # # # #                 "weight": f"{random.uniform(0.1, 5.0):.1f} kg",
# # # # # # # #                 "warranty": f"{random.choice([1, 2, 3])} year(s)"
# # # # # # # #             }
# # # # # # # #         }
# # # # # # # #         products.append(product)
    
# # # # # # # #     return products

# # # # # # # # def main():
# # # # # # # #     print(f"Reading input file: {INPUT_FILE}")
    
# # # # # # # #     # Step 1: Read and parse the input file
# # # # # # # #     lines = read_tree_file(INPUT_FILE)
# # # # # # # #     if not lines:
# # # # # # # #         print("No valid data found in input file")
# # # # # # # #         return
    
# # # # # # # #     # Step 2: Extract categories
# # # # # # # #     categories = parse_categories(lines)
# # # # # # # #     print(f"Found {len(categories)} categories")
    
# # # # # # # #     # Step 3: Generate dummy products
# # # # # # # #     products = generate_dummy_products(categories)
# # # # # # # #     print(f"Generated {len(products)} dummy products")
    
# # # # # # # #     # Step 4: Save to JSON
# # # # # # # #     output_data = {
# # # # # # # #         "metadata": {
# # # # # # # #             "source": INPUT_FILE.name,
# # # # # # # #             "generated_on": "2023-11-15",
# # # # # # # #             "total_products": len(products),
# # # # # # # #             "categories_used": len(set(p['category'] for p in products))
# # # # # # # #         },
# # # # # # # #         "products": products
# # # # # # # #     }
    
# # # # # # # #     try:
# # # # # # # #         with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
# # # # # # # #             json.dump(output_data, f, indent=2, ensure_ascii=False)
# # # # # # # #         print(f"Successfully saved to {OUTPUT_FILE}")
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"[ERROR] Failed to save output: {str(e)}")

# # # # # # # # if __name__ == "__main__":
# # # # # # # #     main()




# # # # # # # import json
# # # # # # # import uuid
# # # # # # # import random
# # # # # # # from datetime import datetime

# # # # # # # # === Categories ===
# # # # # # # categories = [
# # # # # # #     {"id": 1, "name": "Electronics", "level": 0, "is_leaf": False, "parent_id": None},
# # # # # # #     {"id": 2, "name": "Mobiles", "level": 1, "is_leaf": True, "parent_id": 1},
# # # # # # #     {"id": 3, "name": "Laptops", "level": 1, "is_leaf": True, "parent_id": 1},
# # # # # # #     {"id": 4, "name": "Fashion", "level": 0, "is_leaf": False, "parent_id": None},
# # # # # # #     {"id": 5, "name": "Men's Clothing", "level": 1, "is_leaf": True, "parent_id": 4},
# # # # # # #     {"id": 6, "name": "Women's Clothing", "level": 1, "is_leaf": True, "parent_id": 4},
# # # # # # #     {"id": 7, "name": "Home & Kitchen", "level": 0, "is_leaf": False, "parent_id": None},
# # # # # # #     {"id": 8, "name": "Appliances", "level": 1, "is_leaf": True, "parent_id": 7},
# # # # # # #     {"id": 9, "name": "Furniture", "level": 1, "is_leaf": True, "parent_id": 7},
# # # # # # # ]

# # # # # # # with open("categories.json", "w") as f:
# # # # # # #     json.dump(categories, f, indent=4)

# # # # # # # # === Products ===
# # # # # # # brands = ["Sony", "Samsung", "Apple", "Nike", "Levi's", "Whirlpool", "Dell", "HP", "LG"]
# # # # # # # sellers = ["Amazon", "Flipkart", "Reliance Digital", "Croma"]
# # # # # # # titles = ["Super", "Smart", "Premium", "Value", "Eco", "Ultra", "Max", "Pro"]
# # # # # # # descriptions = [
# # # # # # #     "High-quality product", "Best-in-class features", "Top-rated by users", "Budget-friendly option",
# # # # # # #     "Eco-friendly and efficient", "Durable and stylish"
# # # # # # # ]

# # # # # # # def generate_product(index, category_id):
# # # # # # #     return {
# # # # # # #         "product_id": str(uuid.uuid4()),
# # # # # # #         "name": f"Product-{index}",
# # # # # # #         "title": f"{random.choice(titles)} {random.choice(brands)} Item {index}",
# # # # # # #         "description": random.choice(descriptions),
# # # # # # #         "brand": random.choice(brands),
# # # # # # #         "price": round(random.uniform(100, 99999), 2),
# # # # # # #         "discount_price": round(random.uniform(50, 99998), 2),
# # # # # # #         "stock_quantity": random.randint(10, 1000),
# # # # # # #         "category_id": category_id,
# # # # # # #         "rating": round(random.uniform(1, 5), 1),
# # # # # # #         "reviews": random.randint(0, 500),
# # # # # # #         "in_stock": True,
# # # # # # #         "is_active": True,
# # # # # # #         "seller": random.choice(sellers),
# # # # # # #         "specs": json.dumps({
# # # # # # #             "feature1": "Value1",
# # # # # # #             "feature2": "Value2",
# # # # # # #             "feature3": f"Spec-{index}"
# # # # # # #         }),
# # # # # # #         "image_url": f"https://dummyimage.com/600x400/000/fff&text=Product+{index}",
# # # # # # #         "created_at": datetime.utcnow().isoformat()
# # # # # # #     }

# # # # # # # leaf_category_ids = [cat["id"] for cat in categories if cat["is_leaf"]]
# # # # # # # products = [generate_product(i, random.choice(leaf_category_ids)) for i in range(1, 81)]

# # # # # # # with open("products.json", "w") as f:
# # # # # # #     json.dump(products, f, indent=4)
# # # # # # from app.database import engine, Base


# # # # # # # Drop all tables
# # # # # # Base.metadata.drop_all(bind=engine)

# # # # # # # Recreate tables (optional)
# # # # # # # Base.metadata.create_all(bind=engine)


# # # # # import json

# # # # # categories = [
# # # # #     {"id": 1, "name": "Electronics", "level": 1, "is_leaf": False, "parent_id": None},
# # # # #     {"id": 2, "name": "Mobiles", "level": 2, "is_leaf": True, "parent_id": 1},
# # # # #     {"id": 3, "name": "Laptops", "level": 2, "is_leaf": True, "parent_id": 1},
# # # # #     {"id": 4, "name": "Fashion", "level": 1, "is_leaf": False, "parent_id": None},
# # # # #     {"id": 5, "name": "Men's Clothing", "level": 2, "is_leaf": True, "parent_id": 4},
# # # # #     {"id": 6, "name": "Women's Clothing", "level": 2, "is_leaf": True, "parent_id": 4},
# # # # #     {"id": 7, "name": "Home Appliances", "level": 1, "is_leaf": False, "parent_id": None},
# # # # #     {"id": 8, "name": "Kitchen", "level": 2, "is_leaf": True, "parent_id": 7}
# # # # # ]

# # # # # with open("categories.json", "w") as f:
# # # # #     json.dump(categories, f, indent=2)

# # # # # print("✅ categories.json generated.")

# # # # import json

# # # # category_brands = [
# # # #     {
# # # #         "category_id": 2,
# # # #         "category_name": "Mobiles",
# # # #         "brands": [
# # # #             {"brand_name": "Samsung"},
# # # #             {"brand_name": "Apple"},
# # # #             {"brand_name": "OnePlus"},
# # # #             {"brand_name": "Realme"},
# # # #             {"brand_name": "Motorola"}
# # # #         ]
# # # #     },
# # # #     {
# # # #         "category_id": 3,
# # # #         "category_name": "Laptops",
# # # #         "brands": [
# # # #             {"brand_name": "HP"},
# # # #             {"brand_name": "Dell"},
# # # #             {"brand_name": "Asus"},
# # # #             {"brand_name": "Lenovo"},
# # # #             {"brand_name": "Apple"}
# # # #         ]
# # # #     },
# # # #     {
# # # #         "category_id": 5,
# # # #         "category_name": "Men's Clothing",
# # # #         "brands": [
# # # #             {"brand_name": "Levi's"},
# # # #             {"brand_name": "Nike"},
# # # #             {"brand_name": "Adidas"},
# # # #             {"brand_name": "Puma"},
# # # #             {"brand_name": "HRX"}
# # # #         ]
# # # #     },
# # # #     {
# # # #         "category_id": 6,
# # # #         "category_name": "Women's Clothing",
# # # #         "brands": [
# # # #             {"brand_name": "Zara"},
# # # #             {"brand_name": "Only"},
# # # #             {"brand_name": "H&M"},
# # # #             {"brand_name": "Global Desi"},
# # # #             {"brand_name": "Biba"}
# # # #         ]
# # # #     },
# # # #     {
# # # #         "category_id": 8,
# # # #         "category_name": "Kitchen",
# # # #         "brands": [
# # # #             {"brand_name": "Prestige"},
# # # #             {"brand_name": "Butterfly"},
# # # #             {"brand_name": "Hawkins"},
# # # #             {"brand_name": "Pigeon"},
# # # #             {"brand_name": "Borosil"}
# # # #         ]
# # # #     }
# # # # ]

# # # # with open("category_brands.json", "w") as f:
# # # #     json.dump(category_brands, f, indent=2)

# # # # print("✅ category_brands.json generated.")









# # # from sqlalchemy import create_engine
# # # from sqlalchemy.orm import sessionmaker
# # # import random
# # # from faker import Faker
# # # from config import settings  # Import your settings
# # # from models import Brand, Category, Product  # Import your models
# # # from models import fast_add_relationships  # Import your utility function

# # # # Initialize Faker for fake data generation
# # # fake = Faker()

# # # # Database setup - using PostgreSQL from your config
# # # engine = create_engine(settings.DATABASE_URL)
# # # Session = sessionmaker(bind=engine)
# # # db = Session()

# # # def create_dummy_data():
# # #     # Create 20 brands
# # #     brands = []
# # #     for i in range(1, 21):
# # #         brand = Brand(
# # #             name=f"Brand {i}",
# # #             slug=f"brand-{i}",
# # #             description=fake.paragraph(),
# # #             is_active=random.choice([True, False])
# # #         )
# # #         brands.append(brand)
# # #         db.add(brand)
# # #     db.commit()

# # #     # Create 9 levels of categories
# # #     categories = []
# # #     parent = None
    
# # #     for level in range(1, 10):
# # #         # Create 3 categories per level
# # #         for i in range(1, 4):
# # #             category = Category(
# # #                 name=f"Level {level} Category {i}",
# # #                 slug=f"level-{level}-category-{i}",
# # #                 description=fake.sentence(),
# # #                 is_active=random.choice([True, False]),
# # #                 is_leaf=(level == 9),  # Only level 9 categories are leaves
# # #                 parent=parent.id if parent else None
# # #             )
# # #             db.add(category)
# # #             db.commit()
            
# # #             # Add closure table relationships
# # #             fast_add_relationships(db, category)
            
# # #             categories.append(category)
            
# # #             # Assign random brands to this category
# # #             if random.choice([True, False]):
# # #                 category.brands = random.sample(brands, random.randint(1, 3))
# # #                 db.commit()
        
# # #         # Set parent to first category of current level for next iteration
# # #         parent = next(c for c in categories if c.name == f"Level {level} Category 1")

# # #     # Create 100 products
# # #     for i in range(1, 101):
# # #         # Select random leaf category (level 9)
# # #         category = random.choice([c for c in categories if c.is_leaf])
        
# # #         # Get brands associated with this category
# # #         available_brands = category.brands if category.brands else brands
        
# # #         product = Product(
# # #             name=f"Product {i} - {fake.word().capitalize()}",
# # #             slug=f"product-{i}-{fake.word()}",
# # #             description=fake.paragraph(),
# # #             price=round(random.uniform(5, 1000), 2),
# # #             quantity=random.randint(0, 1000),
# # #             is_active=random.choice([True, False]),
# # #             image_path=f"products/image_{i}.jpg",
# # #             category=category,
# # #             brand=random.choice(available_brands)
# # #         )
# # #         db.add(product)
    
# # #     db.commit()
# # #     print("Dummy data created successfully!")

# # # if __name__ == "__main__":
# # #     create_dummy_data()





# # # import random
# # # from faker import Faker
# # # from sqlalchemy import create_engine
# # # from sqlalchemy.orm import sessionmaker
# # # from models import Base, Category, Brand, Product, CategoryRelationship, fast_add_relationships
# # # from pathlib import Path
# # # import csv
# # # import os
# # # from datetime import datetime
# # # import random
# # # from config import settings  # Import your settings
# # # import logging




# # # # Initialize Faker and logging
# # # fake = Faker()
# # # logging.basicConfig(filename='db_population.log', level=logging.INFO, 
# # #                    format='%(asctime)s - %(levelname)s - %(message)s')

# # # # Database setup
# # # # DATABASE_URL = "sqlite:///ecommerce.db"
# # # # engine = create_engine(DATABASE_URL)
# # # # Session = sessionmaker(bind=engine)
# # # # db = Session()

# # # # Database setup - using PostgreSQL from your config
# # # engine = create_engine(settings.DATABASE_URL)
# # # Session = sessionmaker(bind=engine)
# # # db = Session()


# # # def generate_slug(name):
# # #     """Generate URL-friendly slug from a name"""
# # #     return name.lower().replace(' ', '-').replace("'", "").replace(",", "")[:100]

# # # def generate_unique_slug(db, base_slug, model_class, max_attempts=5):
# # #     """Generate a unique slug by appending numbers if needed"""
# # #     slug = generate_slug(base_slug)
# # #     attempt = 1
    
# # #     while attempt <= max_attempts:
# # #         exists = db.query(model_class).filter(model_class.slug == slug).first()
# # #         if not exists:
# # #             return slug
# # #         attempt += 1
# # #         slug = f"{generate_slug(base_slug)}-{attempt}"
    
# # #     raise ValueError(f"Could not generate unique slug after {max_attempts} attempts")

# # # def create_category_hierarchy():
# # #     """Create a 9-level category hierarchy with proper relationships"""
# # #     try:
# # #         categories = []
# # #         logging.info("Starting category hierarchy creation")
        
# # #         # Level 1 (Root categories)
# # #         level1 = [
# # #             "Electronics", "Fashion", "Home & Kitchen", 
# # #             "Beauty", "Sports", "Books", "Toys", "Automotive"
# # #         ]
        
# # #         for name in level1:
# # #             try:
# # #                 cat = Category(
# # #                     name=name,
# # #                     slug=generate_unique_slug(db, name, Category),
# # #                     description=fake.sentence(),
# # #                     is_leaf=False
# # #                 )
# # #                 db.add(cat)
# # #                 categories.append(cat)
# # #                 logging.info(f"Created root category: {name}")
# # #             except Exception as e:
# # #                 logging.error(f"Error creating root category {name}: {str(e)}")
# # #                 continue
        
# # #         db.commit()
        
# # #         # Generate subcategories for levels 2-9
# # #         for level in range(2, 6):
# # #             parent_categories = [c for c in categories if not c.is_leaf]
# # #             new_categories = []
            
# # #             for parent in parent_categories:
# # #                 for _ in range(random.randint(2, 4)):  # 2-4 subcategories per parent
# # #                     try:
# # #                         name = fake.word().capitalize() + " " + fake.word().capitalize()
# # #                         is_leaf = random.choice([True, False]) if level < 9 else True
                        
# # #                         cat = Category(
# # #                             name=name,
# # #                             slug=generate_unique_slug(db, name, Category),
# # #                             description=fake.sentence(),
# # #                             parent_id=parent.id,
# # #                             is_leaf=is_leaf
# # #                         )
# # #                         db.add(cat)
# # #                         new_categories.append(cat)
# # #                         logging.info(f"Created L{level} category: {name} under {parent.name}")
# # #                     except Exception as e:
# # #                         logging.error(f"Error creating subcategory: {str(e)}")
# # #                         continue
            
# # #             db.commit()
# # #             categories.extend(new_categories)
            
# # #             # Add relationships for new categories
# # #             for cat in new_categories:
# # #                 try:
# # #                     fast_add_relationships(db, cat)
# # #                 except Exception as e:
# # #                     logging.error(f"Error creating relationships for {cat.name}: {str(e)}")
# # #                     continue
        
# # #         logging.info(f"Created {len(categories)} total categories")
# # #         return categories
    
# # #     except Exception as e:
# # #         db.rollback()
# # #         logging.error(f"Category hierarchy creation failed: {str(e)}")
# # #         raise

# # # def create_brands(categories):
# # #     """Create brands and associate them with categories"""
# # #     try:
# # #         brands = []
# # #         brand_names = set()
# # #         logging.info("Starting brand creation")
        
# # #         # Create 50 unique brands
# # #         while len(brands) < 50:
# # #             name = fake.company()
# # #             if name not in brand_names:
# # #                 try:
# # #                     brand = Brand(
# # #                         name=name,
# # #                         slug=generate_unique_slug(db, name, Brand),
# # #                         description=fake.catch_phrase(),
# # #                         is_active=random.choice([True, False])
# # #                     )
# # #                     db.add(brand)
# # #                     brands.append(brand)
# # #                     brand_names.add(name)
# # #                     logging.info(f"Created brand: {name}")
# # #                 except Exception as e:
# # #                     logging.error(f"Error creating brand {name}: {str(e)}")
# # #                     continue
        
# # #         db.commit()
        
# # #         # Associate brands with categories (3-8 brands per category)
# # #         for category in categories:
# # #             if random.random() > 0.2:  # 80% chance to have brands
# # #                 num_brands = random.randint(3, min(8, len(brands)))
# # #                 selected_brands = random.sample(brands, num_brands)
# # #                 category.brands.extend(selected_brands)
# # #                 logging.info(f"Associated {num_brands} brands with {category.name}")
        
# # #         db.commit()
# # #         logging.info(f"Created {len(brands)} brands with category associations")
# # #         return brands
    
# # #     except Exception as e:
# # #         db.rollback()
# # #         logging.error(f"Brand creation failed: {str(e)}")
# # #         raise

# # # def create_products(categories, brands, num_products=1000):
# # #     """Create sample products with proper category and brand relationships"""
# # #     try:
# # #         products = []
# # #         logging.info(f"Starting product creation ({num_products} products)")
        
# # #         leaf_categories = [c for c in categories if c.is_leaf]
        
# # #         for _ in range(num_products):
# # #             try:
# # #                 # Select random category that has brands
# # #                 category = random.choice(leaf_categories)
# # #                 while not category.brands:
# # #                     category = random.choice(leaf_categories)
                
# # #                 brand = random.choice(category.brands)
                
# # #                 product = Product(
# # #                     name=fake.text(max_nb_chars=50).rstrip('.'),
# # #                     slug=generate_unique_slug(db, fake.unique.word() + "-" + fake.word(), Product),
# # #                     description=fake.paragraph(),
# # #                     price=round(random.uniform(5, 1000), 2),
# # #                     quantity=random.randint(0, 500),
# # #                     is_active=random.choice([True, False]),
# # #                     image_path=f"products/{fake.uuid4()}.jpg",
# # #                     category_id=category.id,
# # #                     brand_id=brand.id,
# # #                     created_at=fake.date_time_this_year(),
# # #                     updated_at=fake.date_time_this_year()
# # #                 )
# # #                 db.add(product)
# # #                 products.append(product)
                
# # #                 if len(products) % 100 == 0:
# # #                     db.commit()
# # #                     logging.info(f"Created {len(products)} products so far")
# # #             except Exception as e:
# # #                 logging.error(f"Error creating product: {str(e)}")
# # #                 continue
        
# # #         db.commit()
# # #         logging.info(f"Successfully created {len(products)} products")
# # #         return products
    
# # #     except Exception as e:
# # #         db.rollback()
# # #         logging.error(f"Product creation failed: {str(e)}")
# # #         raise

# # # def export_sample_csv(filename="sample_products.csv"):
# # #     """Export sample CSV for bulk upload testing"""
# # #     try:
# # #         categories = db.query(Category).filter(Category.is_leaf == True).all()
# # #         brands = db.query(Brand).all()
        
# # #         with open(filename, mode='w', newline='', encoding='utf-8') as file:
# # #             writer = csv.writer(file)
# # #             writer.writerow([
# # #                 "name", "description", "price", "quantity", "is_active",
# # #                 "image_path", "category_slug", "brand_slug"
# # #             ])
            
# # #             for _ in range(50):
# # #                 category = random.choice(categories)
# # #                 brand = random.choice(brands)
                
# # #                 writer.writerow([
# # #                     fake.text(max_nb_chars=50).rstrip('.'),
# # #                     fake.paragraph(),
# # #                     round(random.uniform(5, 1000), 2),
# # #                     random.randint(0, 500),
# # #                     random.choice(["True", "False"]),
# # #                     f"products/{fake.uuid4()}.jpg",
# # #                     category.slug,
# # #                     brand.slug
# # #                 ])
        
# # #         logging.info(f"Sample CSV exported to {filename}")
    
# # #     except Exception as e:
# # #         logging.error(f"CSV export failed: {str(e)}")
# # #         raise

# # # def main():
# # #     print("Setting up e-commerce database...")
# # #     logging.info("Starting database population")
    
# # #     try:
# # #         # Clear existing data
# # #         print("Clearing existing data...")
# # #         logging.info("Clearing existing data")
# # #         db.query(CategoryRelationship).delete()
# # #         db.query(Product).delete()
# # #         db.query(Brand).delete()
# # #         db.query(Category).delete()
# # #         db.commit()
        
# # #         # Create category hierarchy
# # #         print("Creating category hierarchy (9 levels)...")
# # #         categories = create_category_hierarchy()
# # #         print(f"Created {len(categories)} categories")
        
# # #         # Create brands and associations
# # #         print("Creating brands and associations...")
# # #         brands = create_brands(categories)
# # #         print(f"Created {len(brands)} brands")
        
# # #         # Create sample products
# # #         print("Creating sample products...")
# # #         products = create_products(categories, brands, 1000)
# # #         print(f"Created {len(products)} products")
        
# # #         # Export sample CSV
# # #         print("Exporting sample CSV for testing...")
# # #         export_sample_csv()
# # #         print("Sample CSV exported to 'sample_products.csv'")
        
# # #         print("\nDatabase setup complete!")
# # #         logging.info("Database population completed successfully")
    
# # #     except Exception as e:
# # #         print(f"\nError during database setup: {str(e)}")
# # #         logging.error(f"Database population failed: {str(e)}")
# # #         db.rollback()
# # #     finally:
# # #         db.close()

# # # if __name__ == "__main__":
# # #     main()


# # # import random
# # # from faker import Faker
# # # from sqlalchemy import create_engine
# # # from sqlalchemy.orm import sessionmaker, Session
# # # from models import Base, Category, Brand, Product, CategoryRelationship
# # # from datetime import datetime
# # # import logging
# # # from typing import List
# # # from config import settings  # Import your settings

# # # # Initialize Faker and logging
# # # fake = Faker()
# # # logging.basicConfig(
# # #     level=logging.INFO,
# # #     format='%(asctime)s - %(levelname)s - %(message)s',
# # #     handlers=[
# # #         logging.FileHandler('db_population.log'),
# # #         logging.StreamHandler()
# # #     ]
# # # )

# # # # Database setup
# # # engine = create_engine(settings.DATABASE_URL)
# # # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # # Base.metadata.create_all(bind=engine)

# # # def generate_slug(name: str) -> str:
# # #     """Generate URL-friendly slug from a name"""
# # #     return name.lower().replace(' ', '-').replace("'", "").replace(",", "")[:100]

# # # def generate_unique_slug(db: Session, base_slug: str, model_class) -> str:
# # #     """Generate a unique slug by appending numbers if needed"""
# # #     slug = generate_slug(base_slug)
# # #     counter = 1
    
# # #     while db.query(model_class).filter(model_class.slug == slug).first() is not None:
# # #         slug = f"{generate_slug(base_slug)}-{counter}"
# # #         counter += 1
# # #         if counter > 10:
# # #             raise ValueError(f"Couldn't generate unique slug for {base_slug}")
    
# # #     return slug

# # # def create_category_relationship(db: Session, ancestor_id: int, descendant_id: int, depth: int):
# # #     """Helper function to create category relationships"""
# # #     try:
# # #         relationship = CategoryRelationship(
# # #             ancestor_id=ancestor_id,
# # #             descendant_id=descendant_id,
# # #             depth=depth
# # #         )
# # #         db.add(relationship)
# # #         db.commit()
# # #     except Exception as e:
# # #         db.rollback()
# # #         logging.error(f"Error creating relationship {ancestor_id}->{descendant_id}: {str(e)}")
# # #         raise

# # # def fast_add_relationships(db: Session, category: Category):
# # #     """Properly implement category relationships with transaction handling"""
# # #     try:
# # #         # Self relationship
# # #         create_category_relationship(db, category.id, category.id, 0)
        
# # #         # Inherit relationships from parent
# # #         if category.parent_id:
# # #             parent_relationships = db.query(CategoryRelationship).filter(
# # #                 CategoryRelationship.descendant_id == category.parent_id
# # #             ).all()
            
# # #             for rel in parent_relationships:
# # #                 create_category_relationship(
# # #                     db,
# # #                     rel.ancestor_id,
# # #                     category.id,
# # #                     rel.depth + 1
# # #                 )
# # #     except Exception as e:
# # #         logging.error(f"Error creating relationships for category {category.id}: {str(e)}")
# # #         raise

# # # def create_top_level_categories(db: Session) -> List[Category]:
# # #     """Create exactly 20 top-level categories"""
# # #     top_categories = [
# # #         "Electronics", "Computers", "Smart Home", "Office Supplies", 
# # #         "Men's Fashion", "Women's Fashion", "Kids & Baby", "Jewelry", 
# # #         "Home & Kitchen", "Furniture", "Bed & Bath", "Home Improvement", 
# # #         "Beauty & Personal Care", "Health & Wellness", "Grocery", 
# # #         "Sports & Outdoors", "Toys & Games", "Automotive", "Industrial", 
# # #         "Books & Media"
# # #     ]
    
# # #     categories = []
# # #     for name in top_categories:
# # #         try:
# # #             cat = Category(
# # #                 name=name,
# # #                 slug=generate_unique_slug(db, name, Category),
# # #                 description=fake.sentence(),
# # #                 is_leaf=False,
# # #                 parent_id=None
# # #             )
# # #             db.add(cat)
# # #             db.commit()
# # #             categories.append(cat)
# # #             logging.info(f"Created top-level category: {name}")
            
# # #             # Create self-relationship for top categories
# # #             fast_add_relationships(db, cat)
# # #         except Exception as e:
# # #             logging.error(f"Error creating category {name}: {str(e)}")
# # #             db.rollback()
    
# # #     return categories

# # # def create_subcategories(db: Session, parent_categories: List[Category], current_level: int = 1, max_level: int = 5) -> List[Category]:
# # #     """Recursively create subcategories up to specified depth"""
# # #     if current_level >= max_level:
# # #         return parent_categories
    
# # #     new_categories = []
# # #     for parent in parent_categories:
# # #         # Create 2-4 subcategories per parent
# # #         for _ in range(random.randint(2, 4)):
# # #             try:
# # #                 name = f"{parent.name} {fake.word().capitalize()}"
# # #                 is_leaf = (current_level == max_level - 1)
                
# # #                 cat = Category(
# # #                     name=name,
# # #                     slug=generate_unique_slug(db, name, Category),
# # #                     description=fake.sentence(),
# # #                     parent_id=parent.id,
# # #                     is_leaf=is_leaf
# # #                 )
# # #                 db.add(cat)
# # #                 db.commit()
# # #                 new_categories.append(cat)
# # #                 logging.info(f"Created L{current_level+1} category: {name} under {parent.name}")
                
# # #                 # Create relationships for the new category
# # #                 fast_add_relationships(db, cat)
# # #             except Exception as e:
# # #                 logging.error(f"Error creating subcategory: {str(e)}")
# # #                 db.rollback()
    
# # #     return create_subcategories(db, new_categories, current_level + 1, max_level)

# # # def create_brands(db: Session, categories: List[Category]) -> List[Brand]:
# # #     """Create 2-8 brands for each top-level category"""
# # #     brands = []
# # #     brand_names = set()
    
# # #     # Only associate brands with top-level categories (first 20)
# # #     top_categories = categories[:20]
    
# # #     for category in top_categories:
# # #         num_brands = random.randint(2, 8)
# # #         for _ in range(num_brands):
# # #             try:
# # #                 brand_name = fake.company()
# # #                 if brand_name in brand_names:
# # #                     continue
                    
# # #                 brand = Brand(
# # #                     name=brand_name,
# # #                     slug=generate_unique_slug(db, brand_name, Brand),
# # #                     description=fake.catch_phrase(),
# # #                     is_active=True
# # #                 )
# # #                 db.add(brand)
# # #                 db.commit()
# # #                 brands.append(brand)
# # #                 brand_names.add(brand_name)
                
# # #                 # Associate brand with category
# # #                 category.brands.append(brand)
# # #                 db.commit()
# # #                 logging.info(f"Created brand {brand_name} for category {category.name}")
# # #             except Exception as e:
# # #                 logging.error(f"Error creating brand: {str(e)}")
# # #                 db.rollback()
    
# # #     return brands

# # # def create_products(db: Session, categories: List[Category], products_per_brand: int = 3) -> List[Product]:
# # #     """Create products for each brand-category combination"""
# # #     products = []
# # #     leaf_categories = [c for c in categories if c.is_leaf]
    
# # #     for category in leaf_categories:
# # #         # Get all brands from parent categories if leaf has none
# # #         if not category.brands:
# # #             parent_relationships = db.query(CategoryRelationship).filter(
# # #                 CategoryRelationship.descendant_id == category.id,
# # #                 CategoryRelationship.depth > 0
# # #             ).order_by(CategoryRelationship.depth).first()
            
# # #             if parent_relationships:
# # #                 parent = db.query(Category).get(parent_relationships.ancestor_id)
# # #                 if parent and parent.brands:
# # #                     category.brands = parent.brands
        
# # #         for brand in category.brands:
# # #             for _ in range(products_per_brand):
# # #                 try:
# # #                     product_name = f"{brand.name} {fake.word().capitalize()} {random.randint(100, 999)}"
                    
# # #                     product = Product(
# # #                         name=product_name,
# # #                         slug=generate_unique_slug(db, product_name, Product),
# # #                         description=fake.paragraph(),
# # #                         price=round(random.uniform(10, 2000), 2),
# # #                         quantity=random.randint(10, 500),
# # #                         is_active=True,
# # #                         image_path=f"products/{fake.uuid4()}.jpg",
# # #                         category_id=category.id,
# # #                         brand_id=brand.id,
# # #                         created_at=datetime.now(),
# # #                         updated_at=datetime.now()
# # #                     )
# # #                     db.add(product)
# # #                     db.commit()
# # #                     products.append(product)
# # #                     logging.info(f"Created product {product_name} for {brand.name} in {category.name}")
# # #                 except Exception as e:
# # #                     logging.error(f"Error creating product: {str(e)}")
# # #                     db.rollback()
    
# # #     return products

# # # def main():
# # #     db = SessionLocal()
# # #     try:
# # #         logging.info("Starting database population")
        
# # #         # Clear existing data in proper order due to foreign key constraints
# # #         logging.info("Clearing existing data")
# # #         db.query(Product).delete()
# # #         db.query(CategoryRelationship).delete()
# # #         db.query(Brand).delete()
# # #         db.query(Category).delete()
# # #         db.commit()
        
# # #         # Create exactly 20 top-level categories
# # #         logging.info("Creating 20 top-level categories")
# # #         top_categories = create_top_level_categories(db)
        
# # #         # Create subcategories (5 levels total)
# # #         logging.info("Creating subcategories (5 levels total)")
# # #         all_categories = create_subcategories(db, top_categories)
        
# # #         # Create brands (2-8 per top category)
# # #         logging.info("Creating brands (2-8 per top category)")
# # #         brands = create_brands(db, all_categories)
        
# # #         # Create products (3 per brand-category combination)
# # #         logging.info("Creating products (3 per brand-category combo)")
# # #         products = create_products(db, all_categories)
        
# # #         logging.info(f"""
# # #         Database population completed successfully:
# # #         - Top categories: {len(top_categories)}
# # #         - Total categories: {len(all_categories)}
# # #         - Brands created: {len(brands)}
# # #         - Products created: {len(products)}
# # #         """)
        
# # #     except Exception as e:
# # #         logging.error(f"Database population failed: {str(e)}")
# # #         db.rollback()
# # #         raise
# # #     finally:
# # #         db.close()

# # # if __name__ == "__main__":
# # #     main()







# # # import requests
# # # from bs4 import BeautifulSoup
# # # import random
# # # from sqlalchemy import create_engine
# # # from sqlalchemy.orm import sessionmaker, Session
# # # from models import Base, Category, Brand, Product, CategoryRelationship
# # # from datetime import datetime
# # # import logging
# # # from typing import List, Dict
# # # import json
# # # from config import settings
# # # from uuid import uuid4

# # # # Initialize logging
# # # logging.basicConfig(
# # #     level=logging.INFO,
# # #     format='%(asctime)s - %(levelname)s - %(message)s',
# # #     handlers=[
# # #         logging.FileHandler('db_population.log'),
# # #         logging.StreamHandler()
# # #     ]
# # # )

# # # # Database setup
# # # engine = create_engine(settings.DATABASE_URL)
# # # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # # Base.metadata.create_all(bind=engine)

# # # # Helpers
# # # def generate_slug(name: str) -> str:
# # #     return name.lower().replace(' ', '-').replace("'", "").replace(",", "")[:100]

# # # def generate_unique_slug(db: Session, base_slug: str, model_class) -> str:
# # #     slug = generate_slug(base_slug)
# # #     counter = 1
# # #     while db.query(model_class).filter(model_class.slug == slug).first() is not None:
# # #         slug = f"{generate_slug(base_slug)}-{counter}"
# # #         counter += 1
# # #         if counter > 10:
# # #             raise ValueError(f"Couldn't generate unique slug for {base_slug}")
# # #     return slug

# # # def create_category_relationship(db: Session, ancestor_id: int, descendant_id: int, depth: int):
# # #     try:
# # #         relationship = CategoryRelationship(
# # #             ancestor_id=ancestor_id,
# # #             descendant_id=descendant_id,
# # #             depth=depth
# # #         )
# # #         db.add(relationship)
# # #         db.commit()
# # #     except Exception as e:
# # #         db.rollback()
# # #         logging.error(f"Error creating relationship {ancestor_id}->{descendant_id}: {str(e)}")
# # #         raise

# # # def fast_add_relationships(db: Session, category: Category):
# # #     try:
# # #         create_category_relationship(db, category.id, category.id, 0)
# # #         if category.parent_id:
# # #             parent_relationships = db.query(CategoryRelationship).filter(
# # #                 CategoryRelationship.descendant_id == category.parent_id
# # #             ).all()
# # #             for rel in parent_relationships:
# # #                 create_category_relationship(
# # #                     db,
# # #                     rel.ancestor_id,
# # #                     category.id,
# # #                     rel.depth + 1
# # #                 )
# # #     except Exception as e:
# # #         logging.error(f"Error creating relationships for category {category.id}: {str(e)}")
# # #         raise

# # # # === MAIN CATEGORY + BRAND GENERATION ===

# # # def get_predefined_categories() -> List[Dict]:
# # #     return [
# # #         {
# # #             "name": "Electronics",
# # #             "subcategories": ["Computers", "Smart Home", "Office Supplies"]
# # #         },
# # #         {
# # #             "name": "Fashion",
# # #             "subcategories": ["Men's Clothing", "Women's Clothing", "Kids & Baby"]
# # #         },
# # #     ]

# # # def fetch_brands_for_category(category_name: str) -> List[str]:
# # #     brand_map = {
# # #         "Electronics": ["Apple", "Samsung", "Sony", "LG", "Bose"],
# # #         "Computers": ["Dell", "HP", "Lenovo", "Asus", "Acer"],
# # #         "Men's Clothing": ["Nike", "Adidas", "Levi's", "Calvin Klein", "Tommy Hilfiger"],
# # #     }
# # #     return brand_map.get(category_name, ["Generic Brand"])

# # # def generate_realistic_product_name(category: str, brand: str) -> str:
# # #     product_types = {
# # #         "Electronics": [f"{brand} Smartphone", f"{brand} Tablet", f"{brand} Smart Watch", f"{brand} Earbuds"],
# # #         "Computers": [f"{brand} Laptop", f"{brand} Monitor", f"{brand} Keyboard"],
# # #         "Men's Clothing": [f"{brand} T-Shirt", f"{brand} Jeans", f"{brand} Sneakers"],
# # #     }
# # #     base_category = next((key for key in product_types if key in category), "Electronics")
# # #     return random.choice(product_types[base_category])

# # # def create_real_categories(db: Session) -> List[Category]:
# # #     categories = []
# # #     category_data = get_predefined_categories()  # ✅ Replacing Amazon scraping

# # #     for top_cat in category_data:
# # #         try:
# # #             cat = Category(
# # #                 name=top_cat['name'],
# # #                 slug=generate_unique_slug(db, top_cat['name'], Category),
# # #                 description=f"Shop {top_cat['name']} products",
# # #                 is_leaf=False,
# # #                 parent_id=None
# # #             )
# # #             db.add(cat)
# # #             db.commit()
# # #             categories.append(cat)
# # #             logging.info(f"Created top-level category: {top_cat['name']}")
# # #             fast_add_relationships(db, cat)

# # #             for subcat_name in top_cat.get('subcategories', []):
# # #                 subcat = Category(
# # #                     name=subcat_name,
# # #                     slug=generate_unique_slug(db, subcat_name, Category),
# # #                     description=f"Shop {subcat_name} products",
# # #                     is_leaf=True,
# # #                     parent_id=cat.id
# # #                 )
# # #                 db.add(subcat)
# # #                 db.commit()
# # #                 categories.append(subcat)
# # #                 logging.info(f"Created subcategory: {subcat_name} under {top_cat['name']}")
# # #                 fast_add_relationships(db, subcat)

# # #         except Exception as e:
# # #             logging.error(f"Error creating category {top_cat['name']}: {str(e)}")
# # #             db.rollback()

# # #     return categories

# # # def create_real_brands(db: Session, categories: List[Category]) -> List[Brand]:
# # #     brands = []
# # #     brand_names = set()
# # #     for category in categories[:20]:
# # #         try:
# # #             category_brands = fetch_brands_for_category(category.name)
# # #             for brand_name in category_brands[:5]:
# # #                 if brand_name in brand_names:
# # #                     continue
# # #                 brand = Brand(
# # #                     name=brand_name,
# # #                     slug=generate_unique_slug(db, brand_name, Brand),
# # #                     description=f"{brand_name} official products",
# # #                     is_active=True
# # #                 )
# # #                 db.add(brand)
# # #                 db.commit()
# # #                 brands.append(brand)
# # #                 brand_names.add(brand_name)

# # #                 category.brands.append(brand)
# # #                 db.commit()
# # #                 logging.info(f"Created brand {brand_name} for category {category.name}")
# # #         except Exception as e:
# # #             logging.error(f"Error creating brand {brand_name}: {str(e)}")
# # #             db.rollback()

# # #     return brands

# # # def create_real_products(db: Session, categories: List[Category], products_per_brand: int = 3) -> List[Product]:
# # #     products = []
# # #     leaf_categories = [c for c in categories if c.is_leaf]

# # #     for category in leaf_categories:
# # #         if not category.brands and category.parent_id:
# # #             parent = db.query(Category).get(category.parent_id)
# # #             if parent and parent.brands:
# # #                 category.brands = parent.brands

# # #         for brand in category.brands:
# # #             for _ in range(products_per_brand):
# # #                 try:
# # #                     name = generate_realistic_product_name(category.name, brand.name)
# # #                     price = round(random.uniform(50, 2000), 2)
# # #                     product = Product(
# # #                         name=name,
# # #                         slug=generate_unique_slug(db, name, Product),
# # #                         description=f"Official {brand.name} {name}",
# # #                         price=price,
# # #                         quantity=random.randint(10, 500),
# # #                         is_active=True,
# # #                         image_path=f"products/{brand.slug}-{uuid4()}.jpg",
# # #                         category_id=category.id,
# # #                         brand_id=brand.id,
# # #                         created_at=datetime.now(),
# # #                         updated_at=datetime.now()
# # #                     )
# # #                     db.add(product)
# # #                     db.commit()
# # #                     products.append(product)
# # #                     logging.info(f"Created product {name} in {category.name}")
# # #                 except Exception as e:
# # #                     logging.error(f"Error creating product: {str(e)}")
# # #                     db.rollback()

# # #     return products

# # # # === MAIN SCRIPT ===

# # # def main():
# # #     db = SessionLocal()
# # #     try:
# # #         logging.info("Starting database population")
# # #         db.query(Product).delete()
# # #         db.query(CategoryRelationship).delete()
# # #         db.query(Brand).delete()
# # #         db.query(Category).delete()
# # #         db.commit()

# # #         categories = create_real_categories(db)
# # #         brands = create_real_brands(db, categories)
# # #         products = create_real_products(db, categories)

# # #         logging.info(f"""
# # #         ✅ Database population completed:
# # #         - Categories created: {len(categories)}
# # #         - Brands created: {len(brands)}
# # #         - Products created: {len(products)}
# # #         """)

# # #     except Exception as e:
# # #         logging.error(f"Fatal error: {str(e)}")
# # #         db.rollback()
# # #     finally:
# # #         db.close()

# # # if __name__ == "__main__":
# # #     main()






# # import random
# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker, Session
# # from models import Base, Category, Brand, Product, CategoryRelationship
# # from datetime import datetime
# # import logging
# # from typing import List, Dict
# # from uuid import uuid4
# # from config import settings

# # # Initialize logging
# # logging.basicConfig(
# #     level=logging.INFO,
# #     format='%(asctime)s - %(levelname)s - %(message)s',
# #     handlers=[
# #         logging.FileHandler('db_population.log', encoding='utf-8'),
# #         logging.StreamHandler()
# #     ]
# # )

# # # Database setup
# # engine = create_engine(settings.DATABASE_URL)
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # def create_tables():
# #     """Create all database tables"""
# #     Base.metadata.create_all(bind=engine)
# #     logging.info("Database tables created")

# # # Helper functions
# # def generate_slug(name: str) -> str:
# #     return name.lower().replace(' ', '-').replace("'", "").replace(",", "")[:100]

# # def generate_unique_slug(db: Session, base_slug: str, model_class) -> str:
# #     slug = generate_slug(base_slug)
# #     counter = 1
# #     while db.query(model_class).filter(model_class.slug == slug).first() is not None:
# #         slug = f"{generate_slug(base_slug)}-{counter}"
# #         counter += 1
# #         if counter > 10:
# #             raise ValueError(f"Couldn't generate unique slug for {base_slug}")
# #     return slug

# # def calculate_discount_percent(price: float, selling_price: float) -> float:
# #     """Calculate discount percentage based on price and selling price"""
# #     if selling_price >= price or price == 0:
# #         return 0.0
# #     return round(((price - selling_price) / price) * 100, 2)

# # def create_category_relationship(db: Session, ancestor_id: int, descendant_id: int, depth: int):
# #     """Create a category relationship with proper session handling"""
# #     try:
# #         # Check if relationship already exists
# #         existing = db.query(CategoryRelationship).filter(
# #             CategoryRelationship.ancestor_id == ancestor_id,
# #             CategoryRelationship.descendant_id == descendant_id
# #         ).first()
        
# #         if not existing:
# #             relationship = CategoryRelationship(
# #                 ancestor_id=ancestor_id,
# #                 descendant_id=descendant_id,
# #                 depth=depth
# #             )
# #             db.add(relationship)
# #             db.commit()
# #             return relationship
# #         return existing
# #     except Exception as e:
# #         db.rollback()
# #         logging.error(f"Error creating relationship {ancestor_id}->{descendant_id}: {str(e)}")
# #         raise

# # def fast_add_relationships(db: Session, category: Category):
# #     """Efficiently add all required category relationships"""
# #     try:
# #         # Self-relationship
# #         create_category_relationship(db, category.id, category.id, 0)
        
# #         if category.parent_id:
# #             # Get all ancestor relationships of the parent
# #             parent_relationships = db.query(CategoryRelationship).filter(
# #                 CategoryRelationship.descendant_id == category.parent_id
# #             ).all()
            
# #             # Create relationships from all ancestors to this category
# #             for rel in parent_relationships:
# #                 create_category_relationship(
# #                     db,
# #                     rel.ancestor_id,
# #                     category.id,
# #                     rel.depth + 1
# #                 )
# #     except Exception as e:
# #         logging.error(f"Error creating relationships for category {category.id}: {str(e)}")
# #         raise

# # # Data generation functions
# # def get_predefined_categories() -> List[Dict]:
# #     return [
# #         {
# #             "name": "Electronics",
# #             "subcategories": ["Computers", "Smart Home", "Office Supplies"]
# #         },
# #         {
# #             "name": "Fashion",
# #             "subcategories": ["Men's Clothing", "Women's Clothing", "Kids & Baby"]
# #         },
# #     ]

# # def fetch_brands_for_category(category_name: str) -> List[str]:
# #     brand_map = {
# #         "Electronics": ["Apple", "Samsung", "Sony", "LG", "Bose"],
# #         "Computers": ["Dell", "HP", "Lenovo", "Asus", "Acer"],
# #         "Men's Clothing": ["Nike", "Adidas", "Levi's", "Calvin Klein", "Tommy Hilfiger"],
# #     }
# #     return brand_map.get(category_name, ["Generic Brand"])

# # def generate_realistic_product_name(category: str, brand: str) -> str:
# #     product_types = {
# #         "Electronics": [f"{brand} Smartphone", f"{brand} Tablet", f"{brand} Smart Watch"],
# #         "Computers": [f"{brand} Laptop", f"{brand} Monitor", f"{brand} Keyboard"],
# #         "Men's Clothing": [f"{brand} T-Shirt", f"{brand} Jeans", f"{brand} Sneakers"],
# #     }
# #     base_category = next((key for key in product_types if key in category), "Electronics")
# #     return random.choice(product_types[base_category])

# # def create_real_categories(db: Session) -> List[Category]:
# #     categories = []
# #     category_data = get_predefined_categories()

# #     for top_cat in category_data:
# #         try:
# #             # Create top-level category
# #             cat = Category(
# #                 name=top_cat['name'],
# #                 slug=generate_unique_slug(db, top_cat['name'], Category),
# #                 description=f"Shop {top_cat['name']} products",
# #                 is_leaf=False,
# #                 parent_id=None
# #             )
# #             db.add(cat)
# #             db.commit()
# #             categories.append(cat)
# #             logging.info(f"Created top-level category: {top_cat['name']}")
            
# #             # Create self-relationship
# #             fast_add_relationships(db, cat)

# #             # Create subcategories
# #             for subcat_name in top_cat.get('subcategories', []):
# #                 subcat = Category(
# #                     name=subcat_name,
# #                     slug=generate_unique_slug(db, subcat_name, Category),
# #                     description=f"Shop {subcat_name} products",
# #                     is_leaf=True,
# #                     parent_id=cat.id
# #                 )
# #                 db.add(subcat)
# #                 db.commit()
# #                 categories.append(subcat)
# #                 logging.info(f"Created subcategory: {subcat_name} under {top_cat['name']}")
                
# #                 # Create relationships for subcategory
# #                 fast_add_relationships(db, subcat)

# #         except Exception as e:
# #             logging.error(f"Error creating category {top_cat['name']}: {str(e)}")
# #             db.rollback()

# #     return categories

# # def create_real_brands(db: Session, categories: List[Category]) -> List[Brand]:
# #     brands = []
# #     brand_names = set()
    
# #     for category in categories[:20]:  # Limit to first 20 categories to avoid too many brands
# #         try:
# #             category_brands = fetch_brands_for_category(category.name)
            
# #             for brand_name in category_brands[:5]:  # Limit to 5 brands per category
# #                 if brand_name in brand_names:
# #                     continue
                    
# #                 brand = Brand(
# #                     name=brand_name,
# #                     slug=generate_unique_slug(db, brand_name, Brand),
# #                     description=f"{brand_name} official products",
# #                     is_active=True
# #                 )
# #                 db.add(brand)
# #                 db.commit()
# #                 brands.append(brand)
# #                 brand_names.add(brand_name)

# #                 # Associate brand with category
# #                 category.brands.append(brand)
# #                 db.commit()
# #                 logging.info(f"Created brand {brand_name} for category {category.name}")
                
# #         except Exception as e:
# #             logging.error(f"Error creating brand {brand_name}: {str(e)}")
# #             db.rollback()

# #     return brands

# # def create_real_products(db: Session, categories: List[Category], products_per_brand: int = 3) -> List[Product]:
# #     products = []
# #     leaf_categories = [c for c in categories if c.is_leaf]

# #     for category in leaf_categories:
# #         # If category has no brands but has a parent, inherit parent's brands
# #         if not category.brands and category.parent_id:
# #             parent = db.get(Category, category.parent_id)
# #             if parent and parent.brands:
# #                 category.brands = parent.brands

# #         for brand in category.brands:
# #             for _ in range(products_per_brand):
# #                 try:
# #                     name = generate_realistic_product_name(category.name, brand.name)
                    
# #                     # Generate random prices
# #                     price = round(random.uniform(50, 2000), 2)
# #                     selling_price = round(random.uniform(price * 0.6, price * 0.95), 2)  # 5-40% discount
                    
# #                     # Calculate discount percentage
# #                     discount = calculate_discount_percent(price, selling_price)
                    
# #                     product = Product(
# #                         name=name,
# #                         slug=generate_unique_slug(db, name, Product),
# #                         description=f"Official {brand.name} {name}",
# #                         price=price,
# #                         selling_price=selling_price,
# #                         discount=discount,
# #                         quantity=random.randint(10, 500),
# #                         is_active=True,
# #                         image_path=f"products/{brand.slug}-{uuid4()}.jpg",
# #                         category_id=category.id,
# #                         brand_id=brand.id,
# #                         created_at=datetime.now(),
# #                         updated_at=datetime.now()
# #                     )
# #                     db.add(product)
# #                     db.commit()
# #                     products.append(product)
                    
# #                     logging.info(
# #                         f"Created product {name} - "
# #                         f"Price: ${price:.2f}, "
# #                         f"Selling: ${selling_price:.2f}, "
# #                         f"Discount: {discount}%"
# #                     )
                    
# #                 except Exception as e:
# #                     logging.error(f"Error creating product: {str(e)}")
# #                     db.rollback()

# #     return products

# # def main():
# #     # Create tables if they don't exist
# #     create_tables()
    
# #     db = SessionLocal()
# #     try:
# #         logging.info("Starting database population")
        
# #         # Clear existing data (if any)
# #         db.query(Product).delete()
# #         db.query(CategoryRelationship).delete()
# #         db.query(Brand).delete()
# #         db.query(Category).delete()
# #         db.commit()

# #         # Create new data
# #         categories = create_real_categories(db)
# #         brands = create_real_brands(db, categories)
# #         products = create_real_products(db, categories)

# #         # Success message
# #         logging.info("\nDatabase population completed successfully:")
# #         logging.info(f"- Categories created: {len(categories)}")
# #         logging.info(f"- Brands created: {len(brands)}")
# #         logging.info(f"- Products created: {len(products)}")

# #     except Exception as e:
# #         logging.error(f"Fatal error during database population: {str(e)}")
# #         db.rollback()
# #     finally:
# #         db.close()

# # if __name__ == "__main__":
# #     main()




# import pandas as pd
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# import os

# # Database connection settings (replace with your actual credentials)
# DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/hednor_db"

# # Path to your CSV file
# CSV_FILE_PATH = r"C:\Users\PRABODH AWASTHI\Documents\biilpaymentfastapi\hednor_fastapi\app\Untitled spreadsheet - Amazon_Category_Hierarchy.csv"

# def upload_csv_to_database():
#     try:
#         # Read the CSV file
#         df = pd.read_csv(CSV_FILE_PATH)
        
#         # Display the first few rows to understand the structure
#         print("CSV file sample:")
#         print(df.head())
        
#         # Initialize database connection
#         engine = create_engine(DATABASE_URL)
#         Session = sessionmaker(bind=engine)
#         session = Session()
        
#         # Create a dictionary to store category name to ID mapping
#         category_map = {}
        
#         # First pass: Create all categories and store their IDs
#         for _, row in df.iterrows():
#             # Assuming your CSV has columns like 'name', 'parent_name', etc.
#             # Adjust these column names based on your actual CSV structure
#             category_name = row['name']  # Replace 'name' with actual column name
#             parent_name = row.get('parent_name')  # Replace with actual column name if exists
            
#             # Skip if category already processed
#             if category_name in category_map:
#                 continue
                
#             # Check if this is a root category (no parent)
#             parent_id = None
#             if parent_name and parent_name in category_map:
#                 parent_id = category_map[parent_name]
            
#             # Determine if this is a leaf category (no children)
#             # This logic might need adjustment based on your CSV structure
#             is_leaf = True  # You might need a better way to determine this
            
#             # Insert the category
#             result = session.execute(
#                 text("""
#                     INSERT INTO categories (name, slug, is_active, is_leaf, parent_id)
#                     VALUES (:name, :slug, :is_active, :is_leaf, :parent_id)
#                     RETURNING id
#                 """),
#                 {
#                     'name': category_name,
#                     'slug': category_name.lower().replace(' ', '-'),
#                     'is_active': True,
#                     'is_leaf': is_leaf,
#                     'parent_id': parent_id
#                 }
#             )
            
#             # Store the new category ID
#             category_id = result.fetchone()[0]
#             category_map[category_name] = category_id
        
#         # Commit the transaction
#         session.commit()
#         print(f"Successfully inserted {len(category_map)} categories into the database.")
        
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         session.rollback()
#     finally:
#         session.close()

# if __name__ == "__main__":
#     upload_csv_to_database()






import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import os
import re
from typing import Dict, Optional
import time

# Database connection settings (replace with your actual credentials)
DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/hednor_db"

# Path to your CSV file
CSV_FILE_PATH = r"C:\Users\PRABODH AWASTHI\Documents\biilpaymentfastapi\hednor_fastapi\app\Untitled spreadsheet - Amazon_Category_Hierarchy.csv"

def create_slug(name: str) -> str:
    """Generate a slug from the category name"""
    slug = re.sub(r'[^\w-]+', '-', name.lower().replace("'", ""))
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug

def upload_csv_to_database():
    try:
        # Read the CSV file
        df = pd.read_csv(CSV_FILE_PATH)
        
        print("CSV file loaded successfully. Starting database import...")
        
        # Initialize database connection
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Create a dictionary to store category path to ID mapping
        category_map: Dict[str, int] = {}
        
        # Get existing slugs from database to avoid duplicates
        existing_slugs = {row[0] for row in session.execute(text("SELECT slug FROM categories")).fetchall()}
        
        # Function to get a unique slug
        def get_unique_slug(base_slug: str) -> str:
            slug = base_slug
            counter = 1
            while slug in existing_slugs:
                slug = f"{base_slug}-{counter}"
                counter += 1
            existing_slugs.add(slug)
            return slug
        
        total_rows = len(df)
        processed_rows = 0
        start_time = time.time()
        
        # Process each row in the dataframe
        for _, row in df.iterrows():
            current_path = []
            parent_id = None
            
            # Process each level in the hierarchy
            for level in range(1, 10):  # For Level 1 to Level 9
                col_name = f"Level {level}"
                if col_name not in row or pd.isna(row[col_name]):
                    break
                
                category_name = str(row[col_name]).strip()
                current_path.append(category_name)
                path_key = " > ".join(current_path)
                
                # If category not already processed, insert it
                if path_key not in category_map:
                    # Determine if this is a leaf category
                    is_leaf = True
                    if level < 9:
                        next_level = f"Level {level + 1}"
                        if next_level in row and not pd.isna(row[next_level]):
                            is_leaf = False
                    
                    # Generate slug
                    base_slug = create_slug(category_name)
                    slug = get_unique_slug(base_slug)
                    
                    try:
                        # Insert the category
                        result = session.execute(
                            text("""
                                INSERT INTO categories 
                                (name, slug, is_active, is_leaf, parent_id)
                                VALUES (:name, :slug, :is_active, :is_leaf, :parent_id)
                                RETURNING id
                            """),
                            {
                                'name': category_name,
                                'slug': slug,
                                'is_active': True,
                                'is_leaf': is_leaf,
                                'parent_id': parent_id
                            }
                        )
                        
                        # Store the new category ID
                        category_id = result.fetchone()[0]
                        category_map[path_key] = category_id
                        parent_id = category_id
                        
                    except IntegrityError as e:
                        session.rollback()
                        print(f"Error inserting category {category_name}: {e}")
                        raise
                        
                else:
                    parent_id = category_map[path_key]
            
            processed_rows += 1
            if processed_rows % 100 == 0:
                elapsed = time.time() - start_time
                print(f"Processed {processed_rows}/{total_rows} rows ({processed_rows/total_rows:.1%}) in {elapsed:.1f}s")
        
        # Commit the transaction
        session.commit()
        elapsed = time.time() - start_time
        print(f"\nSuccessfully processed {processed_rows} rows in {elapsed:.1f} seconds")
        print(f"Inserted/updated {len(category_map)} categories")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        if 'session' in locals():
            session.rollback()
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    upload_csv_to_database()