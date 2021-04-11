import csv
import random
import string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from csv_data_generator.models import Schema, SchemaColumn, SchemaDataSetCSV
from csv_data_generator.tasks import task_csv_generator


class IndexSchemaView(LoginRequiredMixin, generic.ListView):
    """
    Show schemas created by current user
    """
    template_name = 'index.html'
    model = Schema

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class NewSchemaView(generic.View):
    """
    In this view, we create new schema with dynamic fields(columns)
    """
    template_name = 'newschema.html'
    success_url = 'index-schema'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        name_of_schemas = request.POST.get('name_of_schemas')
        columns_name = request.POST.getlist('column_name')
        types = request.POST.getlist('choices')
        orders = request.POST.getlist('order')
        schema = self.create_schema(name_of_schemas)
        self.create_columns_to_schema(schema, columns_name, types, orders)
        return redirect(reverse_lazy(self.success_url))

    def create_schema(self, name_of_schemas: str = None) -> Schema:
        schema = Schema.objects.create(name=name_of_schemas, user=self.request.user)
        return schema

    @staticmethod
    def create_columns_to_schema(schema, columns_name: list = None, types: list = None,
                                 orders: list = None) -> None:
        for index in range(len(columns_name)):
            try:
                column_name = columns_name[index]
                type_ = types[index]
                order = orders[index]
            except IndexError:
                raise Exception("Incorrect data")
            SchemaColumn.objects.create(
                schema_id=schema.id, column_name=column_name, type_of_column=type_,
                order=order
            )


class SchemaDetailView(generic.DetailView):
    """
    View for detail schema
    """
    model = Schema
    template_name = 'schema_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class SchemaUpdateAndGenerateCsvView(generic.View):
    """
    View for Generate Csv
    """
    template_name = 'schema_update.html'
    queryset = SchemaDataSetCSV.objects.all()
    success_url = 'schema-update'

    def get(self, request, *args, **kwargs):
        schema = Schema.objects.filter(pk=kwargs['pk']).first()
        queryset = self.queryset.filter(schema__user=self.request.user, schema=schema)
        context = {'object_list': queryset, 'schema': schema}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        count_rows = request.POST['rows']
        dataset = self.create_dataset_csv()
        task_csv_generator.delay(duration=10, count_rows=count_rows, pk=kwargs['pk'], dataset_id=dataset.id)
        return redirect(reverse_lazy(self.success_url, kwargs={'pk': kwargs['pk']}))

    def create_dataset_csv(self):
        schema = Schema.objects.filter(pk=self.kwargs['pk']).first()
        csv_object = SchemaDataSetCSV.objects.create(schema=schema, status='pending')
        return csv_object

    @staticmethod
    def generate_csv_with_fake_data(count_rows: int = None, pk: int = None, dataset: SchemaDataSetCSV = None) -> bool:
        csv_object = dataset
        fields = []
        name_of_csv = SchemaUpdateAndGenerateCsvView.generate_name_to_csv()
        schema = Schema.objects.filter(id=pk).first()
        for column in schema.columns.all():
            fields.append({
                'column_name': column.column_name + '0',
                'type_of_column': column.type_of_column + '1',
            })
        fields_name = [i for x in fields for i in x.values()]
        dict_ = {}

        """create csv file with random data, use DictWriter"""
        with open(f'{name_of_csv}', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields_name)

            writer.writeheader()
            for _ in range(int(count_rows)):
                for index, name in enumerate(fields_name):
                    column_name = None
                    type_of_column = None
                    if name[-1] == '0':
                        try:
                            column_name = name
                            type_of_column = fields_name[index + 1]
                        except IndexError:
                            type_of_column = fields_name[-1]
                    if column_name and type_of_column:
                        value = SchemaUpdateAndGenerateCsvView.get_random_column_name_value()
                        dict_.update({
                            column_name: value,
                            type_of_column: type_of_column,
                        })
                writer.writerow(dict_)
            csv_object.status = 'ready'
            csv_object.link = name_of_csv
            csv_object.save()
        if csv_object.status == 'ready':
            return True
        else:
            return False

    @staticmethod
    def generate_name_to_csv() -> str:
        random_number = random.randint(100000, 9999999999)
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        full_file_name = f'datasets/{random_string}{random_number}.csv'
        return full_file_name

    @staticmethod
    def get_random_column_name_value() -> str:
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
