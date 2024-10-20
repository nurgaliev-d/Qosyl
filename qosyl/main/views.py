from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def users_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def organization_list(request):
    organizations = Organization.objects.all() 
    serializer = OrganizationSerializer(organizations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_profile_list(request):
    user_profiles = UserProfile.objects.all()
    serializer = UserProfileSerializer(user_profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data)

@api_view(['GET'])
def public_user_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data)


@api_view(['GET'])
def other_user_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id) 
    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data)

@api_view(['GET'])
def publication_list(request):
    publications = Publication.objects.all()
    serializer = PublicationSerializer(publications, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def create_publication(request):
    serializer = PublicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    serializer = PublicationSerializer(publication)
    return Response(serializer.data)

@api_view(['PUT'])
def update_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    serializer = PublicationSerializer(publication, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    publication.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def like_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    user_profile = request.user.userprofile  # Assuming user has a UserProfile
    if user_profile in publication.likes.all():
        publication.likes.remove(user_profile)
    else:
        publication.likes.add(user_profile)
    publication.save()
    return Response({"status": "success"})