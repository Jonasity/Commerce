from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activelisting", views.activelisting, name="activelisting"),
    path("viewlisting/<int:product_id>", views.viewlisting, name="viewlisting"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("addtowatchlist/<int:product_id>", views.addtowatchlist, name="addtowatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addcomment/<int:product_id>", views.addcomment, name="addcomment"),
    path("closeauction/<int:product_id>", views.closeauction, name="closeauction"),
    path("closedlistings", views.closedlistings, name="closedlistings"),
    path("categories", views.categories, name="categories")
]
