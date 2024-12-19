from fastapi import UploadFile, HTTPException
from markitdown import MarkItDown
from osbot_utils.utils.Files import file_exists, save_bytes_as_file, path_combine
import tempfile
import os

from osbot_utils.utils.Threads import invoke_async

import cbr_custom_open_sec_summit


class Markitdown_Service:
    def __init__(self):
        self.markitdown = MarkItDown()

    def process_file(self, file: UploadFile) -> str:
        """Process an uploaded file using MarkItDown."""
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        # Create a temporary file to store the upload
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            try:
                # Read the uploaded file content

                content = invoke_async(file.read())

                # Save to temporary file
                save_bytes_as_file(content, temp_file.name)

                # Process with MarkItDown
                result = self.markitdown.convert(temp_file.name)

                if not result or not result.text_content:
                    raise HTTPException(status_code=400, detail="Failed to process file")

                return result.text_content

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)

    def process_local_file(self, file_path: str) -> str:
        full_path = path_combine(cbr_custom_open_sec_summit.path, file_path)
        if not file_exists(full_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

        try:
            result = self.markitdown.convert(full_path)
            if not result or not result.text_content:
                raise HTTPException(status_code=400, detail="Failed to process file")
            return result.text_content

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
