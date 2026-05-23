from app.utils.io import load_csv, save_json
from app.utils.logger import setup_logger


def main() -> None:
    logger = setup_logger("day03", "logs/day03.log")
    rows = load_csv("data/jobs.csv")

    valid_jobs = []
    skipped = 0

    for row in rows:
        if not row.get("jd_text"):
            skipped += 1
            logger.warning("skip empty jd: %s", row.get("company"))
            continue

        valid_jobs.append(row)

    save_json(valid_jobs, "data/jobs.json")
    logger.info("saved jobs: %s, skipped: %s", len(valid_jobs), skipped)

    print(f"saved jobs={len(valid_jobs)}, skipped={skipped}")


if __name__ == "__main__":
    main()