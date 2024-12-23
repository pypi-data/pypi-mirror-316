from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chat_response import ChatResponse


T = TypeVar("T", bound="PaginatedResponseChatResponse")


@_attrs_define
class PaginatedResponseChatResponse:
    """
    Example:
        {'has_next': True, 'has_prev': False, 'items': [], 'page': 1, 'pages': 5, 'size': 10, 'total': 50}

    Attributes:
        items (list['ChatResponse']): List of items for the current page
        total (int): Total number of items
        page (int): Current page number
        size (int): Items per page
        pages (int): Total number of pages
        has_next (bool): Whether there is a next page
        has_prev (bool): Whether there is a previous page
    """

    items: list["ChatResponse"]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        total = self.total

        page = self.page

        size = self.size

        pages = self.pages

        has_next = self.has_next

        has_prev = self.has_prev

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "total": total,
                "page": page,
                "size": size,
                "pages": pages,
                "has_next": has_next,
                "has_prev": has_prev,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.chat_response import ChatResponse

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ChatResponse.from_dict(items_item_data)

            items.append(items_item)

        total = d.pop("total")

        page = d.pop("page")

        size = d.pop("size")

        pages = d.pop("pages")

        has_next = d.pop("has_next")

        has_prev = d.pop("has_prev")

        paginated_response_chat_response = cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev,
        )

        paginated_response_chat_response.additional_properties = d
        return paginated_response_chat_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
