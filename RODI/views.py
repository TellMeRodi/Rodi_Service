from django.shortcuts import redirect


# Create your views here.
def main(request):
    return redirect('Researches:home')