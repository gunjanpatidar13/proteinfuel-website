from django.urls import path
from apps.core.views import (
    HomeView, AboutView, WhyChooseView, PhilosophyView, GalleryView,
    TestimonialsListView, FAQListView, ContactCreateView, FranchiseCreateView,
    CareersListView, JobApplyView, NewsletterSubscribeView, robots_txt, sitemap_xml,
    error_404_view, error_500_view
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('why-choose/', WhyChooseView.as_view(), name='why_choose'),
    path('philosophy/', PhilosophyView.as_view(), name='philosophy'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('testimonials/', TestimonialsListView.as_view(), name='testimonials'),
    path('faq/', FAQListView.as_view(), name='faq'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('franchise/', FranchiseCreateView.as_view(), name='franchise'),
    path('careers/', CareersListView.as_view(), name='careers'),
    path('careers/<int:job_id>/apply/', JobApplyView.as_view(), name='job_apply'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    path('404/', error_404_view, name='test_404'),
    path('500/', error_500_view, name='test_500'),
]
