import csv
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

INAT_BASE_URL = os.getenv("INAT_BASE_URL")
INAT_QUALITY_GRADE = os.getenv("INAT_QUALITY_GRADE")
INAT_PER_PAGE = int(os.getenv("INAT_PER_PAGE"))
INAT_REQUEST_DELAY = float(os.getenv("INAT_REQUEST_DELAY"))
INAT_TIMEOUT = int(os.getenv("INAT_TIMEOUT"))

DATASET_DIR = os.getenv("DATASET_DIR")
MAX_IMAGES_PER_SPECIES = int(os.getenv("MAX_IMAGES_PER_SPECIES"))
LICENSES_CSV = os.getenv("LICENSES_CSV")


def download_inat_images(
    taxon_name: str,
    output_dir: str,
    max_images: int = MAX_IMAGES_PER_SPECIES,
    csv_path: str = None,
) -> None:
    """
    Downloads iNaturalist images for a species and records metadata
    (author, license, source URL) in a CSV.
    """
    os.makedirs(output_dir, exist_ok=True)

    if csv_path is None:
        csv_path = os.path.join(output_dir, "_licenses.csv")

    write_header = not os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        if write_header:
            writer.writerow(
                [
                    "filename",
                    "taxon_name",
                    "observation_id",
                    "photo_id",
                    "source_url",
                    "photo_url",
                    "author",
                    "license_code",
                ]
            )

        page = 1
        downloaded = 0
        skipped_no_license = 0

        while downloaded < max_images:
            resp = requests.get(
                INAT_BASE_URL,
                params={
                    "taxon_name": taxon_name,
                    "quality_grade": INAT_QUALITY_GRADE,
                    "photos": "true",
                    "per_page": INAT_PER_PAGE,
                    "page": page,
                },
                timeout=INAT_TIMEOUT,
            )

            resp.raise_for_status()

            results = resp.json().get("results", [])

            if not results:
                print(
                    f"[{taxon_name}] No more results "
                    f"(stopped at {downloaded} images)."
                )
                break

            for obs in results:
                license_code = obs.get("license_code")

                if not license_code:
                    skipped_no_license += 1
                    continue

                author = (obs.get("user") or {}).get(
                    "login",
                    "unknown",
                )

                obs_id = obs["id"]
                source_url = f"https://www.inaturalist.org/observations/{obs_id}"

                for photo in obs.get("photos", []):
                    if downloaded >= max_images:
                        break

                    photo_url = photo["url"].replace(
                        "square",
                        "medium",
                    )

                    photo_id = photo["id"]
                    fname = f"{obs_id}_{photo_id}.jpg"
                    fpath = os.path.join(output_dir, fname)

                    try:
                        img_resp = requests.get(
                            photo_url,
                            timeout=INAT_TIMEOUT,
                        )
                        img_resp.raise_for_status()
                    except requests.RequestException as exc:
                        print(f"Failed to download {photo_url}: {exc}")
                        continue

                    with open(fpath, "wb") as f:
                        f.write(img_resp.content)

                    writer.writerow(
                        [
                            fname,
                            taxon_name,
                            obs_id,
                            photo_id,
                            source_url,
                            photo_url,
                            author,
                            license_code,
                        ]
                    )

                    downloaded += 1

                if downloaded >= max_images:
                    break

            page += 1
            time.sleep(INAT_REQUEST_DELAY)

    print(
        f"[{taxon_name}] {downloaded} images downloaded "
        f"at '{output_dir}'. "
        f"Licenses registered at '{csv_path}'."
    )


if __name__ == "__main__":
    species_map = {
        "Tetragonisca angustula": os.path.join(DATASET_DIR, "jatai"),
        "Melipona marginata": os.path.join(DATASET_DIR, "manduri"),
        "Plebeia droryana": os.path.join(DATASET_DIR, "mirim"),
        "Melipona scutellaris": os.path.join(DATASET_DIR, "urucu"),
        "Melipona quadrifasciata": os.path.join(DATASET_DIR, "mandacaia"),
    }

    for taxon_name, output_dir in species_map.items():
        download_inat_images(
            taxon_name=taxon_name,
            output_dir=output_dir,
            max_images=MAX_IMAGES_PER_SPECIES,
            csv_path=LICENSES_CSV,
        )
