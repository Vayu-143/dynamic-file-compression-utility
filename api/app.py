from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi.responses import FileResponse

from api.services import (
    CompressionService,
    DecompressionService
)

from src.database import (
    CompressionDatabase
)

import json
import os


app = FastAPI(
    title="Dynamic File Compression Utility API",
    description="Huffman Coding Based Compression Service",
    version="3.1.0"
)


# ==================================================
# Home Endpoint
# ==================================================

@app.get("/")
def home():

    return {
        "project": "Dynamic File Compression Utility",
        "version": "3.1.0",
        "status": "Running"
    }


# ==================================================
# Compress Endpoint
# ==================================================

@app.post("/compress")
async def compress(
    file: UploadFile = File(...)
):

    content = await file.read()

    return (
        CompressionService
        .compress_uploaded_file(
            content
        )
    )


# ==================================================
# Decompress Endpoint
# ==================================================

@app.post("/decompress")
async def decompress(
    binary_file: UploadFile = File(...),
    metadata_file: UploadFile = File(...)
):

    binary_content = (
        await binary_file.read()
    )

    metadata_content = (
        await metadata_file.read()
    )

    return (
        DecompressionService
        .decompress_uploaded_file(
            binary_content,
            metadata_content
        )
    )


# ==================================================
# Download Compressed File
# ==================================================

@app.get("/download")
def download():

    file_path = (
        "compressed_files/api_compressed.bin"
    )

    if not os.path.exists(file_path):

        return {
            "status": "error",
            "message": "Compressed file not found"
        }

    return FileResponse(
        file_path,
        filename="compressed.bin"
    )


# ==================================================
# Download Metadata File
# ==================================================

@app.get("/download-metadata")
def download_metadata():

    file_path = (
        "compressed_files/api_compressed.bin.json"
    )

    if not os.path.exists(file_path):

        return {
            "status": "error",
            "message": "Metadata file not found"
        }

    return FileResponse(
        file_path,
        filename="compressed.bin.json"
    )


# ==================================================
# Download Restored File
# ==================================================

@app.get("/download-restored")
def download_restored():

    file_path = (
        "decompressed_files/api_restored.txt"
    )

    if not os.path.exists(file_path):

        return {
            "status": "error",
            "message": "Restored file not found"
        }

    return FileResponse(
        file_path,
        filename="restored.txt"
    )


# ==================================================
# Analytics Endpoint
# ==================================================

@app.get("/analytics")
def analytics():

    analytics_file = (
        "outputs/analytics.json"
    )

    if not os.path.exists(analytics_file):

        return {
            "status": "error",
            "message": "analytics.json not found"
        }

    with open(
        analytics_file,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==================================================
# Benchmark Endpoint
# ==================================================

@app.get("/benchmark")
def benchmark():

    benchmark_file = (
        "outputs/benchmark.csv"
    )

    if not os.path.exists(benchmark_file):

        return {
            "status": "error",
            "message": "benchmark.csv not found"
        }

    with open(
        benchmark_file,
        "r",
        encoding="utf-8"
    ) as file:

        return {
            "data": file.read()
        }

# ==================================================
# Compression History Endpoint
# ==================================================

@app.get("/history")
def history():

    records = (
        CompressionDatabase.get_all()
    )

    return {
        "history": records
    }
    
# ==================================================
# Statistics Endpoint
# ==================================================

@app.get("/statistics")
def statistics():

    return (
        CompressionDatabase.statistics()
    )
    
# ==================================================
# History By ID
# ==================================================

@app.get("/history/{record_id}")
def history_by_id(
    record_id: int
):

    record = (
        CompressionDatabase.get_by_id(
            record_id
        )
    )

    if record is None:

        return {

            "status":
                "error",

            "message":
                "Record not found"
        }

    return record

# ==================================================
# Delete Record
# ==================================================

@app.delete("/history/{record_id}")
def delete_record(
    record_id: int
):

    deleted = (
        CompressionDatabase.delete_record(
            record_id
        )
    )

    if deleted:

        return {

            "status":
                "success",

            "message":
                f"Record {record_id} deleted"
        }

    return {

        "status":
            "error",

        "message":
            "Record not found"
    }
    
    # ==================================================
# Top Compressions
# ==================================================

@app.get("/top-compressions")
def top_compressions():

    return {

        "top_compressions":
            CompressionDatabase
            .top_compressions()
    }
    
    # ==================================================
# Recent Compressions
# ==================================================

@app.get("/recent-compressions")
def recent_compressions():

    return {

        "recent":
            CompressionDatabase
            .recent()
    }
    
    
# ==================================================
# Clear History
# ==================================================

@app.delete("/history")
def clear_history():

    CompressionDatabase.clear_all()

    return {

        "status":
            "success",

        "message":
            "All history deleted"
    }
# ==================================================
# Export Database
# ==================================================

@app.get("/database/export")
def export_database():

    db_path = (
        "database/compression.db"
    )

    if not os.path.exists(
        db_path
    ):

        return {

            "status":
                "error",

            "message":
                "Database not found"
        }

    return FileResponse(
        db_path,
        filename="compression.db"
    )
    
    # ==================================================
# Search Compression History
# ==================================================

@app.get("/search")
def search_history(
    filename: str
):

    return {

        "results":
            CompressionDatabase
            .search(filename)
    }


# ==================================================
# Dashboard Endpoint
# ==================================================

@app.get("/dashboard")
def dashboard():

    return (
        CompressionDatabase
        .dashboard()
    )
    
# ==================================================
# Health Endpoint
# ==================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "compression-api"
    }