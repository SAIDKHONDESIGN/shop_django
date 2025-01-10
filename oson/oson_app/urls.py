from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("products/", views.products_page, name="products"),
    path("products/<int:pk>/", views.products_detail_page, name="products_detail"),
    path("create/", views.create_product_view, name="create"),
    path("update/<int:pk>/", views.ProductUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.delete_product, name="delete"),
    path("categories/<int:pk>/", views.category_page, name="category"),
    path("login/", views.login_page, name="login"),
    path("registration/", views.registration_page, name="registration"),
    path("profile/", views.profile_page, name="profile"),
    path(
        "profile/<int:profile_id>/edit/", views.profile_edit_view, name="profile_edit"
    ),
    path("logout/", views.logout_page, name="logout"),
    path("search/", views.search, name="search"),
    path("favorite/", views.favorite_page, name="favorite"),
    path(
        "favorite/delete/<int:favorite_id>/",
        views.remove_favorite,
        name="favorite_delete",
    ),
    path("favorite/add/<int:product_id>/", views.add_favorite, name="favorite_add"),
    path("basket/", views.basket_page, name="basket"),
    path(
        "basket/increase/<int:basket_id>/",
        views.increase_quantity,
        name="increase_quantity",
    ),
    path(
        "basket/decrease/<int:basket_id>/",
        views.decrease_quantity,
        name="decrease_quantity",
    ),
    path("basket/add/<int:product_id>/", views.add_to_basket, name="add_to_basket"),
    path(
        "basket/delete/<int:product_id>/",
        views.delete_to_basket,
        name="delete_to_basket",
    ),
    # json
    path("json/", views.json_overview, name="json_overview"),
    path(
        "json/category/",
        views.get_categories,
        name="json_get_get_category",
    ),
    path("json/products/", views.get_ProductsPage, name="json_get_products"),
    path("json/baskets/", views.get_BasketPage, name="json_get_baskets"),
    path("json/favorites/", views.get_FavoritePage, name="json_get_favorites"),
    path("json/user_profile/", views.get_ProfilePage, name="json_get_user_profile"),
]
