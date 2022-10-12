from django.shortcuts import render
from django.views import generic
from .models import Author, Book, BookInstance, Genre, Language
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()


    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.all().count()
    num_genre = Genre.objects.all().count()
    num_books_power = Book.objects.filter(title__icontains ='Power').count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_books_power': num_books_power,
        'num_visits': num_visits,
    }


    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):

    model = Book
    paginate_by: 10

    def get_queryset(self):
        return Book.objects.filter(title__icontains='rich')[:5]

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        context['some_data']= 'This is just some data'
        return context


class BookDetailView(generic.DetailView):

    model = Book


class AuthorListView(generic.ListView):

    model = Author

    def get_queryset(self):
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)

        context['some_data']= 'This is just some data'
        return context
    
class AuthorDetailView(generic.DetailView):

    model = Author


class LoanedBookByUserListView (LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10


    def get_query(self):
        return
BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')