"""Cloud Storage upload helper service."""

class StorageService:
    def generate_upload_url(self, job_id: str, file_name: str) -> str:
        return f"https://storage.googleapis.com/mock-bucket/jobs/{job_id}/{file_name}?mock_token=12345"

storage_service = StorageService()
