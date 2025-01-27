from fastapi import APIRouter, HTTPException, Depends, FastAPI
from app.models import Item
from app.utils.direction import calculate_direction
from app.utils.postcode import is_valid_us_postcode
from mongoengine import ValidationError, SaveConditionError
from app.database import connect_to_mongo
from datetime import datetime
from bson import ObjectId

def serialize_item(item):
    """
    Converts MongoEngine item to a serializable dictionary.
    Ensures ObjectId is converted to a string.
    """
    item_dict = item.to_mongo().to_dict()
    item_dict["_id"] = str(item_dict["_id"])  # Convert ObjectId to string
    return item_dict

router = APIRouter()

@router.post("/items")
async def create_item(payload: dict):
    try:
        # Extract required fields
        name = payload.get("name")
        postcode = payload.get("postcode")
        latitude = payload.get("latitude")
        longitude = payload.get("longitude")
        users = payload.get("users", [])
        start_date_str = payload.get("startDate")
        
        # Validate required fields
        if not name or not postcode or latitude is None or longitude is None:
            raise HTTPException(status_code=400, detail="Missing required fields: name, postcode, latitude, or longitude.")
        if name not in users:
            raise HTTPException(status_code=400, detail="'name' must be included in 'users' list.")
        if not is_valid_us_postcode(postcode):
            raise HTTPException(status_code=400, detail="Invalid postcode format. Please enter a valid US postcode (XXXXX or XXXXX-XXXX).")

        try:
            parsed_date = datetime.fromisoformat(start_date_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'startDate'. Provide a valid ISO 8601 string.")

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            raise HTTPException(status_code=400, detail="Latitude and longitude must be valid floats.")

        # Calculate direction
        direction = calculate_direction(latitude, longitude)

        # Create and save the item
        item = Item(
            name=name,
            postcode=postcode,
            latitude=float(latitude),
            longitude=float(longitude),
            direction_from_new_york=direction,
            title=payload.get("title"),
            users=users,
            start_date=parsed_date
        )
        item.save()
        return {"message": "Item created successfully!"}

    except (ValidationError, SaveConditionError) as e:
        # MongoEngine-specific errors
        raise HTTPException(status_code=422, detail=f"Database validation error: {str(e)}")
    except HTTPException as http_exc:
        # Reraise known HTTP exceptions
        raise http_exc
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/items")
async def get_all_items():
    """
    Get all items.
    """
    try:
        items = Item.objects.all()
        return [serialize_item(item) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/items/{item_id}")
async def get_item_by_id(item_id: str):
    """
    Get a single item by its ID.
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item ID format.")

        item = Item.objects.get(id=item_id)
        return serialize_item(item)
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """
    Delete an item by its ID.
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item ID format.")

        # Attempt to find and delete the item
        item = Item.objects.get(id=item_id)
        item.delete()
        return {"message": f"Item with ID {item_id} has been successfully deleted."}

    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/items/{item_id}")
async def update_item(item_id: str, payload: dict):
    """
    Update an item by its ID.
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item ID format.")

        # Check if the item exists
        item = Item.objects.get(id=item_id)

        # Update item fields
        allowed_fields = {"name", "start_date", "title", "users"}
        for key, value in payload.items():
            if key in allowed_fields:
                setattr(item, key, value)

        # Save updated item
        item.save()
        return {"message": f"Item with ID {item_id} has been successfully updated."}

    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
