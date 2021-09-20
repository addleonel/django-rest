from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (snippet_list, snippet_detail, SnippetList, SnippetDetail,
                    SnippetListUsingMixins, SnippetDetailUsingMixins,
                    SnippetListCreateView, SnippetRetrieveUpdateDestroyView
                    )

app_name = 'snippets'
urlpatterns = [
    # function-based views
    path('', snippet_list, name='snippet_list'),
    path('<int:pk>', snippet_detail, name='snippet_detail'),
    
    # class-based views
    path('snippetsc', SnippetList.as_view(), name='snippet_listc'),
    path('snippetsc/<int:pk>', SnippetDetail.as_view(), name='snippet_detailc'),

    # generic class-based view using mixins
    path('snippetscgm', SnippetListUsingMixins.as_view(), name='snippet_listcgm'),
    path('snippetscgm/<int:pk>', SnippetDetailUsingMixins.as_view(), name='snippet_detailcgm'),

    # generic class-based view
    path('snippetscg', SnippetListCreateView.as_view(), name='snippet_listcg'),
    path('snippetscg/<int:pk>', SnippetRetrieveUpdateDestroyView.as_view(), name='snippet_detailcg'),
]

urlpatterns = format_suffix_patterns(urlpatterns)