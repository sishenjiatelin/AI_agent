from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.io_utils import load_csv, save_json, setup_logger


def normalize_job(
    row: dict[str, str],
    row_number: int,
    logger,
) -> dict[str, object] | None:
    """清洗单条岗位数据；如果 jd_text 为空，返回 None。"""
    company = (row.get("company") or "").strip()
    title = (row.get("title") or "").strip()
    jd_text = (row.get("jd_text") or "").strip()
    source = (row.get("source") or "").strip()

    if not jd_text:
        logger.warning(
            f"第{row_number}行跳过：jd_text 为空。company={company}, title={title}",

        )
        return None
    
    if not title:
        logger.warning(
            f"第{row_number}行跳过：jd_text={jd_text}。company={company}, title 为空",

        )
        return None

    return {
        "id": row_number,
        "company": company,
        "title": title,
        "jd_text": jd_text,
        "source": source,
    }


def convert_jobs(
    csv_path: str = "data/jobs.csv",
    json_path: str = "data/jobs.json",
) -> None:
    """把岗位 CSV 转换成 JSON，并记录处理日志。"""
    logger = setup_logger("day03_convert", "logs/day03_convert.log")

    logger.info("开始转换岗位数据：%s -> %s", csv_path, json_path)

    rows = load_csv(csv_path)
    jobs: list[dict[str, object]] = []
    skipped_count = 0

    for row_number, row in enumerate(rows, start=1):
        job = normalize_job(row, row_number, logger)
        if job is None:
            skipped_count += 1
            continue

        jobs.append(job)
    
    result = {
        "total_rows": len(rows),
        "success_count": len(jobs),
        "skipped_count": skipped_count,
        "jobs": jobs,
    }

    save_json(result, json_path)

    logger.info(
        "转换完成：总计 %s 条，成功 %s 条，跳过 %s 条，输出文件：%s",
        len(rows),
        len(jobs),
        skipped_count,
        json_path,
    )



if __name__ == "__main__":
    convert_jobs()