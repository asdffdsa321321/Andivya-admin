import streamlit as st
import re
from datetime import datetime
from cloudinary_utils import upload_image
from product_repository import slug_exists, upsert_product


def slugify(title: str, color: str, group_key: str | None) -> str:
    """
    Slug format:
    title-color-groupkey (group_key optional)
    """
    parts = [title, color]

    if group_key:
        parts.append(group_key)

    base = "-".join(parts)
    return re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")


def render():
    st.header("Product Uploader")

    # ─────────────────────────
    # Images
    # ─────────────────────────
    files = st.file_uploader(
        "Upload product images",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )

    if files:
        st.image(files, width=120)

    st.divider()

    # ─────────────────────────
    # Core fields
    # ─────────────────────────
    title = st.text_input("Title")
    price = st.number_input("Price (INR)", min_value=1.0, step=1.0)
    category = st.text_input("Category")
    description = st.text_area("Description")

    group_key = st.text_input("Group Key (for variants)")
    color_hex = st.color_picker("Primary Color (UI)", "#d34da0")

    sizes = st.multiselect(
        "Sizes",
        ["XS", "S", "M", "L", "XL", "2XL", "3XL"],
        default=["XS", "S", "M", "L", "XL", "2XL", "3XL"]
    )

    # ✅ SINGLE COLOR INPUT (REQUIRED)
    color_text = st.text_input(
        "Color (single value, e.g. Magenta, Indigo, Blue)"
    )

    is_active = st.checkbox("Active", value=True)

    # ─────────────────────────
    # Save
    # ─────────────────────────
    if st.button("Save Product", type="primary"):
        if not files or not title:
            st.error("Images and title are required")
            return

        if not color_text.strip():
            st.error("Color is required to create unique product variants")
            return

        normalized_color = color_text.strip().upper()

        slug = slugify(
            title=title.strip(),
            color=normalized_color.lower(),
            group_key=group_key.strip() if group_key else None
        )

        if slug_exists(slug):
            st.error(f"Slug already exists: {slug}")
            st.stop()

        urls = [upload_image(f) for f in files]

        product = {
            "slug": slug,
            "title": title.strip(),
            "description": description,
            "price_paise": int(price * 100),
            "currency": "INR",
            "sizes": sizes or None,
            "colors": [normalized_color],      # ✅ TEXT[] with ONE UPPERCASE value
            "material": None,
            # inventory / moq / max_per_order intentionally omitted
            "category": category,
            "tags": None,
            "media_urls": urls,
            "thumbnail_url": urls[0],
            "is_active": is_active,
            "group_key": group_key or None,
            "color_hex": color_hex,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        upsert_product(product)
        st.success("Product saved successfully")
