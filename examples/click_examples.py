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
        "button_text": "Add to Cart",
        "response": {
            "value": 149.99,
            "currency": "USD"
        },
        "response_json": '{"value": 149.99, "currency": "USD"}'
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
        "button_text": "Subscribe Now",
        "response": {
            "value": 29.99,
            "currency": "EUR"
        },
        "response_json": '{"value": 29.99, "currency": "EUR"}'
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
        "button_text": "Read More",
        "response": {
            "value": None,
            "currency": None
        },
        "response_json": '{"value": null, "currency": null}'
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
        "button_text": "Complete Purchase",
        "response": {
            "value": 131.88,
            "currency": "GBP"
        },
        "response_json": '{"value": 131.88, "currency": "GBP"}'
    },
    {
        "html": """
<div class="product-grid">
  <div class="product-card">
    <h2>Product A</h2>
    <div class="price">$19.99</div>
    <button class="buy-btn">Buy Now</button>
  </div>
  <div class="product-card">
    <h2>Product B</h2>
    <div class="price">$25.50</div>
    <button class="buy-btn">Buy Now</button>
  </div>
  <div class="product-card main-product">
    <h2>Product C (Featured)</h2>
    <div class="price">$30.00</div>
    <button class="buy-btn special-offer">Buy Now</button>
  </div>
</div>
        """,
        "button_text": "Buy Now",
        "response": {
            "value": None,
            "currency": None
        },
        "response_json": '{"value": null, "currency": null}'
    },
    {
        "html": """
<div class="product-grid">
  <div class="product-card">
    <h2>Product A</h2>
    <div class="price">$19.99</div>
    <button class="buy-btn">Buy Product A</button>
  </div>
  <div class="product-card">
    <h2>Product B</h2>
    <div class="price">$25.50</div>
    <button class="buy-btn">Buy Product B</button>
  </div>
  <div class="product-card main-product">
    <h2>Product C (Featured)</h2>
    <div class="price">$30.00</div>
    <button class="buy-btn special-offer">Buy Featured Product C</button>
  </div>
</div>
        """,
        "button_text": "Buy Featured Product C",
        "response": {
            "value": 30.00,
            "currency": "USD"
        },
        "response_json": '{"value": 30.00, "currency": "USD"}'
    },
    {
        "html": """
<div class="cart-item">
  <img src="item1.jpg" alt="Item 1">
  <div class="item-details">
    <h3>Item 1</h3>
    <p>Price: 50 ILS</p>
  </div>
  <button class="remove-item">Remove</button>
</div>
<div class="cart-item">
  <img src="item2.jpg" alt="Item 2">
  <div class="item-details">
    <h3>Item 2</h3>
    <p>Price: 75 ILS</p>
  </div>
  <button class="remove-item">Remove</button>
</div>
<div class="cart-summary">
  <p>Total: 125 ILS</p>
  <button class="checkout">Checkout</button>
</div>
        """,
        "button_text": "Checkout",
        "response": {
            "value": 125,
            "currency": "ILS"
        },
        "response_json": '{"value": 125, "currency": "ILS"}'
    },
    {
        "html": """
<div class="cart-item">
  <img src="item1.jpg" alt="Item 1">
  <div class="item-details">
    <h3>Item 1</h3>
    <p>Price: 50 ILS</p>
  </div>
  <button class="remove-item">Remove Item 1</button>
</div>
<div class="cart-item">
  <img src="item2.jpg" alt="Item 2">
  <div class="item-details">
    <h3>Item 2</h3>
    <p>Price: 75 ILS</p>
  </div>
  <button class="remove-item">Remove Item 2</button>
</div>
<div class="cart-summary">
  <p>Total: 125 ILS</p>
  <button class="checkout">Checkout</button>
</div>
        """,
        "button_text": "Remove Item 2",
        "response": {
            "value": 75,
            "currency": "ILS"
        },
        "response_json": '{"value": 75, "currency": "ILS"}'
    }
] 