from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.entities.employee import Employee
from core.serializers.employee_serializer import CreateEmployeeSerializer, EmployeeListSerializer, \
    EmployeeDetailSerializer, EmployeeInactivateSerializer, EmployeeUpdateSerializer


class CreateEmployeeView(generics.CreateAPIView):
    serializer_class = CreateEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        company = self.request.user
        serializer.save(company=company)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Employee created successfully", "data": response.data},
                        status=status.HTTP_201_CREATED)


class AllEmployeesView(generics.ListAPIView):
    serializer_class = EmployeeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filters = None
        company = self.request.user
        return self.serializer_class.get_filtered_queryset(company=company, filters=filters)


class FilteredEmployeesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeListSerializer

    def get_queryset(self):
        filters = self.request.query_params.dict()
        company = self.request.user
        return self.serializer_class.get_filtered_queryset(company=company, filters=filters)


class RetrieveEmployeeView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = self.request.user
        return Employee.objects.filter(company=company)


class InactivateEmployeeView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeInactivateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Funcionário inativado com sucesso!"},
            status=status.HTTP_200_OK)


class EmployeeUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeUpdateSerializer
    queryset = Employee.objects.all()
    lookup_field = 'id'

