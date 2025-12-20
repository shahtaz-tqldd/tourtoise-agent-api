from typing import List, Dict, Any
from cloudinary import (
    uploader, 
    api, 
    config as clodunary_config
)

from app.core.config import get_settings
from app.core.logging import setup_logging

settings = get_settings()
logger = setup_logging()


class CloudinaryImageManager:
    def __init__(self):
        clodunary_config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )

    def upload(self, image_file, folder: str = "tourtoise") -> Dict[str, Any]:
        """
        Upload a single image to Cloudinary
        """
        try:
            result = uploader.upload(
                image_file,
                folder=folder,
                resource_type="image",
            )

            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "width": result["width"],
                "height": result["height"],
                "format": result["format"],
            }

        except Exception as e:
            logger.error("Cloudinary upload failed")
            raise RuntimeError("Image upload failed") from e

    def bulk_upload(self, image_files: List, folder: str = "tourtoise") -> List[Dict[str, Any]]:
        """
        Upload multiple images to Cloudinary
        """
        results = []

        for image in image_files:
            results.append(self.upload(image, folder=folder))

        return results

    def delete(self, public_id: str) -> bool:
        """
        Delete a single image from Cloudinary
        """
        try:
            result = uploader.destroy(public_id)

            return result.get("result") == "ok"

        except Exception as e:
            logger.error("Cloudinary delete failed")
            raise RuntimeError("Image deletion failed") from e

    def bulk_delete(self, public_ids: List[str]) -> Dict[str, str]:
        """
        Delete multiple images from Cloudinary
        """
        try:
            result = api.delete_resources(public_ids)

            # returns dict: {public_id: "deleted"}
            return result.get("deleted", {})

        except Exception as e:
            logger.error("Cloudinary bulk delete failed")
            raise RuntimeError("Bulk image deletion failed") from e
