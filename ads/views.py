import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Category, Ad, Selection
from ads.permissions import SelectionUpdatePermission, AdUpdatePermission
from ads.serializers import CategorySerializer, SelectionSerializer
from hunting import settings
from users.models import User


def root(request):
    return JsonResponse({
        "status": "ok",
    })


@method_decorator(csrf_exempt, name='dispatch')
class AdView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        categories = request.GET.getlist("cat", [])
        if categories:
            self.object_list = self.object_list.filter(category_id__in=categories)

        if request.GET.get("text", None):
            self.object_list = self.object_list.filter(name__icontaions=request.GET.get("text"))

        if request.GET.get("location", None):
            self.object_list = self.object_list.filter(author__locations__name__icontaions=request.GET.get("location"))

        if request.GET.get("price_from", None):
            self.object_list = self.object_list.filter(price_gte=request.GET.get("price_from"))

        if request.GET.get("price_to", None):
            self.object_list = self.object_list.filter(price_lte=request.GET.get("price_to"))

        self.object_list = self.object_list.select_related("author").order_by("-price")
        paginator = Paginator(self.object_list, settings.TOTAL_0N_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None
            })

        response = {
            "items": ads,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }

        return JsonResponse(response, safe=False)


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionRetrieveView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, ad_data["author_id"])
        category = get_object_or_404(Category, ad_data["category_id"])

        ad = Category.objects.create(
            name=ad_data["name"],
            author=ad_data["author"],
            price=ad_data["price"],
            description=ad_data["description"],
            address=ad_data["address"],
            is_published=ad_data["is_published"],
            category=category
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]

        self.object.author = get_object_or_404(User, ad_data["author_id"])
        self.object.category = get_object_or_404(Category, ad_data["category_id"])

        self.object.save()

        return JsonResponse({
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "price": self.price,
            "description": self.description,
            "address": self.address,
            "is_published": self.is_published,
            "category_id": self.category_id,
            "image": self.image.url if self.image else None
        })


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdUpdatePermission]


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(ListView):
    # model = Category
    # queryset = Category.objects.all()

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist("category_id", None)

        category_q = None
        for category in categories:
            if not skills_q:
                skills_q = Q(category__id__contains=category)
            else:
                skills_q |= Q(category__id__contains=category)
        if skills_q:
            self.queryset = self.queryset.filter(skills_q)



class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"],
        )
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(CreateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "address": self.object.address,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        })