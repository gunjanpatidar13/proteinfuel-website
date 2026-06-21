from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User
from apps.core.models import (
    SiteSettings, HomepageContent, WhyChooseItem, Testimonial,
    FAQ, StatCard, SocialLink, Job
)
from apps.catalog.models import Category, Product, NutritionalProfile
from apps.blogs.models import BlogCategory, BlogTag, BlogPost

class Command(BaseCommand):
    help = 'Seeds the database with default ProteinFuel contents and an admin account.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # 1. Create Admin Account
        admin_email = 'admin@proteinfuel.com'
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                password='adminpass',
                first_name='PF',
                last_name='Admin',
                phone_number='+91 99999 99999',
                user_type='ADMIN'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_email} (password: adminpass)'))
        else:
            self.stdout.write('Admin user already exists.')

        # 2. Initialize Site Settings
        settings = SiteSettings.load()
        settings.site_name = "ProteinFuel"
        settings.contact_email = "info@proteinfuel.com"
        settings.contact_phone = "+91 99999 99999"
        settings.contact_address = "HSR Layout, Sector 3, Bangalore, Karnataka - 560102"
        settings.footer_about = "ProteinFuel is a premium fitness-focused food brand re-engineering your favorite waffles, shakes, and coffees with clean proteins and high nutritional yields."
        settings.copyright_text = "© 2026 ProteinFuel. All rights reserved."
        settings.meta_title = "ProteinFuel - Fuel Your Day With Protein"
        settings.meta_description = "Order High Protein Waffles, Pancakes, Shakes & Cold Coffee Delivered Fresh. Clean ingredients, premium nutrition, zero junk."
        settings.save()
        self.stdout.write(self.style.SUCCESS('Site Settings initialized.'))

        # 3. Initialize Homepage Content
        home = HomepageContent.load()
        home.hero_headline = "Fuel Your Day With Protein"
        home.hero_subheadline = "High Protein Waffles, Shakes & Coffee Delivered Fresh to Your Doorstep."
        home.hero_button_text = "Explore Menu"
        home.hero_button_url = "/products/"
        home.why_choose_title = "Why Choose ProteinFuel"
        home.why_choose_subtitle = "We bridge the gap between clean gym nutrition and great-tasting snacks."
        home.nutrition_title = "Our Nutrition Philosophy"
        home.nutrition_content = "We believe protein shouldn't be limited to chalky shakes and powders. Our kitchen re-engineers daily classics—waffles, pancakes, and cold brew coffees—using high-quality whey isolates, oat flour, and zero refined sugars. You get restaurant-grade flavor packed with the precise macros your body needs for recovery and performance."
        home.cta_title = "Start Your Protein Journey Today"
        home.cta_subtitle = "Fuel your gains with our high protein menu items. Clean ingredients, great taste."
        home.cta_button_text = "Order Now"
        home.cta_button_url = "/products/"
        home.save()
        self.stdout.write(self.style.SUCCESS('Homepage Content initialized.'))

        # 4. Create Why Choose Cards
        why_cards = [
            ("High Protein", "Every serving packs 20g-30g of premium whey or plant protein isolates.", "lightning-charge-fill"),
            ("Great Taste", "Extensively tested recipes ensuring zero chalky texture or aftertaste.", "emoji-smile-fill"),
            ("No Junk", "Zero refined sugars, zero seed oils, and no artificial preservatives.", "shield-x"),
            ("Freshly Prepared", "Cooked-to-order in our sanitised home cloud kitchen hubs.", "fire"),
            ("Fitness Focused", "Clear macro breakdowns (Protein, Carbs, Fats, Kcal) for every item.", "activity"),
            ("Quality Ingredients", "Made with organic oats, almond milk, and natural fruit purees.", "egg-fill"),
        ]
        for idx, (title, desc, icon) in enumerate(why_cards):
            card, created = WhyChooseItem.objects.get_or_create(
                title=title,
                defaults={'description': desc, 'icon_name': icon, 'display_order': idx}
            )
            if created:
                self.stdout.write(f'Created WhyChoose card: {title}')

        # 5. Create Statistics
        stats = [
            ("10,000+", "Healthy Meals Served"),
            ("5,000+", "Happy Customers"),
            ("50+", "Fitness Partnerships"),
        ]
        for idx, (val, lbl) in enumerate(stats):
            stat, created = StatCard.objects.get_or_create(
                label=lbl,
                defaults={'value': val, 'display_order': idx}
            )
            if created:
                self.stdout.write(f'Created StatCard: {lbl}')

        # 6. Create FAQs
        faqs = [
            ("What type of protein do you use in your products?", "We use ultra-filtered whey protein isolate for dairy-based items and high-grade organic pea/brown rice protein isolate for vegan alternatives."),
            ("Are your waffles gluten-free?", "Yes! Our waffles are prepared using a blend of gluten-free oat flour and almond flour instead of refined white wheat flour (maida)."),
            ("How do you sweeten your products if you don't use sugar?", "We use natural sweeteners like Stevia extract and high-purity Erythritol, which have zero glycemic index and won't spike your insulin."),
            ("Where can I find the precise macro breakdown for my meal?", "Every item listed on our menu displays the exact protein, fat, carb, and calorie breakdown both on our website and printed on our packaging."),
            ("Do you deliver to my gym or office?", "Yes, we dispatch order shipments via Swiggy and Zomato, covering a wide radius across Bangalore. Simply select us on the apps!"),
        ]
        for idx, (q, a) in enumerate(faqs):
            faq, created = FAQ.objects.get_or_create(
                question=q,
                defaults={'answer': a, 'display_order': idx}
            )
            if created:
                self.stdout.write(f'Created FAQ: {q[:30]}...')

        # 7. Create Social Links
        socials = [
            ("Instagram", "https://instagram.com/proteinfuel", "instagram"),
            ("Facebook", "https://facebook.com/proteinfuel", "facebook"),
            ("Twitter", "https://twitter.com/proteinfuel", "twitter"),
        ]
        for idx, (plat, url, icon) in enumerate(socials):
            link, created = SocialLink.objects.get_or_create(
                platform_name=plat,
                defaults={'url': url, 'icon_name': icon, 'display_order': idx}
            )
            if created:
                self.stdout.write(f'Created Social Link: {plat}')

        # 8. Create Product Categories
        categories = [
            "Protein Waffles",
            "Protein Cold Coffee",
            "Protein Shakes",
            "High Protein Smoothies",
            "Protein Pancakes",
            "Seasonal Protein Specials"
        ]
        cat_objects = {}
        for idx, name in enumerate(categories):
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'display_order': idx, 'description': f"Delicious high protein selections in {name}."}
            )
            cat_objects[name] = cat
            if created:
                self.stdout.write(f'Created Category: {name}')

        # 9. Create Products & Nutrition Profiles
        products_data = [
            {
                "category": "Protein Waffles",
                "name": "Double Chocolate Whey Waffle",
                "desc": "Freshly baked waffle enriched with whey isolate, cocoa powder, topped with sugar-free dark chocolate drizzle.",
                "protein": 24, "calories": 320, "price": 199.00, "is_featured": True,
                "carbs": 28, "fats": 8, "fiber": 4,
                "ingredients": "Whey Protein Isolate, Gluten-Free Oat Flour, Egg Whites, Organic Cocoa Powder, Stevia, Almond Milk.",
                "allergen": "Contains Dairy (Whey), Eggs."
            },
            {
                "category": "Protein Waffles",
                "name": "Peanut Butter Crunch Waffle",
                "desc": "High-protein waffle spread with organic sugar-free creamy peanut butter and roasted almond flakes.",
                "protein": 26, "calories": 380, "price": 219.00, "is_featured": True,
                "carbs": 24, "fats": 14, "fiber": 5,
                "ingredients": "Whey Protein, Oat Flour, Organic Peanut Butter, Eggs, Stevia, Roasted Almonds.",
                "allergen": "Contains Peanuts, Nuts, Eggs, Dairy."
            },
            {
                "category": "Protein Cold Coffee",
                "name": "Espresso Protein Cold Brew",
                "desc": "Double shot espresso blended with chilled skimmed milk, erythritol, and vanilla whey isolate.",
                "protein": 20, "calories": 160, "price": 149.00, "is_featured": True,
                "carbs": 12, "fats": 2, "fiber": 0,
                "ingredients": "Arabica Espresso Coffee, Whey Protein Isolate, Skimmed Milk, Erythritol.",
                "allergen": "Contains Dairy."
            },
            {
                "category": "Protein Shakes",
                "name": "Classic Strawberry Whey Shake",
                "desc": "Thick premium shake made with frozen strawberries, whey isolate, and natural greek yogurt.",
                "protein": 25, "calories": 210, "price": 169.00, "is_featured": True,
                "carbs": 18, "fats": 3, "fiber": 3,
                "ingredients": "Strawberries, Whey Isolate, Low-Fat Greek Yogurt, Almond Milk, Stevia.",
                "allergen": "Contains Dairy."
            },
            {
                "category": "Protein Pancakes",
                "name": "Blueberry Oat Pancakes",
                "desc": "Fluffy oat pancakes packed with fresh local blueberries and served with sugar-free maple syrup.",
                "protein": 22, "calories": 290, "price": 189.00, "is_featured": False,
                "carbs": 38, "fats": 4, "fiber": 6,
                "ingredients": "Gluten-Free Oats, Blueberries, Egg Whites, Plant Protein Isolate, Sugar-free Maple syrup.",
                "allergen": "Contains Eggs."
            },
        ]
        for item in products_data:
            cat_obj = cat_objects[item["category"]]
            product, created = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    'category': cat_obj,
                    'description': item["desc"],
                    'protein_grams': item["protein"],
                    'calories': item["calories"],
                    'price': item["price"],
                    'is_featured': item["is_featured"]
                }
            )
            
            if created:
                NutritionalProfile.objects.create(
                    product=product,
                    calories=item["calories"],
                    protein_grams=item["protein"],
                    carbs_grams=item["carbs"],
                    fats_grams=item["fats"],
                    fiber_grams=item["fiber"],
                    ingredients=item["ingredients"],
                    allergen_info=item["allergen"]
                )
                self.stdout.write(f'Created Product & Nutrition: {item["name"]}')

        # 10. Create Testimonials
        reviews = [
            ("Rohan Sharma", 5, "I order the Double Chocolate Waffle almost every post-workout. Hits my macros perfectly and tastes incredible!"),
            ("Anjali Sen", 5, "As a busy working professional, finding low-sugar breakfast shakes is hard. The Espresso Cold Brew is my daily go-to."),
            ("Vikram Malhotra", 4, "Quality ingredients and accurate nutritional figures. Great to see a local cloud kitchen focus on fitness macros."),
        ]
        for name, rating, text in reviews:
            Testimonial.objects.get_or_create(
                customer_name=name,
                defaults={'rating': rating, 'review_text': text}
            )

        # 11. Create Blog Data
        blog_cat, _ = BlogCategory.objects.get_or_create(name="Nutrition")
        blog_tag, _ = BlogTag.objects.get_or_create(name="MuscleBuilding")
        
        post, post_created = BlogPost.objects.get_or_create(
            title="The Power of Protein in Muscle Recovery",
            defaults={
                'category': blog_cat,
                'content': "<p>Protein is the cornerstone of athletic performance and physical recovery. When we perform resistance workouts, micro-tears are created in muscle tissues. Dietary protein is broken down into amino acids, which serve as building blocks to synthesize and patch these micro-tears, making the muscle stronger and denser.</p><p>Hitting your daily target (ideally 1.6g to 2.2g per kg of bodyweight) is crucial for gains. Snacking on high-protein waffles and shakes can make reaching this goal simple and tasty.</p>",
                'status': 'PUBLISHED',
                'published_at': timezone.now(),
                'meta_title': "Why Protein is Vital for Muscle Recovery",
                'meta_description': "Learn how protein isolates patch muscle micro-tears and accelerate recovery times post-workout."
            }
        )
        if post_created:
            post.tags.add(blog_tag)
            self.stdout.write('Created Blog Post: The Power of Protein...')

        # 12. Create Jobs
        Job.objects.get_or_create(
            position="Kitchen Manager - Cloud Kitchen",
            defaults={
                'location': "HSR Layout, Bangalore",
                'description': "<p>We are looking for an experienced Kitchen Manager to run day-to-day cloud kitchen prep, manage inventory, coordinate with Swiggy/Zomato dispatch agents, and enforce hygiene standards.</p><ul><li>Min 2 years kitchen experience.</li><li>Familiar with inventory management tools.</li><li>Familiar with fitness recipes is a plus.</li></ul>",
                'status': 'ACTIVE'
            }
        )
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
