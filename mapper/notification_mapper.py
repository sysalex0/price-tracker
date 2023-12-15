def product_to_html_message(product):
    html = f"""
        <a href='{product.url}'>{product.search_keyword}, {product.currency}${product.price}, approx post time: {product.approx_posting_time}</a>
    """
    return html