import logging
from pathlib import Path

def extract_text(doc) -> str:
    return "\n\n".join([page.get_text("text") for page in doc])

def extract_images(
        doc,
        base_name: str,
        img_path: Path,
        min_width: int = 100,
        min_height: int = 100,
) -> list[str]:

    print(f"🔍 Search image {base_name}")

    image_paths = []
    for page_index, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)

            width = base_image.get("width", 0)
            height = base_image.get("height", 0)

            if width >= min_width and height >= min_height:
                image_bytes = base_image["image"]
                ext = base_image["ext"]
                image_path = img_path / f"{base_name}_p{page_index+1}_img{img_index+1}.{ext}"
                image_path.write_bytes(image_bytes)
                image_paths.append(image_path.name)

    print(f"🗃️ Extracted {len(image_paths)} images")
    logging.info(f"images extracted for {base_name} at {image_paths}")
    return image_paths