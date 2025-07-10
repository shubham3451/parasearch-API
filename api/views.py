from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .serializers import ParagraphUploadSerializer, ParagraphSerializer
from .models import Paragraph, WordIndex
from .utils import tokenize_paragraphs
from .parser import PlainTextParser  


class ParagraphUploadView(APIView):
    """
    Upload raw text (text/plain), split into paragraphs, and index words.
    Each paragraph is separated by two newlines (\\n\\n).
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [PlainTextParser] 

    @extend_schema(
        request=ParagraphUploadSerializer,
        responses={201: {"type": "object", "properties": {"detail": {"type": "string"}}}},
        tags=["Paragraphs"],
        summary="Upload and index paragraphs",
        description="Accepts raw text (text/plain) with multiple paragraphs separated by two blank lines."
    )
    def post(self, request):
        serializer = ParagraphUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data['text']
        for content, words in tokenize_paragraphs(text):
            paragraph = Paragraph.objects.create(
                content=content,
                created_by=request.user
            )

            normalized_words = set(word.strip().lower() for word in words if word.strip())

            WordIndex.objects.bulk_create([
                WordIndex(word=word, paragraph=paragraph) for word in normalized_words
            ], ignore_conflicts=True)

        return Response({"detail": "Paragraphs uploaded and indexed."}, status=status.HTTP_201_CREATED)

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='word',
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Word to search for in indexed paragraphs.",
            examples=[
                OpenApiExample(
                    name='SearchExample',
                    value='lorem',
                    summary='Example search input'
                )
            ]
        )
    ],
    responses=ParagraphSerializer(many=True),
    tags=["Paragraphs"],
    summary="Search indexed paragraphs",
    description="Returns up to 10 paragraphs where the specified word appears."
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_word(request):
    """Search paragraphs by word (lowercased, whitespace-trimmed)."""
    word = request.query_params.get("word", "").strip().lower()
    if not word:
        return Response(
            {"error": "Query parameter 'word' is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    paragraph_ids = (
        WordIndex.objects
        .filter(word=word)
        .values_list("paragraph_id", flat=True)
        .distinct()[:10]
    )

    paragraphs = Paragraph.objects.filter(id__in=paragraph_ids)
    serializer = ParagraphSerializer(paragraphs, many=True)
    print(serializer.data)
    return Response(serializer.data)

