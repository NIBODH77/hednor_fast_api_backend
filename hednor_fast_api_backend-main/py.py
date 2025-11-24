# import os
# import json
# import csv
# from pathlib import Path
# import sys
# import io


# # File paths
# BASE_DIR = Path("C:/Users/PRABODH AWASTHI/Documents/biilpaymentfastapi/hednor_fastapi/")
# TREE_FILE = BASE_DIR / "tree_output.txt"
# CATEGORIES_JSON = BASE_DIR / "categories.json"
# BRANDS_JSON = BASE_DIR / "brands.json"
# RELATIONSHIPS_JSON = BASE_DIR / "category_relationships.json"
# BRANDS_CSV = BASE_DIR / "brands.csv"


# # Utility functions
# def slugify(name):
#     return name.lower().replace(" ", "-").replace("/", "-").strip()


# def is_brand_line(line):
#     return "Brand:" in line


# def extract_brand_names(line):
#     return [b.strip() for b in line.split("Brand:")[-1].split(",") if b.strip()]


# # Tree parser
# def parse_tree(lines):
#     categories = []
#     brands = {}
#     relationships = []
#     stack = []

#     category_id = 1
#     brand_id = 1
#     id_map = {}

#     for line in lines:
#         stripped = line.lstrip("│├└─ ")
#         depth = len(line) - len(stripped)
#         name = stripped.strip()

#         if is_brand_line(name):
#             brand_names = extract_brand_names(name)
#             if stack:
#                 parent_category_id = stack[-1]["id"]
#                 for brand_name in brand_names:
#                     slug = slugify(brand_name)
#                     if slug not in brands:
#                         brands[slug] = {
#                             "id": brand_id,
#                             "name": brand_name,
#                             "slug": slug,
#                             "description": None,
#                             "is_active": True,
#                             "categories": [parent_category_id],
#                         }
#                         brand_id += 1
#                     else:
#                         if parent_category_id not in brands[slug]["categories"]:
#                             brands[slug]["categories"].append(parent_category_id)
#             continue

#         # Handle category stack
#         while stack and stack[-1]["depth"] >= depth:
#             stack.pop()

#         parent_id = stack[-1]["id"] if stack else None

#         category = {
#             "id": category_id,
#             "name": name,
#             "slug": slugify(name),
#             "description": None,
#             "is_active": True,
#             "is_leaf": True,
#             "parent_id": parent_id
#         }

#         # Update parent to not be leaf
#         if parent_id:
#             for c in categories:
#                 if c["id"] == parent_id:
#                     c["is_leaf"] = False
#                     break

#         # Add closure relationships (CategoryRelationship)
#         for ancestor in stack:
#             relationships.append({
#                 "ancestor_id": ancestor["id"],
#                 "descendant_id": category_id,
#                 "depth": depth - ancestor["depth"]
#             })

#         # Self-relationship (depth = 0)
#         relationships.append({
#             "ancestor_id": category_id,
#             "descendant_id": category_id,
#             "depth": 0
#         })

#         # Add to data
#         categories.append(category)
#         stack.append({"id": category_id, "depth": depth})
#         category_id += 1

#     return categories, list(brands.values()), relationships


# # ---- Run the parser ----
# if not TREE_FILE.exists():
#     raise FileNotFoundError(f"tree_output.txt not found at: {TREE_FILE}")

# with open(TREE_FILE, "r", encoding="utf-8") as f:
#     lines = f.readlines()

# categories, brands, relationships = parse_tree(lines)

# # ---- Write categories.json ----
# with open(CATEGORIES_JSON, "w", encoding="utf-8") as f:
#     json.dump(categories, f, indent=4, ensure_ascii=False)

# # ---- Write brands.json ----
# with open(BRANDS_JSON, "w", encoding="utf-8") as f:
#     json.dump(brands, f, indent=4, ensure_ascii=False)

# # ---- Write category_relationships.json ----
# with open(RELATIONSHIPS_JSON, "w", encoding="utf-8") as f:
#     json.dump(relationships, f, indent=4, ensure_ascii=False)

# # ---- Write brands.csv ----
# with open(BRANDS_CSV, "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["id", "name", "slug", "description", "is_active", "category_ids"])
#     for brand in brands:
#         writer.writerow([
#             brand["id"],
#             brand["name"],
#             brand["slug"],
#             brand["description"] or "",
#             brand["is_active"],
#             ",".join(map(str, brand["categories"]))
#         ])

# print("✅ Generated:")
# print(f"- {CATEGORIES_JSON.name}")
# print(f"- {BRANDS_JSON.name}")
# print(f"- {RELATIONSHIPS_JSON.name}")
# print(f"- {BRANDS_CSV.name}")



# import os
# import csv
# import json
# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# json_path = 'c:/Users/PRABODH AWASTHI/Documents/biilpaymentfastapi/hednor_fastapi/product.json'

# if os.path.exists(json_path):
#     with open(json_path, 'r') as json_file:
#         data = json.load(json_file)

#     with open('products.csv', 'w', newline='', encoding='utf-8') as csv_file:
#         fieldnames = ['image', 'name', 'price', 'stock', 'category', 'brand', 'status', 'actions']
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(data)

#     print("CSV file created successfully.")
# else:
#     print(f"❌ File not found at: {json_path}")


import csv
import os

input_csv = 'hednor_fastapi/products.csv'  # place your original CSV here
output_csv = 'csv/products_cleaned.csv'

# Ensure the CSV folder exists
os.makedirs('csv', exist_ok=True)

with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    
    # New field names
    fieldnames = ['image_path', 'name', 'price', 'quantity', 'category_name', 'brand_name', 'is_active']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        cleaned_row = {
            'image_path': row['Image'].replace('/uploads/products/', ''),
            'name': row['Name'],
            'price': row['Price'],
            'quantity': row['Stock'],
            'category_name': row['Category'],
            'brand_name': row['Brand'],
            'is_active': row['Status'] == 'Active'
        }
        writer.writerow(cleaned_row)

print(f"✅ Cleaned CSV created at: {output_csv}")
