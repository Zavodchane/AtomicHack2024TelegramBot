import os.path
from datetime import date
from uuid import uuid4

import cv2
import pandas as pd
import supervision as sv
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from src.defect import schemas as defect_schemas
from src.defect import service as defect_service
from src.defect.models import Defect
from src.image import models as image_models
from src.image import schemas as image_schemas
from src.image import service as image_service
from src.user import service as user_service
from src.user.models import User


def read_image(imgPath):
    image = cv2.imread(imgPath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


async def predicate_image(
    path: str,
    photo_name: str,
    model,
    session: AsyncSession,
    chat_id: int,
):
    user: User = await user_service.get_user(user_id=str(chat_id), session=session)

    image = read_image(os.path.join(path, photo_name))
    results = model(image)[0]
    bboxes = results.boxes.xywhn
    detections = sv.Detections.from_ultralytics(results)

    image_schema = image_schemas.Image(
        name=photo_name,
        size=image.size,
        created_at=date.today(),
        user_id=str(chat_id),
    )
    image_orm: image_models.Image = await image_service.create_image(
        image_schema=image_schema,
        session=session,
    )

    detected_class = detections.data.get("class_name")
    classes: dict = {}
    predict: dict = {}
    for i in range(len(detected_class)):
        classes.setdefault(detected_class[i], 0)
        classes[detected_class[i]] += 1

        predict.setdefault("class_id", []).append(detections.class_id[i])
        predict.setdefault("rel_x", []).append(bboxes[i][0].detach().numpy())
        predict.setdefault("rel_y", []).append(bboxes[i][1].detach().numpy())
        predict.setdefault("width", []).append(bboxes[i][2].detach().numpy())
        predict.setdefault("height", []).append(bboxes[i][3].detach().numpy())

        defect_schema = defect_schemas.Defect(
            class_id=predict["class_id"][i],
            name=detected_class[i],
            rel_x=predict["rel_x"][i],
            rel_y=predict["rel_y"][i],
            width=predict["width"][i],
            height=predict["height"][i],
            image_id=image_orm.id,
        )
        defect: Defect = await defect_service.create_defect(
            defect_schema=defect_schema,
            session=session,
        )

    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    annotated_image = bounding_box_annotator.annotate(
        scene=image, detections=detections
    )
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections
    )
    im = Image.fromarray(annotated_image)
    predicate_image_path = os.path.join(path, photo_name)
    im.save(predicate_image_path)

    caption: str = "На картинке были найдены:\n"
    for key, value in classes.items():
        caption += f"- {key}: {value}\n"

    csv_path = os.path.join(path, f"{uuid4()}.csv")
    df = pd.DataFrame(predict)

    df.to_csv(csv_path, index=False)

    return predicate_image_path, caption, csv_path
