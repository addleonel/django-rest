from django.http import Http404
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from .models import Snippet
from .serializers import SnippetSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def snippet_list(request, format=None):
    """
    List snippets or create new one
    """

    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def snippet_detail(request, pk, format=None):
    """
    Snippet details, retrieve, update or delete a code snippet
    """

    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SnippetList(APIView):
    """
    Class-based view. List and create snippet
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Class-based view. Retrieve, Update, Delete Snippet
    """
    permission_classes = [IsAuthenticated]

    def get_snippet_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Http404
    
    def get(self, request, pk, format=None):
        snippet = self.get_snippet_object(pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        snippet = self.get_snippet_object(pk=pk)
        serializer = SnippetSerializer(snippet, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_snippet_object(pk=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SnippetListUsingMixins(mixins.ListModelMixin, 
                            mixins.CreateModelMixin, 
                            generics.GenericAPIView):
    """
    Class-based view using mixins and GenericAPIview. List and create
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetailUsingMixins(mixins.RetrieveModelMixin, 
                                mixins.UpdateModelMixin, 
                                mixins.DestroyModelMixin,
                                generics.GenericAPIView):
    """
    Class-based view using mixins and GenericAPIView.
    Retrieve, update, and destroy.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class SnippetListCreateView(generics.ListCreateAPIView):
    """
    class-based view using ListCreateAPIView. List and create.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

class SnippetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    class-based view using RetrieveUpdateDestroyAPIView. 
    Retrieve, update, and destroy 
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]