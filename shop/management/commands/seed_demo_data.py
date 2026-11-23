from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from shop.models import Category, Product


# Product photos are loaded directly from Unsplash image URLs.
# No Unsplash API key, extra app, or manual photo download is required.
CATEGORY_DATA = {
    "Women": {
        "photo_tags": "women,fashion,clothing",
        "description": "Women's clothing, everyday essentials and occasion wear.",
        "category_image": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=900&q=85",
        "brands": ["Style Edit", "Tokyo Talkies", "SASSAFRAS", "DressBerry", "Anouk"],
        "items": ["Floral Dress", "Casual Top", "Straight Fit Jeans", "Printed Kurta", "Co-ord Set", "Maxi Dress", "Cotton Shirt", "Wide Leg Trousers", "Party Wear Gown", "Everyday T-shirt"],
        "images": [
            "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1551163943-3f6a855d1153?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1566206091558-7f218b696731?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=85",
        ],
        "adjectives": ["Classic", "Modern", "Printed", "Elegant", "Comfort", "Premium", "Everyday", "Trendy", "Festive", "Casual"],
        "base_price": 599,
        "description_text": "Designed for versatile styling and comfortable all-day wear. A wardrobe essential with an easy-to-style finish.",
    },
    "Men": {
        "photo_tags": "men,fashion,clothing",
        "description": "Men's casualwear, workwear and weekend essentials.",
        "category_image": "https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=900&q=85",
        "brands": ["Roadster", "HRX", "WROGN", "The Indian Garage Co", "HERE&NOW"],
        "items": ["Cotton Shirt", "Casual T-shirt", "Slim Fit Jeans", "Lightweight Jacket", "Polo T-shirt", "Formal Trousers", "Printed Shirt", "Hooded Sweatshirt", "Casual Shorts", "Everyday Kurta"],
        "images": [
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=85",
        ],
        "adjectives": ["Classic", "Slim Fit", "Urban", "Essential", "Premium", "Relaxed", "Textured", "Modern", "Weekend", "Smart"],
        "base_price": 699,
        "description_text": "A versatile men's style made for everyday comfort, easy layering and a clean contemporary look.",
    },
    "Kids": {
        "photo_tags": "kids,children,clothing",
        "description": "Comfortable, colourful clothing and everyday essentials for kids.",
        "category_image": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?auto=format&fit=crop&w=900&q=85",
        "brands": ["YK", " H&M Kids", "Mini Klub", "Pantaloons Junior", "United Colors of Benetton"],
        "items": ["Printed T-shirt", "Cotton Dress", "Denim Dungaree", "Casual Shorts", "Festive Kurta Set", "Leggings Set", "Hooded Sweatshirt", "Party Wear Dress", "Night Suit", "Polo T-shirt"],
        "images": [
            "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1503919005314-30d93d07d823?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1519457431-44ccd64a579b?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1516627145497-ae6968895b74?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?auto=format&fit=crop&w=800&q=85",
        ],
        "adjectives": ["Playful", "Colour Pop", "Everyday", "Soft Cotton", "Happy", "Comfy", "Little Star", "Fun Print", "Festive", "Easy Wear"],
        "base_price": 399,
        "description_text": "Made for movement, play and comfort with kid-friendly styling and an easy-care feel.",
    },
    "Footwear": {
        "photo_tags": "sneakers,shoes,footwear",
        "description": "Sneakers, casual shoes, sandals and everyday footwear.",
        "category_image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=85",
        "brands": ["Puma", "Campus", "Roadster", "HRX", "Red Tape"],
        "items": ["Everyday Sneakers", "Running Shoes", "Casual Slip-ons", "Classic Sandals", "Sports Shoes", "Canvas Shoes", "Walking Shoes", "Slides", "Casual Loafers", "Training Shoes"],
        "images": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1491553895911-0055eca6402d?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1460170779742-3f2f4e9f3b4a?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&w=800&q=85",
        ],
        "adjectives": ["Street Style", "Lightweight", "Active", "Classic", "Comfort", "Sport", "Urban", "Everyday", "Flex", "Essential"],
        "base_price": 899,
        "description_text": "Built for daily comfort and dependable wear, with a versatile design for work, travel and weekends.",
    },
    "Beauty": {
        "photo_tags": "beauty,skincare,cosmetics",
        "description": "Skincare, makeup, haircare and self-care favourites.",
        "category_image": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=900&q=85",
        "brands": ["Beauty Edit", "Minimalist", "The Face Shop", "Mamaearth", "Lakme"],
        "items": ["Hydrating Face Moisturizer", "Daily Face Cleanser", "Glow Serum", "Matte Lip Colour", "Sunscreen SPF 50", "Nourishing Hair Mask", "Body Lotion", " kajal Eyeliner", "Gentle Toner", "Daily Beauty Combo"],
        "images": [
            "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=800&q=85",
        ],
        "adjectives": ["Daily Care", "Hydra Boost", "Radiance", "Soft Matte", "Gentle", "Nourish", "Fresh Glow", "Essential", "Vitamin Care", "Premium"],
        "base_price": 249,
        "description_text": "A beauty and personal-care essential for a simple everyday routine. Check the product packaging for ingredients and usage instructions.",
    },
    "Home & Living": {
        "photo_tags": "home,interior,decor",
        "description": "Home decor, soft furnishings and thoughtful everyday essentials.",
        "category_image": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=900&q=85",
        "brands": ["Home Centre", "Story@Home", "Urban Space", "DDecor", "Home Edit"],
        "items": ["Decor Cushion Cover", "Cotton Bedsheet Set", "Ceramic Vase", "Table Runner", "Soft Throw Blanket", "Decorative Planter", "Bath Towel Set", "Wall Art Print", "Storage Basket", "Table Lamp"],
        "images": [
            "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1616486029423-aaa4789e8c9a?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=800&q=85",
        ],
        "adjectives": ["Minimal", "Soft Touch", "Natural", "Modern", "Classic", "Cozy", "Artisan", "Everyday", "Elegant", "Urban"],
        "base_price": 349,
        "description_text": "A practical home essential selected to add comfort, texture and a fresh look to your living space.",
    },
}


