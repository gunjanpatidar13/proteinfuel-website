from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, CreateView, ListView, View
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from apps.core.models import (
    HomepageContent, WhyChooseItem, Testimonial, GalleryItem, FAQ,
    ContactInquiry, FranchiseApplication, Job, JobApplication,
    StatCard, SiteSettings, NewsletterSubscriber
)
from apps.catalog.models import Product
from apps.core.forms import ContactForm, FranchiseForm, JobApplicationForm

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepage'] = HomepageContent.load()
        context['featured_products'] = Product.objects.filter(is_featured=True, is_active=True)[:6]
        context['why_choose_items'] = WhyChooseItem.objects.filter(is_active=True)[:6]
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:3]
        context['stat_cards'] = StatCard.objects.filter(is_active=True)[:4]
        context['faqs'] = FAQ.objects.filter(is_active=True)[:5]
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepage'] = HomepageContent.load()
        return context


class WhyChooseView(TemplateView):
    template_name = 'core/why_choose.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['why_choose_items'] = WhyChooseItem.objects.filter(is_active=True)
        return context


class PhilosophyView(TemplateView):
    template_name = 'core/philosophy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homepage'] = HomepageContent.load()
        return context


class GalleryView(TemplateView):
    template_name = 'core/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_items'] = GalleryItem.objects.filter(is_active=True)
        return context


class TestimonialsListView(ListView):
    model = Testimonial
    template_name = 'core/testimonials.html'
    context_object_name = 'testimonials'
    paginate_by = 9

    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True)


class FAQListView(TemplateView):
    template_name = 'core/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True)
        return context


class ContactCreateView(CreateView):
    model = ContactInquiry
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = '/contact/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you for reaching out! We will contact you shortly.")
        return super().form_valid(form)


class FranchiseCreateView(CreateView):
    model = FranchiseApplication
    form_class = FranchiseForm
    template_name = 'core/franchise.html'
    success_url = '/franchise/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your application has been submitted successfully. Our team will review and get in touch.")
        return super().form_valid(form)


class CareersListView(TemplateView):
    template_name = 'core/careers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.filter(status='ACTIVE')
        return context


class JobApplyView(CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'core/job_apply.html'
    success_url = '/careers/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['job_id'], status='ACTIVE')
        return context

    def form_valid(self, form):
        job = get_object_or_404(Job, pk=self.kwargs['job_id'], status='ACTIVE')
        form.instance.job = job
        form.save()
        messages.success(self.request, f"Your application for {job.position} has been submitted successfully!")
        return super().form_valid(form)


class NewsletterSubscribeView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '').strip()
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address.'}, status=400)
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created:
            if not subscriber.is_active:
                subscriber.is_active = True
                subscriber.save()
                return JsonResponse({'status': 'success', 'message': 'Subscribed successfully!'})
            return JsonResponse({'status': 'info', 'message': 'You are already subscribed.'})
        
        return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing!'})


def robots_txt(request):
    settings = SiteSettings.load()
    content = settings.robots_txt or "User-agent: *\nAllow: /"
    return HttpResponse(content, content_type="text/plain")


def sitemap_xml(request):
    settings = SiteSettings.load()
    if settings.sitemap_xml:
        return HttpResponse(settings.sitemap_xml, content_type="application/xml")
    
    # Simple fallback sitemap generation
    domain = request.build_absolute_uri('/')[:-1]
    urls = [
        '',
        '/about/',
        '/products/',
        '/why-choose/',
        '/philosophy/',
        '/gallery/',
        '/testimonials/',
        '/faq/',
        '/contact/',
        '/franchise/',
        '/careers/',
        '/blog/'
    ]
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url in urls:
        xml_lines.append(f'  <url><loc>{domain}{url}</loc><changefreq>weekly</changefreq></url>')
    
    # Add products
    for product in Product.objects.filter(is_active=True):
        xml_lines.append(f'  <url><loc>{domain}/products/{product.slug}/</loc><changefreq>weekly</changefreq></url>')
        
    xml_lines.append('</urlset>')
    return HttpResponse("\n".join(xml_lines), content_type="application/xml")


def error_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def error_500_view(request):
    return render(request, '500.html', status=500)
