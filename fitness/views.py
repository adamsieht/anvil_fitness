from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Service, Testimonial, FitnessTip

def home(request):
    featured_services = Service.objects.filter(is_featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    featured_tips = FitnessTip.objects.filter(is_featured=True)[:2]
    
    context = {
        'featured_services': featured_services,
        'testimonials': testimonials,
        'featured_tips': featured_tips,
    }
    return render(request, 'fitness/home.html', context)

def about(request):
    return render(request, 'fitness/about.html')

def services(request):
    all_services = Service.objects.all()
    context = {'services': all_services}
    return render(request, 'fitness/services.html', context)

def contact(request):
    return render(request, 'fitness/contact.html')

class FitnessTipListView(ListView):
    model = FitnessTip
    template_name = 'fitness/tips.html'
    context_object_name = 'tips'
    paginate_by = 6
    ordering = ['-created_at']

def tip_detail(request, pk):
    tip = get_object_or_404(FitnessTip, pk=pk)
    related_tips = FitnessTip.objects.filter(category=tip.category).exclude(pk=pk)[:3]
    context = {
        'tip': tip,
        'related_tips': related_tips,
    }
    return render(request, 'fitness/tip_detail.html', context)
