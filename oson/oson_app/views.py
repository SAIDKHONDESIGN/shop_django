from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import UpdateView

from . import models
from .forms import CommentForm, LoginForm, ProductForm, RegistrationForm

# Create your views here.


def home_page(request):
    sliders = models.Slider.objects.all()
    products = models.Products.objects.all()
    context = {"sliders": sliders, "products": products}
    return render(request, "pages/index.html", context)


def category_page(request, pk):
    sort_query = request.GET.get("sort")
    category = models.Category.objects.get(pk=pk)
    products = models.Products.objects.filter(category=category)

    if sort_query:
        products = products.order_by(sort_query)

    context = {"category": category, "products": products}
    return render(request, "pages/category.html", context)


def products_page(request):
    categories = models.Category.objects.all()
    products = models.Products.objects.all()
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, "pages/products.html", context)


def products_detail_page(request, pk):
    product = models.Products.objects.get(pk=pk)
    gallery = models.ProductsGallery.objects.filter(product=product)
    print(dir(request))
    print(request.environ)
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.product = product
            form.save()
            return redirect("products_detail", pk=product.pk)
    else:
        form = CommentForm()
    comments = models.Comment.objects.filter(product=product)

    if not request.session.session_key:
        request.session.save()

    session_key = request.session.session_key

    product_viewed = models.ProductsViews.objects.filter(
        products=product, session_id=session_key
    ).count()
    if product_viewed == 0 and session_key != "None":
        obj = models.ProductsViews(products=product, session_id=session_key)
        obj.save()

        product.views += 1
        product.save()

    context = {
        "product": product,
        "gallery": gallery,
        "form": form,
        "comments": comments,
    }
    return render(request, "pages/products_detail.html", context)


def login_page(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    context = {"form": form}
    return render(request, "pages/login.html", context)


def registration_page(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "pages/registration.html", context)


def logout_page(request):
    logout(request)
    return redirect("home")


def create_product_view(request):
    if request.method == "POST":
        print(request.POST, request.FILES)
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()

            for item in request.FILES.getlist("image"):
                new_obj = models.ProductsGallery(product=form, image=item)
                new_obj.save()
            return redirect("products_detail", pk=form.pk)
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "pages/article_form.html", context)


class ProductUpdateView(UpdateView):
    model = models.Products
    success_url = "/"
    form_class = ProductForm
    template_name = "pages/article_form.html"

    def post(self, request, pk):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            images = request.FILES.getlist("image")
            for img in images:
                models.ProductsGallery.objects.create(product=self.object, image=img)
            return self.form_valid(form)


def delete_product(request, pk):
    product = models.Products.objects.get(pk=pk)
    product.delete()
    return redirect("home")


def search(request):
    query = request.GET.get("q")
    products = []
    if query:
        products = models.Products.objects.filter(name__icontains=query)

    context = {"products": products, "query": query}
    return render(request, "pages/search_page.html", context)


@login_required(login_url="/login/")
def profile_page(request):
    profile = models.Profile.objects.filter(user=request.user)
    message = None
    if not profile:
        message = "Пока что вас админ не добавил в систему."
    context = {"message": message}
    return render(request, "pages/profile.html", context)


def profile_edit_view(request, profile_id):
    profile = models.Profile.objects.get(pk=profile_id)
    if request.method == "POST":
        data = request.POST
        avatar_image = request.FILES.get("avatar")
        user = User.objects.get(pk=data["user_id"])
        user.username = data["username"]
        user.save()
        profile.bio = data["bio"]
        if avatar_image is not None:
            profile.avatar = avatar_image
        profile.save()
        return redirect("profile")

    return render(
        request,
        "pages/profile_edit.html",
    )


def basket_page(request):
    if request.user.is_authenticated:
        baskets = models.Basket.objects.filter(user=request.user)
        total_sum = 0
        for basket in baskets:
            total_sum += basket.total_price()
    else:
        baskets = []
        total_sum = 0
    context = {"baskets": baskets, "total_sum": total_sum}
    return render(request, "pages/basket.html", context)


