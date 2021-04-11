from celery.decorators import task
from time import sleep


@task(name='task_csv_generator')
def task_csv_generator(duration, count_rows, pk, dataset_id):
    sleep(duration)
    from csv_data_generator.views import SchemaUpdateAndGenerateCsvView
    from csv_data_generator.models import SchemaDataSetCSV

    dataset = SchemaDataSetCSV.objects.get(pk=dataset_id)
    SchemaUpdateAndGenerateCsvView.generate_csv_with_fake_data(count_rows, pk, dataset)
    return'csv generated'

