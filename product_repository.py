from sqlalchemy import text
from db import get_engine


def slug_exists(slug: str) -> bool:
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT 1 FROM products WHERE slug = :slug LIMIT 1"),
            {"slug": slug}
        ).fetchone()
        return res is not None


def upsert_product(p: dict):
    """
    Centralized DB write.
    Applies safe defaults for fields not controlled by UI.
    """

    # ✅ SAFETY DEFAULTS (IMPORTANT)
    p = {
        **p,
        "inventory": p.get("inventory", 0),
        "moq": p.get("moq", 1),
        "max_per_order": p.get("max_per_order", None),
    }

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO products (
                    slug, title, description, price_paise, currency,
                    sizes, colors, material,
                    inventory, moq, max_per_order,
                    category, tags,
                    media_urls, thumbnail_url,
                    is_active, group_key, color_hex,
                    created_at, updated_at
                )
                VALUES (
                    :slug, :title, :description, :price_paise, :currency,
                    :sizes, :colors, :material,
                    :inventory, :moq, :max_per_order,
                    :category, :tags,
                    :media_urls, :thumbnail_url,
                    :is_active, :group_key, :color_hex,
                    :created_at, :updated_at
                )
                ON CONFLICT (slug) DO UPDATE SET
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    price_paise = EXCLUDED.price_paise,
                    sizes = EXCLUDED.sizes,
                    colors = EXCLUDED.colors,
                    inventory = EXCLUDED.inventory,
                    media_urls = EXCLUDED.media_urls,
                    thumbnail_url = EXCLUDED.thumbnail_url,
                    updated_at = NOW();
            """),
            p
        )
