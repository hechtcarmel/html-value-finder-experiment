EXAMPLES = [
    {
        "html": """
<div class="product-container">
  <h1>Premium Headphones</h1>
  <div class="price-container">
    <span class="price">$149.99</span>
    <span class="original-price">$199.99</span>
  </div>
  <button class="add-to-cart-btn">Add to Cart</button>
</div>
        """,
        "click_path": ["div.product-container", "button.add-to-cart-btn"],
        "button_text": "Add to Cart",
        "response": {
            "isValueClick": True,
            "value": 149.99,
            "currency": "USD"
        },
        "response_json": '{"isValueClick": true, "value": 149.99, "currency": "USD"}'
    },
    {
        "html": """
<div class="subscription-plan">
  <h2>Professional Plan</h2>
  <div class="plan-price">€29.99<span class="period">/month</span></div>
  <ul class="features">
    <li>Unlimited access</li>
    <li>Priority support</li>
  </ul>
  <button class="subscribe-btn">Subscribe Now</button>
</div>
        """,
        "click_path": ["div.subscription-plan", "button.subscribe-btn"],
        "button_text": "Subscribe Now",
        "response": {
            "isValueClick": True,
            "value": 29.99,
            "currency": "EUR"
        },
        "response_json": '{"isValueClick": true, "value": 29.99, "currency": "EUR"}'
    },
    {
        "html": """
<div class="article-container">
  <h1>How to Improve Your Productivity</h1>
  <p class="author">By John Doe</p>
  <div class="article-body">
    <p>First paragraph of the article...</p>
  </div>
  <button class="read-more-btn">Read More</button>
</div>
        """,
        "click_path": ["div.article-container", "button.read-more-btn"],
        "button_text": "Read More",
        "response": {
            "isValueClick": False,
            "value": None,
            "currency": None
        },
        "response_json": '{"isValueClick": false, "value": null, "currency": null}'
    },
    {
        "html": """
<div class="checkout-summary">
  <div class="items">
    <div class="item">
      <span class="item-name">Wireless Earbuds</span>
      <span class="item-price">£89.95</span>
    </div>
    <div class="item">
      <span class="item-name">Charging Case</span>
      <span class="item-price">£19.95</span>
    </div>
  </div>
  <div class="totals">
    <div class="subtotal">
      <span>Subtotal:</span>
      <span>£109.90</span>
    </div>
    <div class="tax">
      <span>VAT (20%):</span>
      <span>£21.98</span>
    </div>
    <div class="total">
      <span>Total:</span>
      <span>£131.88</span>
    </div>
  </div>
  <button id="complete-purchase">Complete Purchase</button>
</div>
        """,
        "click_path": ["div.checkout-summary", "button#complete-purchase"],
        "button_text": "Complete Purchase",
        "response": {
            "isValueClick": True,
            "value": 131.88,
            "currency": "GBP"
        },
        "response_json": '{"isValueClick": true, "value": 131.88, "currency": "GBP"}'
    },
    {
        "html": """
<div class="product-details">
  <h2>Smartphone XS Pro</h2>
  <div class="price-info">
    <div class="current-price">₹59,999</div>
    <div class="original-price"><s>₹69,999</s></div>
    <div class="discount">15% off</div>
  </div>
  <div class="product-actions">
    <button class="wishlist-btn">Add to Wishlist</button>
    <button class="buy-now-btn">Buy Now</button>
  </div>
</div>
        """,
        "click_path": ["div.product-details", "div.product-actions", "button.buy-now-btn"],
        "button_text": "Buy Now",
        "response": {
            "isValueClick": True,
            "value": 59999,
            "currency": "INR"
        },
        "response_json": '{"isValueClick": true, "value": 59999, "currency": "INR"}'
    },
    {
        "html": """
<div class="digital-download">
  <div class="content-details">
    <h3>Photography E-Book</h3>
    <div class="download-info">PDF Format (25MB)</div>
  </div>
  <div class="action-area">
    <div class="price">Free</div>
    <button class="download-button">Download</button>
  </div>
</div>
        """,
        "click_path": ["div.digital-download", "div.action-area", "button.download-button"],
        "button_text": "Download",
        "response": {
            "isValueClick": False,
            "value": None,
            "currency": None
        },
        "response_json": '{"isValueClick": false, "value": null, "currency": null}'
    }
] 