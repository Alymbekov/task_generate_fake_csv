import csv
import random
import string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from csv_data_generator.models import Schema, SchemaColumn, SchemaDataSetCSV, TYPE_OF_COLUMN


class IndexSchemaView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    model = Schema


class NewSchemaView(generic.View):
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

    @staticmethod
    def create_schema(name_of_schemas: str = None) -> Schema:
        schema = Schema.objects.create(name=name_of_schemas)
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
    model = Schema
    template_name = 'schema_detail.html'


class SchemaUpdateAndGenerateCsvView(generic.View):
    template_name = 'schema_update.html'
    queryset = SchemaDataSetCSV.objects.all()
    success_url = 'schema-update'

    def get(self, request, *args, **kwargs):
        schema = Schema.objects.filter(pk=kwargs['pk']).first()
        context = {'object_list': self.queryset, 'schema': schema}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        count_rows = request.POST['rows']
        self.generate_csv_with_fake_data(count_rows, kwargs['pk'])
        return redirect(reverse_lazy(self.success_url, kwargs={'pk': kwargs['pk']}))

    @staticmethod
    def generate_csv_with_fake_data(count_rows: int = None, pk: int = None) -> bool:
        fields = []
        name = SchemaUpdateAndGenerateCsvView.generate_name_to_csv()
        schema = Schema.objects.filter(id=pk).first()
        for column in schema.columns.all():
            fields.append({
                'column_name': column.column_name + '0',
                'type_of_column': column.type_of_column + '1',
                'order': str(column.order) + '2'
            })
        fields_name = [i for x in fields for i in x.values()]
        dict_ = {}
        with open(f'{name}', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields_name)

            writer.writeheader()
            for _ in range(int(count_rows)):
                for index, name in enumerate(fields_name):
                    column_name = None
                    type_of_column = None
                    order = None
                    if name[-1] == '0':
                        column_name = name
                    if name[-1] == '1':
                        type_of_column = type_of_column
                    if name[-1] == '2':
                        order = order
                    dict_.update({
                        column_name: SchemaUpdateAndGenerateCsvView.get_random_column_name_value(),
                        type_of_column: type_of_column,
                        order: index
                    })
            print(dict_)
            return True

    @staticmethod
    def generate_name_to_csv():
        random_number = random.randint(100000, 9999999999)
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        full_file_name = f'{random_string}{random_number}.csv'
        return full_file_name

    @staticmethod
    def get_random_column_name_value():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

