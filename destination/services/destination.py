import asyncio
from uuid import UUID
from typing import Optional
from app.utils.print_log import print_log

from app.utils.cloudinary_manager import CloudinaryImageManager

from destination.db.crud import (
	DestinationCRUD, 
	AccommodationCRUD, 
	TransportCRUD, 
	ActivityCRUD
)

from destination.schema import DestinationImageDetails

class DestinationService:
	def __init__(self, db):
		self.db = db
		self.destination_crud = DestinationCRUD(db)
		self.accommodation_crud = AccommodationCRUD(db)
		self.transport_crud = TransportCRUD(db)
		self.activity_crud = ActivityCRUD(db)
		self.image_manager = CloudinaryImageManager()

	async def __validate_reference_ids(self, destination_data: dict):
		"""
		Validate that all referenced accommodation, transport, and activity types exist
		"""
		# Validate accommodation types
		for acc_type in destination_data.get("accommodation_types", []):
			type_id = UUID(acc_type["accommodation_type_id"])
		
			exists = await self.accommodation_crud.get_accommodation_type_by_id(type_id)
			if not exists:
				raise ValueError(f"Accommodation type with ID {type_id} does not exist")

		# Validate transport types
		for transport in destination_data.get("transport_options", []):
			type_id = UUID(transport["transport_type_id"])
			exists = await self.transport_crud.get_transport_type_by_id(type_id)
			if not exists:
				raise ValueError(f"Transport type with ID {type_id} does not exist")

		# Validate activity types
		for activity in destination_data.get("activities", []):
			type_id = UUID(activity["activity_type_id"])
			exists = await self.activity_crud.get_activity_type_by_id(type_id)
			if not exists:
				raise ValueError(f"Activity type with ID {type_id} does not exist")


	async def __image_uploader(self, images: list[dict]) -> list[dict]:
		loop = asyncio.get_running_loop()

		tasks = [
			loop.run_in_executor(
				None,
				self.image_manager.upload,
				img["file"].file,
			)
			for img in images
		]

		results = await asyncio.gather(*tasks)

		uploaded = []
		for img, res in zip(images, results):
			uploaded.append({
				"type": img["type"],
				"destination_id": img.get("destination_id"),
				"attraction_id": img.get("attraction_id"),
				"image_url": res["url"],
				"public_id": res["public_id"],
				"alt_text": img.get("alt_text"),
			})

		return uploaded

	
	async def upload_images(self, image_data: list[dict]):
		uploaded_images = await self.__image_uploader(image_data)

		destination_images = []
		attraction_images = []

		for img in uploaded_images:
			if img["type"] == "destination":
				destination_images.append({
					"destination_id": img["destination_id"],
					"image_url": img["image_url"],
					"public_id": img["public_id"],
					"alt_text": img["alt_text"],
				})

			elif img["type"] == "attraction":
				attraction_images.append({
					"attraction_id": img["attraction_id"],
					"image_url": img["image_url"],
					"public_id": img["public_id"],
					"alt_text": img["alt_text"],
				})

		uploaded = []

		if destination_images:
			dest_imgs = await self.destination_crud.add_destination_images(
				destination_images
			)
			uploaded.extend([
        DestinationImageDetails(
            image_url=img.image_url,
            alt_text=img.alt_text
        )
        for img in dest_imgs
    	])

		if attraction_images:
			attr_imgs = await self.destination_crud.add_attraction_images(
				attraction_images
			)
			uploaded.extend([
        DestinationImageDetails(
            image_url=img.image_url,
            alt_text=img.alt_text
        )
        for img in attr_imgs
    	])

		return uploaded


	async def create_destination(self, destination_data: dict):
		# 1. create destination in Database
		
		try:
			# Validate that referenced types exist
			await self.__validate_reference_ids(destination_data)

			created_destination = await self.destination_crud.create(destination_data)

			# 2. bring vector resources and handle vector database

			return created_destination
			
        
		except Exception as e:
			raise Exception(f"Failed to create destination: {str(e)}")
	
	
	async def delete_destination(self, destination_id: UUID):
		"""
		Delete destination with destination_id
		** Later clear the vector db resources
		"""
		try:
			await self.destination_crud.delete(destination_id)
		
		except Exception as e:
			raise Exception(f"Failed to delete destination: {str(e)}")


	async def destination_list(
		self, 
		page: int, 
		page_size: int = 10, 
		search_query: Optional[str] = None
	):
		
		destination_list, total_count = await self.destination_crud.get_list(
			page, 
			page_size, 
			search_query
		)

		return destination_list, total_count
	