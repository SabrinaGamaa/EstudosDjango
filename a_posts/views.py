from django.shortcuts import render

def home_view(request):
    print("-=" * 20)
    print('Request Method: ', request.method)
    if request.method == 'POST':
        print('Bye bye')
    return render(request, 'a_posts/home.html')


 