from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from csv_data_generator.models import Schema, SchemaColumn


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


class SchemaUpdateAndGenerateCsvView(generic.UpdateView):
    model = Schema
    template_name = 'schema_update.html'
