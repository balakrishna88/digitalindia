from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponseRedirect

from categories.models import Contact
from django.contrib import messages



def contact_form(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Create a new Contact object and save it to the database
        contact = Contact.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            message=message
        )

        # Display success message
        messages.success(request, 'Your message has been successfully sent!')

        # Redirect the user to the contact URL
        return redirect('contact')  # assuming 'contact' is the name of your contact page URL

    return render(request, 'contact.html')  # specify the template name 'contact.html'



