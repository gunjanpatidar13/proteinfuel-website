from django.test import TestCase
from django.urls import reverse
from apps.catalog.models import Category, Product
from apps.core.models import SiteSettings, HomepageContent

class ProteinFuelWebTests(TestCase):
    
    def setUp(self):
        # Initialize default configurations
        self.settings = SiteSettings.load()
        self.homepage = HomepageContent.load()
        
        # Create category & products for catalog views
        self.category = Category.objects.create(name="Shakes", description="Test Category")
        self.product = Product.objects.create(
            category=self.category,
            name="Vanilla Shake",
            description="Test Product",
            protein_grams=25,
            calories=200,
            price=150.00,
            is_active=True
        )

    def test_homepage_resolves_and_renders(self):
        url = reverse('core:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_about_page_resolves_and_renders(self):
        url = reverse('core:about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')

    def test_philosophy_page_resolves_and_renders(self):
        url = reverse('core:philosophy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/philosophy.html')

    def test_catalog_resolves_and_renders(self):
        url = reverse('catalog:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_list.html')
        self.assertContains(response, "Vanilla Shake")

    def test_product_detail_resolves_and_renders(self):
        url = reverse('catalog:product_detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_detail.html')
        self.assertContains(response, "Vanilla Shake")

    def test_blog_listing_resolves_and_renders(self):
        url = reverse('blogs:post_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/post_list.html')

    def test_robots_txt_resolves_and_renders(self):
        url = reverse('core:robots_txt')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "text/plain")

    def test_sitemap_xml_resolves_and_renders(self):
        url = reverse('core:sitemap_xml')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/xml")

    def test_custom_404_resolves_and_renders(self):
        response = self.client.get('/asdasd/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
