from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from core.serializers.company_serializer import CompanySerializer,  CompanyDetailsSerializer, \
    CompanyUpdateSerializer, CompanyFilteredSerializer
from core.serializers.jwt_serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from core.entities.company import Company


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class CreateCompanyView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CompanySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        business_name = serializer.data.get("business_name")
        headers = self.get_success_headers(serializer.data)
        return Response(
            f"Empresa {business_name} cadastrada com sucesso!",
            status=status.HTTP_201_CREATED,
            headers=headers)


class ApproveCompanyView(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        company = self.get_object()
        return Response(
            {"detail": f"The company {company.business_name} has been successfully approved!"},
            status=status.HTTP_200_OK
        )


class AllCompaniesView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CompanyFilteredSerializer

    def get_queryset(self):
        filters = None
        return CompanyFilteredSerializer.get_filtered_queryset(filters=filters)


class FilteredCompaniesView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CompanyFilteredSerializer

    def get_queryset(self):
        filters = self.request.query_params.dict()
        return CompanyFilteredSerializer.get_filtered_queryset(filters=filters)


class CompanyDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CompanyDetailsSerializer
    queryset = Company.objects.all()
    lookup_field = 'id'


class CompanyUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CompanyUpdateSerializer
    queryset = Company.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        super().update(self, request, *args, **kwargs)
        return Response(
            {"detail": "Company successfully updated!"},
            status=status.HTTP_204_NO_CONTENT)


class InactivateCompanyView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(
            {"detail": "Company successfully inactivated!"},
            status=status.HTTP_204_NO_CONTENT
        )


