import json
import cv2
from pathlib import Path

IMAGE_FOLDER = Path("generated_images/no_none")
JSON_FILE = "auto_boxes_no.json"
OUTPUT_FOLDER = Path("preview_boxes")

OUTPUT_FOLDER.mkdir(exist_ok=True)

with open(JSON_FILE, "r") as f:
    data = json.load(f)

for item in data:
    img_path = IMAGE_FOLDER / item["file_name"]
    img = cv2.imread(str(img_path))

    if img is None:
        print("Could not read:", img_path)
        continue

    for person in item["people"]:
        x1, y1, x2, y2 = person["bbox"]
        pid = person["id"]

        # Draw box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Label text: ID + role
        label_text = f"id:{pid}"

        # Draw text background (for readability)
        (w, h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - h - 5), (x1 + w, y1), (0, 255, 0), -1)

        # Draw text
        cv2.putText(
            img,
            label_text,
            (x1, y1 - 3),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1
        )

    out_path = OUTPUT_FOLDER / item["file_name"]
    cv2.imwrite(str(out_path), img)

print(f"Done. Check the folder: {OUTPUT_FOLDER}")