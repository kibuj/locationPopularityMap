from django.db.models import Avg, Count, Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Location, Category, Review, ReviewVote
from .serializers import LocationSerializer, CategorySerializer, ReviewSerializer
from .filters import LocationFilter



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = (DjangoFilterBackend, SearchFilter) # детальна фільтрація полів і повнотекстовий пошук по вказаних полях

    search_fields = ['name', 'address', 'coordinates']

    filterset_class = LocationFilter

    def get_queryset(self):
        return Location.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating', 'name')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.all()
        location_id = self.request.query_params.get('location_id')
        if location_id:
            queryset = queryset.filter(location_id=location_id)

        return queryset.annotate(
            likes_count=Count('votes', filter=Q(votes__vote=ReviewVote.LIKE)),
            dislikes_count=Count('votes', filter=Q(votes__vote=ReviewVote.DISLIKE))
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    def _create_vote(self, request, review, vote_type):
        user = request.user
        vote, created = ReviewVote.objects.update_or_create(
            review=review,
            user=user,
            defaults={'vote': vote_type}
        )
        return Response({'status': 'vote set'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        review = self.get_object()
        return self._create_vote(request, review, ReviewVote.LIKE)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        review = self.get_object()
        return self._create_vote(request, review, ReviewVote.DISLIKE)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove_vote(self, request, pk=None):
        review = self.get_object()
        ReviewVote.objects.filter(review=review, user=request.user).delete()
        return Response({'status': 'vote removed'}, status=status.HTTP_200_OK)