import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import LoadControl, LoadError
from sqlalchemy.dialects.postgresql import insert as pg_insert

def process_batch(db: Session, target_table_name: str, model_class, batch_data: list, pydantic_schema):
    
    load_control = LoadControl(
        target_table=target_table_name,
        total_records=len(batch_data)
    )
    db.add(load_control)
    db.flush() 

    valid_records = []
    error_records = []

    for item in batch_data:
        try:

            validated_item = pydantic_schema(**item)
            item_dict = validated_item.model_dump()

            if any(value is None for value in item_dict.values()):
                raise ValueError("El registro contiene valores nulos")

            valid_records.append(item_dict)

        except Exception as e:
            error_records.append(
                LoadError(
                    load_control_id=load_control.id,
                    raw_data=json.dumps(item, default=str),
                    error_message=str(e)
                )
            )

    if valid_records:
        stmt = pg_insert(model_class).values(valid_records)
        stmt = stmt.on_conflict_do_nothing(index_elements=['id'])
        
        db.execute(stmt)

    if error_records:
        db.add_all(error_records)

    load_control.success_records = len(valid_records)
    load_control.failed_records = len(error_records)
    load_control.end_time = datetime.utcnow()

    db.commit()

    return {
        "load_control_id": load_control.id,
        "total_received": len(batch_data),
        "inserted": len(valid_records),
        "failed": len(error_records)
    }