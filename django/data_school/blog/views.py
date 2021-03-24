from django.shortcuts import render


posts = [
    {
        'author': 'Pushkin',
        'title': 'Captains daughter',
        'content': 'Really long story',
        'date_posted': 'August 28, 1800',
    },
    {
        'author': 'Tolstoy',
        'title': 'War and peace',
        'content': 'Really really long story',
        'date_posted': 'September 23, 1850',
    }
    
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)
    

def about(request):
    return render(request, 'blog/about.html')