class Command(BaseCommand):
    help = "Create or update 50 demo products with descriptions and image URLs in every Myntra category."

    def handle(self, *args, **options):
        total_created = 0
        total_updated = 0

        for category_name, info in CATEGORY_DATA.items():
            category, _ = Category.objects.update_or_create(
                slug=slugify(category_name),
                defaults={
                    "name": category_name,
                    "description": info["description"],
                    "image_url": info["category_image"],
                    "is_active": True,
                },
            )

            for index in range(50):
                item_name = info["items"][index % len(info["items"])]
                adjective = info["adjectives"][index // len(info["items"])]
                product_name = f"{adjective} {item_name}"
                slug = f"{category.slug}-{slugify(product_name)}"
                price = Decimal(info["base_price"] + (index % 10) * 150 + (index // 10) * 75)
                original_price = (price * Decimal("1.25")).quantize(Decimal("1"))

                product, created = Product.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "category": category,
                        "name": product_name,
                        "brand": info["brands"][index % len(info["brands"])].strip(),
                        "description": (
                            f"{info['description_text']} "
                            f"Category: {category_name}. Style: {adjective}. "
                            f"Product type: {item_name}. "
                            "Please review the displayed product information before ordering."
                        ),
                        "price": price,
                        "original_price": original_price,
                        "image_url": info["images"][index % len(info["images"])],
                        "stock": 5 + (index % 46),
                        "available": True,
                    },
                )
                if created:
                    total_created += 1
                else:
                    total_updated += 1

            count = Product.objects.filter(category=category, available=True).count()
            self.stdout.write(f"{category_name}: {count} available products")

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {total_created} products and updated {total_updated}. "
                "Each of the 6 categories now has at least 50 seeded products."
            )
        )