def increase_quantity(request, basket_id):
    try:
        basket = models.Basket.objects.get(id=basket_id)
        basket.quantity += 1
        basket.save()
    except:
        pass
    return redirect("basket")


def decrease_quantity(request, basket_id):
    try:
        basket = models.Basket.objects.get(id=basket_id)
        if basket.quantity > 1:
            basket.quantity -= 1
            basket.save()
    except:
        pass
    return redirect("basket")


def add_to_basket(request, product_id):
    product = models.Products.objects.get(id=product_id)
    basket, created = models.Basket.objects.get_or_create(
        user=request.user, product=product
    )
    basket.save()
    return redirect("basket")


def delete_to_basket(request, product_id):
    basket = models.Basket.objects.filter(
        user=request.user, product_id=product_id
    ).first()
    basket.delete()
    return redirect("basket")


def favorite_page(request):
    if request.user.is_authenticated:
        favorites = models.Favorite.objects.filter(user=request.user)
    else:
        favorites = []
    context = {
        "favorites": favorites,
    }
    return render(request, "pages/favorite.html", context)


def add_favorite(request, product_id):
    if request.user.is_authenticated:
        try:
            product = models.Products.objects.get(id=product_id)
            models.Favorite.objects.get_or_create(user=request.user, product=product)
        except:
            pass
    return redirect("favorite")


def remove_favorite(request, favorite_id):
    if request.user.is_authenticated:
        favorite = models.Favorite.objects.filter(
            id=favorite_id, user=request.user
        ).first()
        favorite.delete()
    return redirect("favorite")


# Json
def json_overview(request):
    routes = {
        "Категории": "/json/category/",
        "Продукты": "/json/products/",
        "Корзины": "/json/baskets/",
        "Избранное": "/json/favorites/",
        "Профиль пользователя": "/json/user_profile/",
    }
    return JsonResponse({"Доступные маршруты": routes})


def get_categories(request):
    categories = models.Category.objects.all()
    categories_list = [{"id": c.id, "name": c.name} for c in categories]
    return JsonResponse({"категории": categories_list})


# Products Page
def get_ProductsPage(request):
    categories = models.Category.objects.all()
    products = models.Products.objects.all()
    categories_list = [{"id": c.id, "name": c.name} for c in categories]
    products_list = [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    return JsonResponse(
        {
            "категории": categories_list,
            "товары": products_list,
        }
    )


# Profile Page
def get_ProfilePage(request):
    if request.user.is_authenticated:
        try:
            profile = models.Profile.objects.get(user=request.user)
            profile_data = {
                "username": request.user.username,
                "email": request.user.email,
                "bio": profile.bio,
            }
            return JsonResponse({"профил": profile_data})
        except models.Profile.DoesNotExist:
            return JsonResponse({"ошибка": "Profile not found"}, status=404)
    else:
        return JsonResponse({"ошибка": "User not authenticated"}, status=401)


# Basket Page
def get_BasketPage(request):
    if request.user.is_authenticated:
        baskets = models.Basket.objects.filter(user=request.user)
        baskets_list = [
            {
                "id": b.id,
                "product": b.product.name,
                "quantity": b.quantity,
                "total_price": b.total_price(),
            }
            for b in baskets
        ]
        total_sum = sum(basket["total_price"] for basket in baskets_list)
        return JsonResponse({"корзина": baskets_list, "общая стоимость": total_sum})
    else:
        return JsonResponse({"ошибка": "User not authenticated"}, status=401)


# Favorites Page
def get_FavoritePage(request):
    if request.user.is_authenticated:
        favorites = models.Favorite.objects.filter(user=request.user)
        favorites_list = [{"товары": f.product.name} for f in favorites]
        return JsonResponse({"избранное": favorites_list})
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)
