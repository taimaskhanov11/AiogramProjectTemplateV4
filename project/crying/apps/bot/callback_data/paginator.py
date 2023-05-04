from __future__ import annotations

from enum import StrEnum
from typing import Sequence, Callable, Any, TypeVar, Self

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton as IKButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

T = TypeVar("T")


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class PaginatorCallback(CallbackData, prefix="paginator"):
    offset: int = 0
    limit: int = 10
    sort_order: SortOrder | None = None

    def make(self, offset: int) -> Self:
        return PaginatorCallback(
            offset=offset,
            limit=self.limit,
            sort_order=self.sort_order
        )

    def next(self) -> Self:
        return self.make(self.offset + self.limit)

    def prev(self) -> Self:
        return self.make(self.offset - self.limit)

    def switch_to(self, page: int) -> Self:
        """
         Switch to page.
         Fist page is 0
        :param page:
        :return:
        """
        return self.make(page * self.limit)

    def switch_to_last(self, length: int) -> Self:
        return self.switch_to(length // self.limit)

    def switch_to_first(self) -> Self:
        return self.switch_to(0)

    def has_prev(self, page: int = 0) -> bool:
        return self.offset > page * self.limit

    def has_next(self, length: int, page: int = 0) -> bool:
        return self.offset + self.limit < length - page * self.limit

    def slice(self, items: Sequence[T]) -> Sequence[T]:
        return items[self.offset:self.offset + self.limit]

    def sort(self, items: list[T], key: Callable[[T], Any]) -> list[T]:
        if not self.sort_order:
            return items
        return sorted(items, key=key, reverse=self.sort_order == SortOrder.DESC)

    def add_pagination_buttons(self, builder: InlineKeyboardBuilder, length: int):
        prev5offset = self.offset - 5 * self.limit
        has5prev = self.has_prev(5)
        has5prev_cd = self.make(prev5offset).pack() if has5prev else self.switch_to_first().pack()

        next5offset = self.offset + 5 * self.limit
        has5next = self.has_next(length, 5)
        has5next_cd = self.make(next5offset).pack() if has5next else self.switch_to_last(length).pack()

        has1prev_cd = self.prev().pack() if self.has_prev() else self.switch_to_last(length).pack()
        has1next_cd = self.next().pack() if self.has_next(length) else self.switch_to_first().pack()
        builder.row(
            # В самое начало
            IKButton(text="≪", callback_data=self.switch_to_first().pack()),
            # Назад на 5 страниц
            IKButton(text="≺5", callback_data=has5prev_cd),
            # Назад на 1 страницу
            IKButton(text="≺", callback_data=has1prev_cd),
            # Вперед на 1 страницу
            IKButton(text="≻", callback_data=has1next_cd),
            # по 5 страниц вперед
            IKButton(text="5≻", callback_data=has5next_cd),
            # В самый конец
            IKButton(text="≫", callback_data=self.switch_to_last(length).pack())
        )
        counter_str = f"{self.offset // self.limit + 1} / {length // self.limit + 1}"
        builder.row(IKButton(text=counter_str, callback_data="None"))

    # Кнопки сортировки по убыванию и возрастанию
    def add_sort_buttons(self, builder: InlineKeyboardBuilder):
        asc_callback = self.make(self.offset)
        asc_callback.sort_order = SortOrder.ASC
        default_callback = self.make(self.offset)
        default_callback.sort_order = None
        desc_callback = self.make(self.offset)
        desc_callback.sort_order = SortOrder.DESC
        builder.row(
            IKButton(
                text="🔺",
                callback_data=asc_callback.pack()
            ),
            IKButton(
                text="🌟",
                callback_data=default_callback.pack()
            ),
            IKButton(
                text="🔻",
                callback_data=desc_callback.pack()
            )
        )

    def get_keyboard(self, length: int = 0) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        self.add_pagination_buttons(builder, length)
        self.add_sort_buttons(builder)
        return builder.as_markup()
