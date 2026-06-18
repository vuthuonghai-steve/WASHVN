"""sample_clean.py — fixture dùng cho self-test. Đạt chuẩn Google review."""

from typing import Optional


class BillingService:
    """Service tính toán billing với dependency injection cho repository."""

    DEFAULT_TIMEOUT_SEC = 10

    def __init__(self, repository, logger=None) -> None:
        """Khởi tạo với repository (DI) và logger tùy chọn."""
        self._repository = repository
        self._logger = logger

    def calculate_total(self, user_id: str) -> float:
        """Tính tổng chi phí cho user. Trả về 0 nếu user không tồn tại.

        Args:
            user_id: ID của user cần tính.

        Returns:
            Tổng chi phí dưới dạng float. Trả 0.0 khi không có record.
        """
        if not user_id:
            return 0.0
        try:
            record = self._repository.fetch(user_id, timeout=self.DEFAULT_TIMEOUT_SEC)
        except IOError as exc:
            if self._logger is not None:
                self._logger.error("billing fetch failed: %s", exc)
            return 0.0
        return self._sum_amounts(record.items)

    def _sum_amounts(self, items) -> float:
        """Helper cô lập để dễ test độc lập."""
        return float(sum(item.amount for item in items))


def load_config(path: str) -> Optional[dict]:
    """Đọc config từ file path. Trả None nếu file không tồn tại.

    Args:
        path: Đường dẫn tuyệt đối tới config file.

    Returns:
        Dict config hoặc None.
    """
    try:
        with open(path, encoding="utf-8") as handle:
            return _parse(handle.read())
    except OSError:
        return None


def _parse(raw: str) -> dict:
    """Parse raw text thành dict. Tách riêng để testable."""
    return {"raw": raw}
