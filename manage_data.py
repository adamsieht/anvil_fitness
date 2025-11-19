#!/usr/bin/env python
"""
Sample data creation script for Anvil Fitness website
Run this with: python manage_data.py
"""

import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anvil_fitness.settings')
django.setup()

from fitness.models import Service, Testimonial, FitnessTip

def create_sample_data():
    """Create sample data for the Anvil Fitness website"""
    
    # Create Services
    services_data = [
        {
            'name': 'Personal Training',
            'description': 'One-on-one customized training sessions designed specifically for adults 40+. Focus on functional movements, strength building, and injury prevention with programs that fit your lifestyle and schedule.',
            'icon': 'fas fa-dumbbell',
            'is_featured': True
        },
        {
            'name': 'Functional Fitness',
            'description': 'Movement patterns that translate to real-life activities. Improve your daily functional capacity with exercises that enhance balance, coordination, and core stability while building practical strength.',
            'icon': 'fas fa-running',
            'is_featured': True
        },
        {
            'name': 'Strength & Conditioning',
            'description': 'Build lean muscle mass, increase bone density, and boost metabolism with progressive resistance training. Joint-friendly modifications ensure safety while maximizing results.',
            'icon': 'fas fa-weight-hanging',
            'is_featured': True
        },
        {
            'name': 'Mobility & Recovery',
            'description': 'Specialized programs to improve flexibility, reduce joint pain, and enhance recovery. Essential for maintaining an active lifestyle and preventing injuries as we age.',
            'icon': 'fas fa-leaf',
            'is_featured': False
        },
        {
            'name': 'Cardiovascular Health',
            'description': 'Heart-healthy exercise programs that build endurance without burnout. Low-impact cardio options and interval training protocols designed for optimal cardiovascular health.',
            'icon': 'fas fa-heartbeat',
            'is_featured': False
        },
        {
            'name': 'Nutrition Guidance',
            'description': 'Practical nutrition advice tailored for adults 40+. Focus on sustainable eating habits that support your fitness goals, energy levels, and overall health.',
            'icon': 'fas fa-apple-alt',
            'is_featured': False
        }
    ]
    
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            print(f"Created service: {service.name}")
    
    # Create Testimonials
    testimonials_data = [
        {
            'name': 'Sarah M.',
            'age': 45,
            'content': 'I never thought I could feel this strong and confident at 45! The personalized approach really made the difference. My trainer understood my busy schedule and created workouts that actually fit my life. Six months later, I\'m stronger than I was in my 30s!',
            'is_featured': True
        },
        {
            'name': 'Robert K.',
            'age': 52,
            'content': 'After years of on-and-off gym memberships, I finally found an approach that works. The focus on functional fitness has helped me with everything from playing with my grandkids to feeling confident on hiking trails. Highly recommend!',
            'is_featured': True
        },
        {
            'name': 'Jennifer L.',
            'age': 48,
            'content': 'The best investment I\'ve made in my health. The training is challenging but never overwhelming, and the constant support keeps me motivated. I love that I can use my existing fitness app while getting expert guidance.',
            'is_featured': True
        },
        {
            'name': 'Michael T.',
            'age': 41,
            'content': 'As a busy executive, I needed efficiency in my workouts. The programs are perfectly designed to maximize results in minimal time. I\'ve gained muscle, lost fat, and feel more energetic than I have in years.',
            'is_featured': False
        },
        {
            'name': 'Lisa P.',
            'age': 55,
            'content': 'I was hesitant to start fitness training at my age, but the supportive approach made all the difference. Every workout is adapted to my needs, and I never feel judged or rushed. It\'s been transformational.',
            'is_featured': False
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial, created = Testimonial.objects.get_or_create(
            name=testimonial_data['name'],
            defaults=testimonial_data
        )
        if created:
            print(f"Created testimonial: {testimonial.name}")
    
    # Create Fitness Tips
    tips_data = [
        {
            'title': 'Start with Compound Movements for Maximum Results',
            'content': '''When you're short on time but want maximum results, compound movements are your best friend. These exercises work multiple muscle groups simultaneously, giving you incredible bang for your buck.

Focus on these fundamental movements:
• Squats (bodyweight or weighted)
• Deadlifts (can start with light weights)
• Push-ups (modify as needed)
• Pull-ups or rows
• Overhead presses

These exercises not only build strength but also improve coordination, balance, and functional movement patterns that translate to everyday activities.

For adults over 40, compound movements are especially beneficial because they:
- Maximize time efficiency
- Build functional strength
- Improve bone density
- Enhance metabolic rate
- Reduce injury risk through integrated movement patterns

Start with 2-3 compound movements per workout, focusing on proper form over heavy weights. As you build strength and confidence, you can add complexity and resistance.

Remember: it's not about lifting the heaviest weights in the gym. It's about consistent, progressive improvement that enhances your daily life.''',
            'category': 'exercise',
            'is_featured': True
        },
        {
            'title': 'The Protein Priority: Why 40+ Adults Need More',
            'content': '''As we age, our bodies become less efficient at building and maintaining muscle mass. This is where adequate protein intake becomes crucial for adults over 40.

The research is clear: adults over 40 should aim for 1.2-1.6 grams of protein per kilogram of body weight daily. For a 150-pound person, that's about 80-110 grams of protein per day.

Why protein matters more after 40:
• Muscle mass naturally declines 3-8% per decade after 30
• Protein synthesis becomes less efficient
• Recovery from exercise takes longer
• Metabolic rate can slow down

Practical protein strategies:
- Include 20-30g protein at each meal
- Choose high-quality sources: lean meats, fish, eggs, dairy, legumes
- Consider protein timing around workouts
- Don't forget plant-based options like quinoa and hemp seeds

Easy protein additions:
• Greek yogurt with breakfast
• Hard-boiled eggs as snacks
• Protein powder in smoothies
• Nuts and seeds throughout the day

Remember: you don't need to overhaul your entire diet overnight. Start by adding one quality protein source to each meal and build from there.''',
            'category': 'nutrition',
            'is_featured': True
        },
        {
            'title': 'Sleep: The Underrated Recovery Tool',
            'content': '''Quality sleep isn't just about feeling rested – it's a critical component of your fitness and health strategy, especially after 40.

During sleep, your body:
- Repairs and rebuilds muscle tissue
- Balances hormones (including growth hormone and cortisol)
- Consolidates memories and motor skills
- Regulates appetite hormones (leptin and ghrelin)

For adults over 40, sleep becomes even more important because:
• Recovery takes longer than it used to
• Hormone production naturally changes
• Stress levels often increase with life responsibilities
• Sleep quality often declines with age

Sleep optimization strategies:
1. Maintain consistent bedtime and wake times (even on weekends)
2. Create a cool, dark, quiet sleeping environment
3. Limit screens 1-2 hours before bed
4. Avoid caffeine after 2 PM
5. Keep your bedroom temperature around 65-68°F

Evening routine ideas:
- Light stretching or gentle yoga
- Reading (physical books, not screens)
- Meditation or deep breathing
- Warm bath with Epsom salts
- Journaling about the day

If you're not sleeping well, address it with the same priority you give your workouts. Your body repairs and grows stronger during sleep – don't shortchange this crucial process.''',
            'category': 'wellness',
            'is_featured': False
        },
        {
            'title': 'Progress Over Perfection: The Sustainable Mindset',
            'content': '''The fitness industry loves to sell "perfect" – perfect diets, perfect workout plans, perfect transformations. But here's the truth: perfection is the enemy of progress, especially for busy adults over 40.

Your life is complex. You have work deadlines, family responsibilities, social commitments, and unexpected challenges. The goal isn't to live like a fitness influencer – it's to build sustainable habits that enhance your real life.

The 80/20 approach:
• 80% of your results come from consistent, imperfect action
• 20% might come from perfect execution (which rarely happens)

Practical examples:
- A 20-minute walk is infinitely better than a skipped 60-minute gym session
- A protein-rich breakfast beats no breakfast, even if it's not "perfect"
- Two workouts per week consistently beats sporadic intense weeks

Building momentum:
1. Start ridiculously small (even 5-minute workouts count)
2. Focus on consistency over intensity
3. Celebrate small wins daily
4. Don't restart on Monday – restart right now
5. Adjust expectations based on life seasons

Remember: The person who exercises twice a week for 10 years will be far healthier than someone who does perfect workouts for 10 weeks then quits.

Your goal is progress, not perfection. Every small action compounds over time.''',
            'category': 'motivation',
            'is_featured': False
        },
        {
            'title': 'Listen to Your Body: Recovery Wisdom After 40',
            'content': '''When we're younger, we can often push through fatigue and recover quickly. After 40, wisdom means learning to listen to your body's signals and responding appropriately.

This isn't about making excuses – it's about training smarter, not just harder.

Signs you might need extra recovery:
• Persistent muscle soreness lasting more than 48 hours
• Decreased performance despite consistent effort
• Trouble sleeping or feeling unrested
• Increased irritability or mood changes
• Higher resting heart rate than normal
• Frequent minor injuries or aches

Recovery strategies:
1. Active recovery days (light walking, gentle yoga, swimming)
2. Prioritize sleep (7-9 hours nightly)
3. Stay hydrated throughout the day
4. Include anti-inflammatory foods in your diet
5. Consider massage or foam rolling
6. Manage stress through meditation or relaxation techniques

The difference between soreness and pain:
- Soreness: Dull ache, improves with movement, peaks 24-48 hours after exercise
- Pain: Sharp, doesn't improve with movement, may worsen over time

When to take a full rest day:
• When you feel genuinely exhausted (not just lazy)
• When minor aches become persistent
• When you've had several high-intensity days in a row
• When life stress is particularly high

Remember: Recovery is when your body actually gets stronger. Don't see rest days as lost opportunities – see them as investments in your long-term success.''',
            'category': 'wellness',
            'is_featured': False
        },
        {
            'title': 'Hydration: More Important Than Ever After 40',
            'content': '''As we age, our sense of thirst diminishes, kidney function changes, and our body's water content naturally decreases. This makes proper hydration more critical – and more challenging – for adults over 40.

Why hydration matters more after 40:
• Decreased kidney efficiency in concentrating urine
• Reduced total body water content (from ~60% to ~50%)
• Diminished thirst sensation
• Medications may affect fluid balance
• Hot flashes and hormonal changes can increase fluid loss

Signs of mild dehydration:
- Fatigue and decreased energy
- Headaches
- Difficulty concentrating
- Constipation
- Dark yellow urine
- Dry skin and mouth

Hydration strategies:
1. Start your day with 16-20 oz of water
2. Keep water visible throughout the day
3. Set phone reminders to drink water
4. Eat water-rich foods (fruits and vegetables)
5. Monitor urine color (aim for pale yellow)
6. Drink before, during, and after exercise

How much water do you need?
A general guideline is half your body weight in ounces. So if you weigh 160 pounds, aim for about 80 ounces (10 cups) daily. Increase this with exercise, heat, or illness.

Hydration helpers:
• Herbal teas count toward fluid intake
• Coconut water provides natural electrolytes
• Water-rich foods like cucumber, watermelon, and soup help
• Limit alcohol and excessive caffeine, which can dehydrate

Make it easier: Use a marked water bottle, keep water by your bedside, and flavor plain water with lemon, cucumber, or mint if needed.

Your body's ability to perform – in workouts and in life – depends heavily on proper hydration. Don't wait until you're thirsty to drink up.''',
            'category': 'wellness',
            'is_featured': False
        }
    ]
    
    for tip_data in tips_data:
        tip, created = FitnessTip.objects.get_or_create(
            title=tip_data['title'],
            defaults=tip_data
        )
        if created:
            print(f"Created fitness tip: {tip.title}")

    print("\nSample data creation complete!")
    print(f"Created {Service.objects.count()} services")
    print(f"Created {Testimonial.objects.count()} testimonials")
    print(f"Created {FitnessTip.objects.count()} fitness tips")

if __name__ == '__main__':
    create_sample_data()