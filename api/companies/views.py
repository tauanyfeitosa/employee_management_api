from django.core.exceptions import FieldError
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from core.serializers.company_serializer import CompanySerializer, CompanyListSerializer, CompanyDetailsSerializer, \
    CompanyUpdateSerializer
from core.serializers.jwt_serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from core.entities.company import Company
from core.use_cases.company.get_companies_use_case import GetCompaniesUseCase


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class CreateCompanyView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CompanySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Salva a nova empresa no banco de dados
        business_name = serializer.data.get("business_name")  # Acessa o business_name da nova empresa
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
        company = self.get_object()
        if company.is_approved:
            return Response(
                {"message": f"A empresa {company.business_name} já está aprovada."},
                status=status.HTTP_400_BAD_REQUEST)

        company.is_approved = True
        company.save()
        return Response(
            {"message": f"A empresa {company.business_name} foi aprovada com sucesso!"},
            status=status.HTTP_200_OK)


class AllCompaniesView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CompanyListSerializer
    use_case = GetCompaniesUseCase()

    def get_queryset(self):
        return self.use_case.execute()


class FilteredCompaniesView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CompanyListSerializer
    use_case = GetCompaniesUseCase()

    def get_queryset(self):
        filters = self.request.query_params.dict()
        try:
            return self.use_case.execute(filters=filters)
        except FieldError as e:
            raise ValidationError({"detail": str(e)})


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


class InactivateCompanyView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_active:
            return Response({"detail": "Empresa já está inativa."}, status=status.HTTP_400_BAD_REQUEST)

        instance.is_active = False
        instance.is_approved = False
        instance.save()
        return Response({"detail": "Empresa inativada com sucesso!"}, status=status.HTTP_200_OK)


