from operator import truediv
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.messages import get_messages


from .models import *

# Create your views here.

def userPosted(user, reviews):
	reviewsList = list(reviews)
	for review in reviewsList:
		if review.user_id == user.id:
			return True
	return False

def details_view(request, productId):
	if request.method == 'POST':
		current_user = request.user
		review = request.POST['reviewtext']

		product = get_object_or_404(Watch, pk = productId)
		reviews = Review.objects.filter(product_id = productId)
		context = {'product': product,
		'reviews': reviews}

		if len(review) < 10:
			messages.error(request, 'Review is too short')
		if userPosted(current_user, reviews):
			messages.error(request, 'You have already posted a review')


		poruke = get_messages(request)
		if len(poruke) != 0:
			return render(request, 'watch/details.html', context)
		else:
			Review.objects.create(user = current_user, reviewText= review, product_id = productId)
			return render(request, 'watch/details.html', context)

	else:
		product = get_object_or_404(Watch, pk = productId)
		reviews = Review.objects.filter(product_id = productId)
		context = {'product': product,
		'reviews': reviews}
		return render(request, 'watch/details.html', context)