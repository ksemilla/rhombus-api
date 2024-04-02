from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from .models import Ingest, Record, Column
from .tasks import process_file
from typing import List
from .schemas import IngestOut, RecordOut, ColumnOut, ColumnIn
from ninja.pagination import paginate, PageNumberPagination

ingest_api = NinjaAPI()

@ingest_api.post("/upload/")
def upload(request, file: UploadedFile = File(...)):
    ingest_id = request.POST.get("ingest_id")
    name = request.POST.get("name")
    file_name = request.POST.get("file_name")
    final_chunk = request.POST.get("finalChunk")


    if not ingest_id:

        temp_ingest = Ingest.objects.filter(name=name).first()
        if temp_ingest:
            return ingest_api.create_response(
                request=request,
                data={
                    "message": "Name already exists"
                },
                status=400
            )


        ingest = Ingest.objects.create(name=name, file_name=file_name)
    else:
        ingest = Ingest.objects.get(id=ingest_id)

    if ingest.file:
        with ingest.file.open(mode="ab") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    else:
        ingest.file.save(file_name, file)
    
    ingest.save()
    
    if final_chunk == "true":
        ingest.status = Ingest.Status.PROCESSING
        ingest.save()
        process_file.delay(ingest.id)

    return {
        "ingest_id": ingest.id,
        "status": ingest.status
    }

@ingest_api.get("", response=List[IngestOut])
@paginate(PageNumberPagination, page_size=20)
def list_ingest(request):
    return Ingest.objects.all()

@ingest_api.get("{ingest_id}/", response=IngestOut)
def get_ingest(request, ingest_id: int):
    return Ingest.objects.get(id=ingest_id)

@ingest_api.get("{ingest_id}/columns/", response=List[ColumnOut])
def get_ingest_columns(request, ingest_id: int):
    return Column.objects.filter(ingest__id=ingest_id).order_by("display_order")

@ingest_api.put("{ingest_id}/columns/{column_id}/", response=ColumnOut)
def get_ingest_columns(request, ingest_id: int, column_id: int, data: ColumnIn):
    column = Column.objects.filter(ingest__id=ingest_id).get(id=column_id)
    column.dtype = data.dtype
    column.save()
    return column

@ingest_api.get("{ingest_id}/records/", response=List[RecordOut])
@paginate(PageNumberPagination, page_size=20)
def get_ingest_records(request, ingest_id: int):
    return Record.objects.filter(ingest__id=ingest_id)