from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product

class Command(BaseCommand):
    help = "Create starter Myntra demo categories and products"

    def handle(self, *args, **options):
        data = {
            "Women": ("Women's fashion, everyday essentials and occasion wear.", "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=900&q=85"),
            "Men": ("Modern styles for work, weekends and every day.", "https://images.unsplash.com/photo-1516257984-b1b4d707412e?auto=format&fit=crop&w=900&q=85"),
            "Kids": ("Comfortable and colourful styles for little ones.", "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?auto=format&fit=crop&w=900&q=85"),
            "Footwear": ("Sneakers, casual shoes and everyday favourites.", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=85"),
            "Beauty": ("Skincare, beauty and self-care favourites.", "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=900&q=85"),
            "Home & Living": ("Thoughtful details to refresh your space.", "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=900&q=85"),
        }
        categories = {}
        for name, (description, image) in data.items():
            category, _ = Category.objects.update_or_create(slug=slugify(name), defaults={"name": name, "description": description, "image_url": image, "is_active": True})
            categories[name] = category
        products = [
            ("Women", "Everyday Floral Dress", "Style Edit", 1499, 20, "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=800&q=85"),
            ("Women", "Relaxed Fit Top", "Style Edit", 899, 25, "https://images.unsplash.com/photo-1551163943-3f6a855d1153?auto=format&fit=crop&w=800&q=85"),
            ("Men", "Casual Cotton Shirt", "Roadster Edit", 1199, 20, "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=85"),
            ("Men", "Weekend Jacket", "Style Edit", 2199, 12, "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=85"),
            ("Kids", "Kids Casual Outfit", "Tiny Tribe", 799, 30, "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?auto=format&fit=crop&w=800&q=85"),
            ("Footwear", "Classic Everyday Sneakers", "Campus Edit", 1299, 30, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=85"),
            ("Beauty", "Daily Glow Skincare Set", "Beauty Edit", 699, 40, "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=800&q=85"),
            ("Home & Living", "Soft Neutral Cushion", "Home Edit", 549, 35, "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=800&q=85"),
        ]
        for category_name, name, brand, price, stock, image in products:
            Product.objects.update_or_create(slug=slugify(name), defaults={"category": categories[category_name], "name": name, "brand": brand, "price": price, "original_price": int(price * 1.4), "stock": stock, "image_url": image, "available": True})
        self.stdout.write(self.style.SUCCESS("Starter categories and products created/updated."))
