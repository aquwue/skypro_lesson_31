
import json
from functools import partial

import pandas as pandas
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from rest_framework import viewsets, status
from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from ads.models import Category, Ad
from hunting import settings
from users.models import User, Location


# @method_decorator(csrf_exempt, name='dispatch')
from users.serializers import UserSerializer


class ItemViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # model = User
    # queryset = User.objects.all()
    #
    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #     self.object_list = self.object_list.annotate(total_ads=Count('ad'))
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_0N_PAGE)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #
    #     users = []
    #     for user in users:
    #         users.append({
    #             "id": user.id,
    #             "username": user.username,
    #             "first_name": user.first_name,
    #             "last_name": user.last_name,
    #             "role": user.role,
    #             "age": user.age,
    #             "total_ads": user.total_ads,
    #             "locations": list(map(str, user.locations.all()))
    #         })
    #
    #     response = {
    #         "items": users,
    #         "num_pages": page_obj.paginator.num_pages,
    #         "total": page_obj.paginator.count,
    #     }
    #
    #     return JsonResponse(response, safe=False)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # model = User
    #
    # def get(self, request, *args, **kwargs):
    #     user = self.get_object()
    #
    #     return JsonResponse({
    #         "id": user.id,
    #         "name": user.name,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "role": user.role,
    #         "age": user.age,
    #         "locations": list(map(str, user.locations.all()))
    #     })


# @method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # model = User
    # fields = ["username", "password", "first_name", "last_name", "role", "age", "location"]
    #
    # def post(self, request, *args, **kwargs):
    #     user_data = json.loads(request.body)
    #
    #     user = User.objects.create(
    #         username=user_data["username"],
    #         password=user_data["password"],
    #         first_name=user_data["first_name"],
    #         last_name=user_data["last_name"],
    #         role=user_data["role"],
    #         age=user_data["age"],
    #     )
    #
    #     for location_name in user_data["locations"]:
    #         location, _ = Location.object.get_or_create(name=location_name)
    #         user.locations.add(location)
    #
    #     return JsonResponse({
    #         "id": user.id,
    #         "name": user.name,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "role": user.role,
    #         "age": user.age,
    #         "locations": list(map(str, user.locations.all()))
    #     })


# @method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # model = User
    # fields = ["username", "password", "first_name", "last_name", "role", "age", "location"]
    #
    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #
    #     user_data = json.loads(request.body)
    #     self.object.username = user_data["username"]
    #     self.object.password = user_data["password"]
    #     self.object.first_name = user_data["first_name"]
    #     self.object.last_name = user_data["last_name"]
    #     self.object.age = user_data["age"]
    #
    #     for location_name in user_data["locations"]:
    #         location, _ = Location.object.get_or_create(name=location_name)
    #         self.object.locations.add(location)
    #
    #     self.object.save()
    #
    #     return JsonResponse({
    #         "id": self.object.id,
    #         "name": self.object.name,
    #         "first_name": self.object.first_name,
    #         "last_name": self.object.last_name,
    #         "role": self.object.role,
    #         "age": self.object.age,
    #         "locations": list(map(str, self.object.locations.all()))
    #     })


# @method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # model = User
    # success_url = "/"
    #
    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse({"status": "ok"}, status=200)


class LocationViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        serializer = UserSerializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)

        return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
